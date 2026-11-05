import json
import os
import plistlib
import re
import shutil
import subprocess
import tempfile
import time
import tokenize
import warnings

try:
    import importlib_resources as resources
except ImportError:
    from importlib import resources

from ds_store import DSStore
from mac_alias import Alias

from . import colors, licensing

try:
    from . import badge
except ImportError:
    badge = None


DISKUTIL = "/usr/sbin/diskutil"
HDIUTIL = "/usr/bin/hdiutil"

# The output formats that ``diskutil image create from`` can produce.
SUPPORTED_FORMATS = ("UDRO", "UDZO", "ULFO", "ULMO", "UDSB", "RAW", "ASIF")

# The filesystems dmgbuild can create in the image.
SUPPORTED_FILESYSTEMS = ("HFS+", "APFS")


class DMGError(Exception):
    def __init__(self, callback, message):
        self.message = message
        callback({"type": "error::fatal", "message": message})

    def __str__(self):
        return str(self.message)


def quiet_callback(info):
    pass


def run_tool(args, plist=True):
    """Run a command line tool, returning ``(retcode, output)``.

    If ``plist`` is true and the tool succeeds, ``output`` is the tool's standard
    output parsed as a plist. Otherwise, ``output`` is the tool's text output
    (standard output followed by standard error).
    """
    p = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE if plist else subprocess.STDOUT,
        check=False,
    )
    if plist and p.returncode == 0:
        return p.returncode, plistlib.loads(p.stdout)
    output = p.stdout + (p.stderr or b"")
    return p.returncode, output.decode(errors="replace")


def eject(device, force=False):
    """Eject a disk, and everything on it, given its name (e.g. ``disk5``)."""
    args = [DISKUTIL, "eject"]
    if force:
        args.append("force")
    args.append(device)
    return run_tool(args, plist=False)


def newfs_command(filesystem, volume_name, device):
    """Return the command that creates ``filesystem`` on the whole of ``device``."""
    if filesystem == "APFS":
        return ["/sbin/newfs_apfs", "-v", volume_name, f"/dev/{device}"]
    return [
        "/sbin/newfs_hfs",
        "-v",
        volume_name,
        "-c",
        "c=64,a=16,e=16",
        f"/dev/r{device}",
    ]


def load_settings(filename, settings):
    encoding = "utf-8"
    with open(filename, "rb") as fp:
        try:
            encoding = tokenize.detect_encoding(fp.readline)[0]
        except SyntaxError:
            pass

    with open(filename, encoding=encoding) as fp:
        exec(compile(fp.read(), filename, "exec"), settings, settings)


