#! /usr/bin/env python3
import argparse

from .core import build_dmg


def main():
    parser = argparse.ArgumentParser(description="Construct a disk image file.")
    parser.add_argument(
        "volume_name",
        metavar="volume-name",
        help="The name to give to the volume (this will appear in the title bar when the user mounts the disk image).",
    )
    parser.add_argument(
        "filename",
        metavar="output.dmg",
        help="The filename of the disk image to create.",
    )
    parser.add_argument("-s", "--settings", help="The path of the settings file.")
    parser.add_argument(
        "-D",
        dest="defines",
        action="append",
        default=[],
        help="Define a value for the settings file (e.g. -Dfoo=bar).",
    )
    parser.add_argument(
        "--no-hidpi",
        dest="lookForHiDPI",
        action="store_false",
        default=True,
        help="Do not search for HiDPI versions of the background image (if specified)",
    )

    args = parser.parse_args()

    defines = {}
    for d in args.defines:
        k, v = d.split("=", 1)
        k = k.strip()
        v = v.strip()
        if (v.startswith("'") and v.endswith("'")) or (
            v.startswith('"') and v.endswith('"')
        ):
            v = v[1:-1]
        defines[k] = v

    build_dmg(
        args.filename,
        args.volume_name,
        args.settings,
        defines=defines,
        lookForHiDPI=args.lookForHiDPI,
    )


if __name__ == "__main__":
    main()
