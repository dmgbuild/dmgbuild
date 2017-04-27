``dmgbuild`` is a command line tool to create Mac OS X disk images (aka
``.dmg`` files).  While it is possible to create disk images easily enough
from the command line using the ``hdiutil`` program that ships with Mac OS X,
there is no easy way to configure the appearance of the resulting disk image
when the user opens it.

``dmgbuild`` allows for full customization of the resulting disk image,
without relying on Finder, and without using deprecated APIs (like the
Alias Manager functions).

See the documentation_ for more information.

.. _documentation: http://dmgbuild.rtfd.org