def load_json(filename, settings):
    """Read an appdmg .json spec.

    Uses the defaults for appdmg, rather than the usual defaults for
    dmgbuild.
    """

    with open(filename) as fp:
        json_data = json.load(fp)

    if "title" not in json_data:
        raise ValueError("missing 'title' in JSON settings file")
    if "contents" not in json_data:
        raise ValueError("missing 'contents' in JSON settings file")

    settings["volume_name"] = json_data["title"]
    settings["icon"] = json_data.get("icon", None)
    settings["badge_icon"] = json_data.get("badge-icon", None)
    bk = json_data.get("background", None)
    if bk is None:
        bk = json_data.get("background-color", None)
    if bk is not None:
        settings["background"] = bk
    settings["icon_size"] = json_data.get("icon-size", 80)
    tsize = json_data.get("text-size", None)
    if tsize is not None:
        settings["text_size"] = tsize
    wnd = json_data.get(
        "window",
        {
            "position": {"x": 100, "y": 100},
            "size": {"width": 640, "height": 480},
        },
    )
    pos = wnd.get("position", {"x": 100, "y": 100})
    siz = wnd.get("size", {"width": 640, "height": 480})
    settings["window_rect"] = (
        (pos.get("x", 100), pos.get("y", 100)),
        (siz.get("width", 640), siz.get("height", 480)),
    )
    settings["format"] = json_data.get("format", "UDZO")
    settings["filesystem"] = json_data.get("filesystem", "HFS+")
    settings["compression_level"] = json_data.get("compression-level", None)
    settings["license"] = json_data.get("license", None)
    settings["size"] = json_data.get("size", None)
    settings["shrink"] = json_data.get("shrink", True)
    files = []
    hide = []
    hide_extensions = []
    symlinks = {}
    icon_locations = {}
    for fileinfo in json_data.get("contents", []):
        if "path" not in fileinfo:
            raise ValueError("missing 'path' in contents in JSON settings file")
        if "x" not in fileinfo:
            raise ValueError("missing 'x' in contents in JSON settings file")
        if "y" not in fileinfo:
            raise ValueError("missing 'y' in contents in JSON settings file")

        kind = fileinfo.get("type", "file")
        path = fileinfo["path"]
        name = fileinfo.get("name", os.path.basename(path.rstrip("/")))
        if kind == "file":
            files.append((path, name))
        elif kind == "link":
            symlinks[name] = path
        elif kind == "position":
            pass
        icon_locations[name] = (fileinfo["x"], fileinfo["y"])
        hide_ext = fileinfo.get("hide_extension", False)
        if hide_ext:
            hide_extensions.append(name)
        hidden = fileinfo.get("hidden", False)
        if hidden:
            hide.append(name)

    settings["files"] = files
    settings["hide_extensions"] = hide_extensions
    settings["hide"] = hide
    settings["symlinks"] = symlinks
    settings["icon_locations"] = icon_locations


