# dmgbuild

[![Python Versions](https://img.shields.io/pypi/pyversions/dmgbuild.svg)](https://pypi.python.org/pypi/dmgbuild) [![PyPI Version](https://img.shields.io/pypi/v/dmgbuild.svg)](https://pypi.python.org/pypi/dmgbuild) [![Maturity](https://img.shields.io/pypi/status/dmgbuild.svg)](https://pypi.python.org/pypi/dmgbuild) [![MIT License](https://img.shields.io/pypi/l/dmgbuild.svg)](https://github.com/dmgbuild/dmgbuild/blob/master/LICENSE) [![Build status](https://github.com/dmgbuild/dmgbuild/workflows/CI/badge.svg?branch=main)](https://github.com/dmgbuild/dmgbuild/actions)

`dmgbuild` is a command line tool to create macOS disk images (aka `.dmg` files).  While it is possible to create disk images easily enough from the command line using the `hdiutil` program that ships with macOS, there is no easy way to configure the appearance of the resulting disk image when the user opens it.

`dmgbuild` allows for full customization of the resulting disk image, without relying on Finder, and without using deprecated APIs (like the Alias Manager functions).

`dmgbuild` is a wrapper around macOS specific tools, so it can't be used on Windows or Linux.

See the [documentation](https://dmgbuild.readthedocs.io) for more information.
