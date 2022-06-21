Usage
=====

Typical usage looks like this::

  dmgbuild -s settings.py "Volume Name" output.dmg

The (optional) ``settings.py`` file specifies the attributes that
control the appearance of the disk image.  The other arguments give
the volume name and the name of the output file respectively.

``dmgbuild`` also accepts arguments of the form ``-D key=value``;
these can be used from within the settings file, for instance so that
you can write a single settings file for multiple disk images, or so
that you can easily alter settings at build time.
