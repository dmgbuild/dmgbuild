.. dmgbuild documentation master file, created by
   sphinx-quickstart on Sat Feb 15 10:06:11 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dmgbuild - A command line tool to build ``.dmg`` files
======================================================

This document refers to version |release|

What is this?
=============

``dmgbuild`` is a command line tool to create macOS disk images
(aka ``.dmg`` files).  While it is possible to create disk images
easily enough from the command line using the ``hdiutil`` program that
ships with macOS, there is no easy way to configure the appearance
of the resulting disk image when the user opens it.  Some people have
used AppleScript to automate Finder to adjust the appearance, but
since Finder saves its ``.DS_Store`` files asynchronously, it is hard
to guarantee that the changes will actually be saved when you want
them to be.  It also means that you need a GUI session, with Finder
running, in order to build your disk image.

``dmgbuild`` does not rely on Finder; nor does it rely on deprecated
APIs (like the Alias Manager functions).  Instead, it uses the
``ds_store`` and ``mac_alias`` Python modules, which know how to
construct the relevant data in Python code.

Contents:

.. toctree::
   :maxdepth: 2

   usage
   settings
   example

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
