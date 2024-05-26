========
dmgbuild
========

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/dmgbuild.svg
   :target: https://pypi.python.org/pypi/dmgbuild
   :alt: Python Versions

.. |version| image:: https://img.shields.io/pypi/v/dmgbuild.svg
   :target: https://pypi.python.org/pypi/dmgbuild
   :alt: PyPI Version

.. |maturity| image:: https://img.shields.io/pypi/status/dmgbuild.svg
   :target: https://pypi.python.org/pypi/dmgbuild
   :alt: Maturity

.. |license| image:: https://img.shields.io/pypi/l/dmgbuild.svg
   :target: https://github.com/dmgbuild/dmgbuild/blob/main/LICENSE
   :alt: MIT License

.. |ci| image:: https://github.com/dmgbuild/dmgbuild/workflows/CI/badge.svg?branch=main
   :target: https://github.com/dmgbuild/dmgbuild/actions
   :alt: Build Status

|pyversions| |version| |maturity| |license| |ci|

What is this?
-------------

``dmgbuild`` is a command line tool to create macOS disk images (aka
``.dmg`` files).  While it is possible to create disk images easily enough
from the command line using the ``hdiutil`` program that ships with macOS,
there is no easy way to configure the appearance of the resulting disk image
when the user opens it.

``dmgbuild`` allows for full customization of the resulting disk image,
without relying on Finder, and without using deprecated APIs (like the
Alias Manager functions).

``dmgbuild`` is a wrapper around macOS specific tools, so it can't be used on
Windows or Linux.

See the documentation_ for more information.

.. _documentation: http://dmgbuild.readthedocs.io
