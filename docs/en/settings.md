# Settings

DMGBuild accepts, as one of its arguments, a settings file. This is in fact a Python script, which means anything you can do in Python code, you can do in your settings file. This makes it easy for you to customize the behavior of DMGBuild.

Each of the available settings is documented below; all of them are optional; the DMGBuild program has defaults for those that matter. The default values *are* visible from within your settings file, if you want to examine or alter them rather than replacing them completely.

If any `-D key=value` settings have been made on the command line, they are visible in a dictionary named `defines` within the settings file.

## Disk Image Settings

### `filename` { #filename }

If defined, overrides the output filename specified on the command line. The command line value is the default value.

### `volume_name` { #volume_name }

If defined, overrides the volume name specified on the command line, which is the default value.

### `format` { #format }

Specifies the format code for the final output disk image. Must be one of the formats supported by `diskutil image create from`:

| Code | Meaning                         |
|------|---------------------------------|
| ULFO | Compressed (lzfse); the default |
| ULMO | Compressed (lzma)               |
| UDZO | Compressed (zlib)               |
| UDRO | Read-only, uncompressed         |
| UDSB | Sparse bundle                   |
| RAW  | Raw, uncompressed               |
| ASIF | Apple Sparse Image Format       |

For disk images you intend to distribute over the Internet, you should use one of the compressed formats: 'ULFO', 'ULMO' or 'UDZO'.

### `filesystem` { #filesystem }

Specifies the file system for the output disk image. Must be either 'HFS+' (the default) or 'APFS'.

### `size` { #size }

If defined, specifies the size of the file system within the image. If this is not defined, DMGBuild will attempt to determine a reasonable size for the image.

If you set this, you should set it large enough to hold the files you intend to copy into the image. The value is passed to the `--size` argument of`diskutil image create blank`: a number without a suffix is a size in bytes; the suffixes 'k', 'm', 'g' and 't' are decimal units (powers of 1000); and the suffixes 'KiB', 'MiB', 'GiB' and 'TiB' are binary units (powers of 1024).

### `shrink` { #shrink }

If set to `False`, DMGBuild will not shrink the file system to the minimum size after copying files. This is useful when you want to preserve the explicit `size` you specified for the mounted volume. Defaults to `True`.

## Content Settings

### `files` { #files }

A list of files (or folders) to copy into the image. Each of these is copied to the root of the image; folders are copied recursively. e.g.:

```python
files = ["/Applications/TextEdit.app"]
```

The items in this list may be a tuple consisting of the path to copy from and the name to copy to. e.g.:

```python
files = [("/Applications/TextEdit.app", "Editor.app")]
```

### `symlinks` { #symlinks }

A dictionary specifying symbolic links to create in the image. For example:

```python
symlinks = {"Applications": "/Applications"}
```

### `hide` { #hide }

A list of files or folders that should be hidden from the user. The names in this list are relative to the root of the disk image. e.g.:

```python
hide = ["Secret.data"]
```

### `hide_extensions` { #hide_extensions }

A list of files or folders whose extensions should be hidden. The names in this list are relative to the root of the disk image. e.g.:

```python
hide_extensions = ["README.rst"]
```

### `icon` { #icon }