def build_dmg(
    filename,
    volume_name,
    settings_file=None,
    settings=None,
    defines=None,
    lookForHiDPI=True,
    detach_retries=12,
    callback=quiet_callback,
):
    if defines is None:
        defines = {}
    if settings is None:
        settings = {}
    options = {
        # Default settings
        "filename": filename,
        "volume_name": volume_name,
        "format": "ULFO",
        "filesystem": "HFS+",
        "compression_level": None,
        "size": None,
        "shrink": True,
        "files": [],
        "symlinks": {},
        "hide": [],
        "hide_extensions": [],
        "icon": None,
        "badge_icon": None,
        "background": None,
        "show_status_bar": False,
        "show_tab_view": False,
        "show_toolbar": False,
        "show_pathbar": False,
        "show_sidebar": False,
        "sidebar_width": 180,
        "arrange_by": None,
        "grid_offset": (0, 0),
        "grid_spacing": 100.0,
        "scroll_position": (0.0, 0.0),
        "show_icon_preview": False,
        "show_item_info": False,
        "label_pos": "bottom",
        "text_size": 16.0,
        "icon_size": 128.0,
        "include_icon_view_settings": "auto",
        "include_list_view_settings": "auto",
        "list_icon_size": 16.0,
        "list_text_size": 12.0,
        "list_scroll_position": (0, 0),
        "list_sort_by": "name",
        "list_use_relative_dates": True,
        "list_calculate_all_sizes": False,
        "list_columns": ("name", "date-modified", "size", "kind", "date-added"),
        "list_column_widths": {
            "name": 300,
            "date-modified": 181,
            "date-created": 181,
            "date-added": 181,
            "date-last-opened": 181,
            "size": 97,
            "kind": 115,
            "label": 100,
            "version": 75,
            "comments": 300,
        },
        "list_column_sort_directions": {
            "name": "ascending",
            "date-modified": "descending",
            "date-created": "descending",
            "date-added": "descending",
            "date-last-opened": "descending",
            "size": "descending",
            "kind": "ascending",
            "label": "ascending",
            "version": "ascending",
            "comments": "ascending",
        },
        "window_rect": ((100, 100), (640, 280)),
        "default_view": "icon-view",
        "icon_locations": {},
        "license": None,
        "defines": defines,
    }

    callback({"type": "build::started"})

    # Execute the settings file
    if settings_file:
        callback(
            {
                "type": "operation::start",
                "operation": "settings::load",
            }
        )

        # We now support JSON settings files using appdmg's format
        if settings_file.endswith(".json"):
            load_json(settings_file, options)
        else:
            load_settings(settings_file, options)

        callback(
            {
                "type": "operation::finished",
                "operation": "settings::load",
            }
        )

    # Add any overrides
    options.update(settings)

    # Validate the settings before doing any work.
    filesystem = str(options["filesystem"]).upper()
    if filesystem not in SUPPORTED_FILESYSTEMS:
        raise DMGError(
            callback,
            f"Unsupported filesystem {options['filesystem']!r}; "
            f"must be one of {', '.join(SUPPORTED_FILESYSTEMS)}",
        )

    image_format = options["format"]
    if image_format not in SUPPORTED_FORMATS:
        raise DMGError(
            callback,
            f"Unsupported format {image_format!r}; "
            f"must be one of {', '.join(SUPPORTED_FORMATS)}",
        )

    if options["compression_level"]:
        warnings.warn(
            "The compression_level setting is no longer supported, "
            "and will be ignored.",
            UserWarning,
            stacklevel=2,
        )

    if options["license"]:
        warnings.warn(
            "Apple has deprecated the mechanism used to embed license agreements "
            "in disk images. The license setting will be removed in a future "
            "release of dmgbuild.",
            FutureWarning,
            stacklevel=2,
        )

    # Set up the finder data
    bounds = options["window_rect"]

    bounds_string = (
        f"{{{{{bounds[0][0]}, {bounds[0][1]}}}, {{{bounds[1][0]}, {bounds[1][1]}}}}}"
    )
    bwsp = {
        "ShowStatusBar": options["show_status_bar"],
        "WindowBounds": bounds_string,
        "ContainerShowSidebar": False,
        "PreviewPaneVisibility": False,
        "SidebarWidth": options["sidebar_width"],
        "ShowTabView": options["show_tab_view"],
        "ShowToolbar": options["show_toolbar"],
        "ShowPathbar": options["show_pathbar"],
        "ShowSidebar": options["show_sidebar"],
    }

    arrange_options = {
        "name": "name",
        "date-modified": "dateModified",
        "date-created": "dateCreated",
        "date-added": "dateAdded",
        "date-last-opened": "dateLastOpened",
        "size": "size",
        "kind": "kind",
        "label": "label",
    }

    icvp = {
        "viewOptionsVersion": 1,
        "backgroundType": 0,
        "backgroundColorRed": 1.0,
        "backgroundColorGreen": 1.0,
        "backgroundColorBlue": 1.0,
        "gridOffsetX": float(options["grid_offset"][0]),
        "gridOffsetY": float(options["grid_offset"][1]),
        "gridSpacing": float(options["grid_spacing"]),
        "arrangeBy": str(arrange_options.get(options["arrange_by"], "none")),
        "showIconPreview": bool(options["show_icon_preview"]),
        "showItemInfo": bool(options["show_item_info"]),
        "labelOnBottom": options["label_pos"] == "bottom",
        "textSize": float(options["text_size"]),
        "iconSize": float(options["icon_size"]),
        "scrollPositionX": float(options["scroll_position"][0]),
        "scrollPositionY": float(options["scroll_position"][1]),
    }

    background = options["background"]

    columns = {
        "name": "name",
        "date-modified": "dateModified",
        "date-created": "dateCreated",
        "date-added": "dateAdded",
        "date-last-opened": "dateLastOpened",
        "size": "size",
        "kind": "kind",
        "label": "label",
        "version": "version",
        "comments": "comments",
    }

    default_widths = {
        "name": 300,
        "date-modified": 181,
        "date-created": 181,
        "date-added": 181,
        "date-last-opened": 181,
        "size": 97,
        "kind": 115,
        "label": 100,
        "version": 75,
        "comments": 300,
    }

    default_sort_directions = {
        "name": "ascending",
        "date-modified": "descending",
        "date-created": "descending",
        "date-added": "descending",
        "date-last-opened": "descending",
        "size": "descending",
        "kind": "ascending",
        "label": "ascending",
        "version": "ascending",
        "comments": "ascending",
    }

    lsvp = {
        "viewOptionsVersion": 1,
        "sortColumn": columns.get(options["list_sort_by"], "name"),
        "textSize": float(options["list_text_size"]),
        "iconSize": float(options["list_icon_size"]),
        "showIconPreview": options["show_icon_preview"],
        "scrollPositionX": options["list_scroll_position"][0],
        "scrollPositionY": options["list_scroll_position"][1],
        "useRelativeDates": options["list_use_relative_dates"],
        "calculateAllSizes": options["list_calculate_all_sizes"],
    }

    lsvp["columns"] = {}
    cndx = {}

    for n, column in enumerate(options["list_columns"]):
        cndx[column] = n
        width = options["list_column_widths"].get(column, default_widths[column])
        asc = (
            options["list_column_sort_directions"].get(
                column, default_sort_directions[column]
            )
            == "ascending"
        )

        lsvp["columns"][columns[column]] = {
            "index": n,
            "width": width,
            "identifier": columns[column],
            "visible": True,
            "ascending": asc,
        }

    n = len(options["list_columns"])
    for k in columns:
        if cndx.get(k) is None:
            cndx[k] = n
            width = default_widths[k]
            asc = default_sort_directions[k] == "ascending"

        lsvp["columns"][columns[column]] = {
            "index": n,
            "width": width,
            "identifier": columns[column],
            "visible": False,
            "ascending": asc,
        }

        n += 1

    default_view = options["default_view"]
    views = {
        "icon-view": b"icnv",
        "column-view": b"clmv",
        "list-view": b"Nlsv",
        "coverflow": b"Flwv",
    }

    icvl = (b"type", views.get(default_view, "icnv"))

    include_icon_view_settings = default_view == "icon-view" or options[
        "include_icon_view_settings"
    ] not in ("auto", "no", 0, False, None)
    include_list_view_settings = default_view in ("list-view", "coverflow") or options[
        "include_list_view_settings"
    ] not in ("auto", "no", 0, False, None)

    filename = options["filename"]
    volume_name = options["volume_name"]

    # Construct a writeable image to start with
    dirname, basename = os.path.split(os.path.realpath(filename))
    if not basename.endswith(".dmg"):
        basename += ".dmg"
    writableFile = tempfile.NamedTemporaryFile(
        dir=dirname, prefix=".temp", suffix=basename
    )

    callback(
        {
            "type": "operation::start",
            "operation": "size::calculate",
        }
    )

    total_size = options["size"]
    if total_size is None:
        # Start with a size of 128MB - this way we don't need to calculate the
        # size of the background image, volume icon, and .DS_Store file (and
        # 128 MB should be well sufficient for even the most outlandish image
        # sizes, like an uncompressed 5K multi-resolution TIFF)
        total_size = 128 * 1024 * 1024

        def roundup(x, n):
            return x if x % n == 0 else x + n - x % n

        for path in options["files"]:
            if isinstance(path, tuple):
                path = path[0]

            if not os.path.islink(path) and os.path.isdir(path):
                for dirpath, _dirnames, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += roundup(os.lstat(fp).st_size, 4096)
            else:
                total_size += roundup(os.lstat(path).st_size, 4096)

        for name, target in options["symlinks"].items():
            total_size += 4096

        total_size = str(total_size)

    callback(
        {
            "type": "operation::finished",
            "operation": "size::calculate",
            "size": total_size,
        }
    )

    callback(
        {
            "type": "command::start",
            "command": "diskutil::create",
        }
    )

    # Create a raw image with no filesystem (and no partition map); the
    # filesystem is created on the whole disk below.
    ret, output = run_tool(
        [
            DISKUTIL,
            "image",
            "create",
            "blank",
            "--plist",
            "--format",
            "RAW",
            "--fs",
            "None",
            "--size",
            str(total_size),
            writableFile.name,
        ]
    )

    callback(
        {
            "type": "command::finished",
            "command": "diskutil::create",
            "ret": ret,
            "output": output,
        }
    )

    if ret:
        raise DMGError(callback, f"Unable to create disk image: {output}")

    callback(
        {
            "type": "command::start",
            "command": "diskutil::format",
        }
    )

    ret, output = run_tool(
        [DISKUTIL, "image", "attach", "--plist", "--noMount", writableFile.name]
    )
    if ret:
        raise DMGError(callback, f"Unable to attach disk image: {output}")

    device = output["system-entities"][0]["dev-entry"]
    ret, output = run_tool(newfs_command(filesystem, volume_name, device), plist=False)
    if ret:
        eject(device, force=True)
        raise DMGError(callback, f"Unable to create {filesystem} filesystem: {output}")

    ret, eject_output = eject(device)

    callback(
        {
            "type": "command::finished",
            "command": "diskutil::format",
            "ret": ret,
            "output": output,
        }
    )

    if ret:
        eject(device, force=True)
        raise DMGError(callback, f"Unable to detach disk image: {eject_output}")

    callback(
        {
            "type": "command::start",
            "command": "diskutil::attach",
        }
    )

    ret, output = run_tool(
        [
            DISKUTIL,
            "image",
            "attach",
            "--plist",
            "--nobrowse",
            "--mountOptions",
            "noowners",
            writableFile.name,
        ]
    )

    callback(
        {
            "type": "command::finished",
            "command": "diskutil::attach",
            "ret": ret,
            "output": output,
        }
    )

    if ret:
        raise DMGError(callback, f"Unable to attach disk image: {output}")

    # The first entity is the image's whole disk; ejecting it also ejects any
    # volumes on it (including APFS volumes, which are on a synthesized disk).
    device = output["system-entities"][0]["dev-entry"]

    callback(
        {
            "type": "operation::start",
            "operation": "dmg::create",
        }
    )

    try:
        mount_points = [
            info["mount-point"]
            for info in output["system-entities"]
            if info.get("mount-point")
        ]
        if not mount_points:
            raise DMGError(callback, f"Disk image was not mounted: {output}")
        mount_point = mount_points[0]

        icon = options["icon"]
        if badge:
            badge_icon = options["badge_icon"]
        else:
            badge_icon = None
        icon_target_path = os.path.join(mount_point, ".VolumeIcon.icns")
        if icon:
            shutil.copyfile(icon, icon_target_path)
        elif badge_icon:
            badge.badge_disk_icon(badge_icon, icon_target_path)

        if icon or badge_icon:
            subprocess.check_call(["/usr/bin/SetFile", "-a", "C", mount_point])

        callback(
            {
                "type": "operation::start",
                "operation": "background::create",
            }
        )

        if not isinstance(background, str):
            pass
        elif colors.isAColor(background):
            c = colors.parseColor(background).to_rgb()

            icvp["backgroundType"] = 1
            icvp["backgroundColorRed"] = float(c.r)
            icvp["backgroundColorGreen"] = float(c.g)
            icvp["backgroundColorBlue"] = float(c.b)
        else:
            if os.path.isfile(background):
                # look to see if there are HiDPI resources available

                if lookForHiDPI is True:
                    name, extension = os.path.splitext(os.path.basename(background))
                    orderedImages = [background]
                    imageDirectory = os.path.dirname(background)
                    if imageDirectory == "":
                        imageDirectory = "."
                    for candidateName in os.listdir(imageDirectory):
                        hasScale = re.match(
                            r"^(?P<name>.+)@(?P<scale>\d+)x(?P<extension>\.\w+)$",
                            candidateName,
                        )
                        if (
                            hasScale
                            and name == hasScale.group("name")
                            and extension == hasScale.group("extension")
                        ):
                            scale = int(hasScale.group("scale"))
                            if len(orderedImages) < scale:
                                orderedImages += [None] * (scale - len(orderedImages))
                            orderedImages[scale - 1] = os.path.join(
                                imageDirectory, candidateName
                            )

                    if len(orderedImages) > 1:
                        # compile the grouped tiff
                        backgroundFile = tempfile.NamedTemporaryFile(suffix=".tiff")
                        background = backgroundFile.name
                        output = tempfile.TemporaryFile(mode="w+")
                        try:
                            subprocess.check_call(
                                ["/usr/bin/tiffutil", "-cathidpicheck"]
                                + list(filter(None, orderedImages))
                                + ["-out", background],
                                stdout=output,
                                stderr=output,
                            )
                        except Exception as e:
                            output.seek(0)
                            raise ValueError(
                                f"unable to compile combined HiDPI file {background!r} "
                                f"got error: {e!s}\noutput: {output.read()}"
                            )

                _, kind = os.path.splitext(background)
                path_in_image = os.path.join(mount_point, ".background" + kind)
                shutil.copyfile(background, path_in_image)
            else:
                dmg_resources = resources.files("dmgbuild")
                bg_resource = dmg_resources.joinpath(
                    "resources/" + background + ".tiff"
                )
                if bg_resource.is_file():
                    path_in_image = os.path.join(mount_point, ".background.tiff")
                    with (
                        bg_resource.open("rb") as in_file,
                        open(path_in_image, "wb") as out_file,
                    ):
                        out_file.write(in_file.read())
                else:
                    raise ValueError(f'background file "{background}" not found')

            alias = Alias.for_file(path_in_image)

            icvp["backgroundType"] = 2
            icvp["backgroundImageAlias"] = alias.to_bytes()

        callback(
            {
                "type": "operation::finished",
                "operation": "background::create",
            }
        )

        callback(
            {
                "type": "operation::start",
                "operation": "files::add",
                "total": len(options["files"]),
            }
        )

        for f in options["files"]:
            if isinstance(f, tuple):
                f_in_image = os.path.join(mount_point, f[1])
                f = f[0]
            else:
                basename = os.path.basename(f.rstrip("/"))
                f_in_image = os.path.join(mount_point, basename)

            callback(
                {
                    "type": "operation::start",
                    "operation": "file::add",
                    "file": f_in_image,
                }
            )

            # use system ditto command to preserve code signing, etc.
            p = subprocess.run(
                ["/usr/bin/ditto", f, f_in_image],
                check=False,
                stderr=subprocess.PIPE,
                text=True,
            )
            if p.returncode:
                raise DMGError(
                    callback,
                    f"Unable to copy {f!r} into disk image: {p.stderr.strip()}",
                )

            callback(
                {
                    "type": "operation::finished",
                    "operation": "file::add",
                    "file": f_in_image,
                }
            )

        callback(
            {
                "type": "operation::finished",
                "operation": "files::add",
            }
        )

        callback(
            {
                "type": "operation::start",
                "operation": "symlinks::add",
                "total": len(options["symlinks"]),
            }
        )

        for name, target in options["symlinks"].items():
            name_in_image = os.path.join(mount_point, name)
            callback(
                {
                    "type": "operation::start",
                    "operation": "symlink::add",
                    "file": name_in_image,
                    "target": target,
                }
            )
            os.symlink(target, name_in_image)
            callback(
                {
                    "type": "operation::finished",
                    "operation": "symlink::add",
                    "file": name_in_image,
                    "target": target,
                }
            )

        callback(
            {
                "type": "operation::finished",
                "operation": "symlinks::add",
            }
        )

        callback(
            {
                "type": "operation::start",
                "operation": "extensions::hide",
            }
        )

        to_hide = []
        for name in options["hide_extensions"]:
            name_in_image = os.path.join(mount_point, name)
            to_hide.append(name_in_image)

        if to_hide:
            subprocess.check_call(["/usr/bin/SetFile", "-a", "E"] + to_hide)

        to_hide = []
        for name in options["hide"]:
            name_in_image = os.path.join(mount_point, name)
            to_hide.append(name_in_image)

        if to_hide:
            subprocess.check_call(["/usr/bin/SetFile", "-a", "V"] + to_hide)

        callback(
            {
                "type": "operation::finished",
                "operation": "extensions::hide",
            }
        )

        userfn = options.get("create_hook")
        if callable(userfn):
            userfn(mount_point, options)

        callback(
            {
                "type": "operation::start",
                "operation": "dsstore::create",
            }
        )

        image_dsstore = os.path.join(mount_point, ".DS_Store")

        with DSStore.open(image_dsstore, "w+") as d:
            d["."]["vSrn"] = ("long", 1)
            d["."]["bwsp"] = bwsp
            if include_icon_view_settings:
                d["."]["icvp"] = icvp
            if include_list_view_settings:
                d["."]["lsvp"] = lsvp
            d["."]["icvl"] = icvl

            for k, v in options["icon_locations"].items():
                d[k]["Iloc"] = v

        callback(
            {
                "type": "operation::finished",
                "operation": "dsstore::create",
            }
        )

        # Delete .Trashes, if it gets created
        shutil.rmtree(os.path.join(mount_point, ".Trashes"), True)
    except Exception:
        # Always try to detach
        eject(device, force=True)
        raise

    callback(
        {
            "type": "operation::finished",
            "operation": "dmg::create",
        }
    )

    # Flush writes before attempting to detach.
    subprocess.check_call(("sync", "--file-system", mount_point))

    retry_time = 1
    for _ in range(detach_retries):
        callback(
            {
                "type": "command::start",
                "command": "diskutil::detach",
            }
        )

        ret, output = eject(device)

        callback(
            {
                "type": "command::finished",
                "command": "diskutil::detach",
                "ret": ret,
                "output": output,
            }
        )

        if not ret:
            break

        # Exponentially backoff retries
        retry_time *= 1.5
        time.sleep(retry_time)

    if ret:
        eject(device, force=True)
        raise DMGError(callback, f"Unable to detach device cleanly: {output}")

    # Shrink the output to the minimum possible size
    if options["shrink"]:
        callback(
            {
                "type": "command::start",
                "command": "diskutil::resize",
            }
        )

        ret, output = run_tool(
            [DISKUTIL, "image", "resize", "--size", "min", writableFile.name],
            plist=False,
        )

        callback(
            {
                "type": "command::finished",
                "command": "diskutil::resize",
                "ret": ret,
                "output": output,
            }
        )

        if ret:
            raise DMGError(callback, f"Unable to shrink: {output}")

    callback(
        {
            "type": "operation::start",
            "operation": "dmg::shrink",
        }
    )

    callback(
        {
            "type": "command::start",
            "command": "diskutil::convert",
        }
    )

    # diskutil can't overwrite an existing image.
    if os.path.isfile(filename) or os.path.islink(filename):
        os.remove(filename)

    ret, output = run_tool(
        [
            DISKUTIL,
            "image",
            "create",
            "from",
            "--plist",
            "--format",
            image_format,
            writableFile.name,
            filename,
        ]
    )

    callback(
        {
            "type": "command::finished",
            "command": "diskutil::convert",
            "ret": ret,
            "output": output,
        }
    )

    if ret:
        raise DMGError(callback, f"Unable to convert: {output}")

    callback(
        {
            "type": "operation::finished",
            "operation": "dmg::shrink",
        }
    )

    if options["license"]:
        callback(
            {
                "type": "operation::start",
                "command": "dmg::addlicense",
            }
        )

        licenseDict = licensing.build_license(options["license"])

        tempLicenseFile = open(os.path.join(dirname, "license.plist"), "wb")
        plistlib.dump(licenseDict, tempLicenseFile)
        tempLicenseFile.close()

        # see https://developer.apple.com/forums/thread/668084
        ret, output = run_tool(
            [
                HDIUTIL,
                "udifrez",
                "-xml",
                tempLicenseFile.name,
                "",
                "-quiet",
                filename,
            ],
            plist=False,
        )

        os.remove(tempLicenseFile.name)

        if ret:
            raise DMGError(callback, f"Unable to add license: {output}")

        callback(
            {
                "type": "operation::finished",
                "command": "dmg::addlicense",
            }
        )

    callback({"type": "build::finished"})
