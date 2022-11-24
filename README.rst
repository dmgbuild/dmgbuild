========
dmgbuild
========

.. image:: https://img.shields.io/pypi/pyversions/dmgbuild.svg
   :target: https://pypi.python.org/pypi/dmgbuild
   :alt: Python Versions

.. image:: https://img.shields.io/pypi/v/dmgbuild.svg
   :target: https://pypi.python.org/pypi/dmgbuild
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/status/dmgbuild.svg
   :target: https://pypi.python.org/pypi/dmgbuild
   :alt: Maturity

.. image:: https://img.shields.io/pypi/l/dmgbuild.svg
   :target: https://github.com/dmgbuild/dmgbuild/blob/main/LICENSE
   :alt: MIT License

.. image:: https://github.com/dmgbuild/dmgbuild/workflows/CI/badge.svg?branch=main
   :target: https://github.com/dmgbuild/dmgbuild/actions
   :alt: Build Status

.. image:: https://readthedocs.org/projects/dmgbuild/badge/?version=latest
   :target: http://dmgbuild.readthedocs.io/en/latest/?badge=latest
   :alt: Docs Build Status

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

See the documentation_ for more information.

.. _documentation: http://dmgbuild.readthedocs.io