Specifies the path of an icon file to copy to the volume. You can either specify this, or as an alternative you can use the [`badge_icon`](#badge_icon) setting.

### `badge_icon` { #badge_icon }

As an alternative to the above, if you set `badge_icon` to the path of an icon file or image, it will be used to badge the system's standard external disk icon. This is a convenient way to construct a suitable icon from your application's icon, e.g.:

```python
badge_icon = "/Applications/TextEdit.app/Contents/Resources/Edit.icns"
```

The use of badge icons requires that DMGBuild be installed with the `badge_icons` extra; i.e., you need to install DMGBuild using:

```console
pip install "dmgbuild[badge_icons]"
```

### `icon_locations` { #icon_locations }

A dictionary specifying the co-ordinates of items in the root directory of the disk image, where the keys are filenames and the values are (x, y) tuples. e.g.:

```python
icon_locations = {"TextEdit.app": (100, 100), "Applications": (300, 100)}
```

## Window Settings

### `background` { #background }

A string containing any of the following:

| Example            | Meaning                                              |
|--------------------|------------------------------------------------------|
| `#3344ff`          | Web-style RGB color                                  |
| `#34f`             | Web-style RGB color, short form (`#34f` = `#3344ff`) |
| `rgb(1,0,0)`       | RGB color, each value is between 0 and 1             |
| `hsl(120,1,.5)`    | HSL (Hue Saturation Lightness) color                 |
| `hwb(300,0,0)`     | HWB (Hue Whiteness Blackness) color                  |
| `cmyk(0,1,0,0)`    | CMYK (Cyan Magenta Yellow Black) color               |
| `goldenrod`        | X11/SVG named color                                  |
| `builtin-arrow`    | A simple blue arrow image (retina enabled)           |
| `/foo/bar/baz.png` | The path to an image file                            |

The hue component in `hsl()` and `hwb()` may include a unit; it defaults to degrees ('deg'), but also supports radians ('rad') and gradians ('grad' or 'gon').

Other color components may be expressed either in the range 0 to 1, or as percentages (e.g. 60% is equivalent to 0.6).

For no background, specify `None` instead of a string value.

### `show_status_bar` { #show_status_bar }

### `show_tab_view` { #show_tab_view }

### `show_toolbar` { #show_toolbar }

### `show_pathbar` { #show_pathbar }

### `show_sidebar` { #show_sidebar }

Each of the above controls the display of one of the standard window elements. All of them default to `False`.

### `sidebar_width` { #sidebar_width }

The width of the Finder sidebar.

### `window_rect` { #window_rect }

The position of the window in `((x, y), (w, h))` format, with y co-ordinates running from bottom to top. The Finder makes sure that the window will be on the user's display, so if you want your window at the top left of the display you could use `(0, 100000)` as the x, y co-ordinates. Unfortunately it doesn't appear to be possible to position the window relative to the top left or relative to the center of the user's screen.

### `default_view` { #default_view }

The default view for the window; should be a string containing one of:

| View name     |
|---------------|
| `icon-view`   |
| `list-view`   |
| `column-view` |
| `coverflow`   |

### `show_icon_preview` { #show_icon_preview }

Whether or not to show icon previews for the contents of the disk image (defaults to `False`)

### `include_icon_view_settings` { #include_icon_view_settings }

### `include_list_view_settings` { #include_list_view_settings }

Set these to `True` to force inclusion of the icon/list view settings respectively. By default, DMGBuild will only include settings for the default view type.

## Icon View Settings

### `arrange_by` { #arrange_by }

If set, indicates that the Finder should arrange the icons in the icon view according to the specified field. Allowable settings are:

| Field name         |
|--------------------|
| `name`             |
| `date-modified`    |
| `date-created`     |
| `date-added`       |
| `date-last-opened` |
| `size`             |
| `kind`             |
| `label`            |

Any other value disables automatic icon arrangement (which is the default, since the main use-case for DMGBuild is building application distribution images, where icon positioning is an important part of the design).

### `grid_offset` { #grid_offset }

Specifies the grid offset for automatic arrangement.

### `grid_spacing` { #grid_spacing }

Specifies the grid spacing for automatic arrangement.

!!! warning

    As of Mac OS X Yosemite (v10.10), Finder checks to make sure that `grid_spacing` is less than 100. If it is over that value, it will reject the saved settings.

### `scroll_position` { #scroll_position }

An (x, y) tuple specifying the scroll position; this is only relevant if you position icons outside of the window area.

### `label_pos` { #label_pos }

Specifies the position of the icons' labels. Choose 'bottom' or 'right' (defaults to 'bottom').

### `text_size` { #text_size }

Specifies the point size of the label text. Default is 16pt.

### `icon_size` { #icon_size }

Specifies the size of icon to use. Default is 128pt.

### `icon_locations`

If [`arrange_by`](#arrange_by) is not set, a dictionary mapping the names of items in the root of the volume to an (x, y) tuple specifying their location in points. See also [`icon_locations`](#icon_locations) under [Content Settings](#content-settings).

## List View Settings

In list view, the following columns are available:

| Field name         |
|--------------------|
| `name`             |
| `date-modified`    |
| `date-created`     |
| `date-added`       |
| `date-last-opened` |
| `size`             |
| `kind`             |
| `label`            |
| `version`          |
| `comments`         |

### `list_icon_size` { #list_icon_size }

Sets the size of the icon in list view. Default is 16pt.

### `list_text_size` { #list_text_size }

Sets the size of the text in list view. Default is 12pt.

### `list_scroll_position` { #list_scroll_position }

Specifies the scroll position, assuming there are enough items to make the view scroll.

### `list_sort_by` { #list_sort_by }

Specifies which column the Finder should sort the display by. Defaults to 'name'.

### `list_use_relative_dates` { #list_use_relative_dates }

If `True`, formats dates using words like "Today" or "Yesterday" where possible; otherwise they will be displayed as a full date. Defaults to `True`.

### `list_calculate_all_sizes` { #list_calculate_all_sizes }

If `True`, forces the Finder to compute all of the item sizes; normally this is set to `False` because it can be expensive calculating the sizes of deeply nested folders. Defaults to `False`.

### `list_columns` { #list_columns }

A list or tuple of strings containing the names of columns, in the order you want them to appear.

### `list_column_widths` { #list_column_widths }

A dictionary specifying the width, in points, for each of the columns. There are default widths for every column, so you may not need to set this variable in practice.

### `list_column_sort_directions` { #list_column_sort_directions }

A dictionary specifying the sort direction (either 'ascending', or 'descending') for each column. Again, there are individual defaults for each column, so you may not need to touch this unless you wish to override the default behavior.

## License Settings

!!! warning

    The `license` setting will be removed in a future release of DMGBuild.

    Apple has deprecated the tool used to embed license agreements in disk images, and does not appear to be providing an alternate method for embedding licenses. If you need the user to acknowledge a license, consider using a PKG installer instead of a DMG.

DMGBuild can attach license text to your disk image; this will be displayed automatically when the user tries to open your disk image.

Note that license text is either RTF, or it must be encoded in the legacy macOS encoding matching its language; DMGBuild will *try* to do this, but the built-in set of codecs in Python doesn't cover all the macOS encodings, so in some cases you will need to encode the data and use a byte string.

### `license` { #license }

If defined, a dictionary specifying the details of the license to display. It has the following keys:

| Key                | Optional | Value                                                                                                                       |
|--------------------|----------|-----------------------------------------------------------------------------------------------------------------------------|
| `default-language` | No       | The name of the default language to display if there is no license matching the system language.                            |
| `licenses`         | No       | A dictionary mapping language names to license text (either RTF data or plain text) or paths to files containing the license text. |
| `buttons`          | Yes      | A dictionary mapping language names to a sequence of user interface strings.                                                |

The user interface strings are as follows:

| Index | Comment               | Typical English text                                                                                                 |
|:-----:|-----------------------|----------------------------------------------------------------------------------------------------------------------|
| 0     | Language name         | English                                                                                                              |
| 1     | Agree button label    | Agree                                                                                                                |
| 2     | Disagree button label | Disagree                                                                                                             |
| 3     | Print button label    | Print                                                                                                                |
| 4     | Save button label     | Save                                                                                                                 |
| 5     | Instruction text      | If you agree with the terms of this license, press "Agree" to install the software.  If you do not agree, press "Disagree". |

There are built-in user interface strings for the following languages:

- Danish (`da_DK`)
- German (`de_DE`, `de_AT`, `de_CH`)
- English (`en_US`, `en_AU`, `en_IE`, `en_GB`, `en_SG`)
- Spanish (`es_ES`)
- Finnish (`fi_FI`)
- French (`fr_FR`, `fr_BE`, `fr_CA`, `fr_CH`)
- Italian (`it_IT`)
- Japanese (`ja_JP`)
- Korean (`ko_KR`)
- Norwegian (`nb_NO`)
- Dutch (`nl_NL`, `nl_BE`)
- Portuguese (`pt_BR`, `pt_PT`)
- Russian (`ru_RU`)
- Swedish (`sv_SE`)
- Simplified Chinese (`zh_CN`)
- Traditional Chinese (`zh_TW`)

For other languages, if you don't specify a suitable set, DMGBuild will use the English defaults instead.

DMGBuild will auto-detect RTF data by looking for the string `{\rtf1` at the start of the data. If it does not find this string, it will assume that you have supplied plain text.
