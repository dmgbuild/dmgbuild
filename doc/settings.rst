Settings
========

``dmgbuild`` accepts, as one of its arguments, a settings file.  This
is in fact a Python script, which means anything you can do in Python
code, you can do in your settings file.  This makes it easy for you to
customise the behaviour of ``dmgbuild``.

Each of the available settings is documented below; all of them are
optional; the ``dmgbuild`` program has defaults for those that matter.
The default values *are* visible from within your settings file, if
you want to examine or alter them rather than replacing them
completely.

Disk Image Settings
-------------------

.. py:data:: filename

   If defined, overrides the output filename specified on the command
   line.  The command line value is the default value.

.. py:data:: volume_name

   If defined, overrides the volume name specified on the command
   line, which is the default value.

.. py:data:: format

   Specifies the format code for the final output disk image.  Must be
   one of the types supported by ``hdiutil`` on the build system;
   currently the list includes

   ====  =========================
   Code  Meaning
   ====  =========================
   UDRO  Read-only
   UDCO  Compressed (ADC)
   UDZO  Compressed (gzip)
   UDBZ  Compressed (bzip2)
   UFBI  Entire device
   IPOD  iPod image
   UDxx  UDIF stub
   UDSB  Sparse bundle
   UDSP  Sparse
   UDRW  Read/write
   UDTO  DVD/CD master
   DC42  Disk Copy 4.2
   RdWr  NDIF read/write
   Rdxx  NDIF read-only
   ROCo  NDIF Compressed
   Rken  NDIF Compressed (KenCode)
   ====  =========================

   For disk images you intend to distribute over the Internet, you
   should probably stick to 'UDZO' and 'UDBZ'.

.. py:data:: size

   Specifies the size of the filesystem within the image.  You should
   set this large enough to hold the files you intend to copy into the
   image.  The syntax is the same as for the ``-size`` argument to
   ``hdiutil``, i.e. you can use the suffixes 'b', 'k', 'm', 'g', 't',
   'p' and 'e' for bytes, kilobytes, megabytes, gigabytes, terabytes,
   exabytes and petabytes respectively.

   Defaults to '100M'

Content Settings
----------------

.. py:data:: files

   A list of files (or folders) to copy into the image.  Each of these
   is copied to the root of the image; folders are copied
   recursively. e.g.::

     files = [ '/Applications/TextEdit.app' ]

.. py:data:: symlinks

   A dictionary specifying symbolic links to create in the image.  For
   example::

     symlinks = { 'Applications': '/Applications' }

.. py:data:: icon

   Specifies the path of an icon file to copy to the volume.  You can
   either specify this, or as an alternative you can use the
   :data:`badge_icon` setting.

.. py:data:: badge_icon

   As an alternative to the above, if you set `badge_icon` to the path
   of an icon file or image, it will be used to badge the system's
   standard external disk icon.  This is a convenient way to construct
   a suitable icon from your application's icon, e.g.::

     badge_icon = '/Applications/TextEdit.app/Contents/Resources/Edit.icns'

.. py:data:: icon_locations

   A dictionary specifying the co-ordinates of items in the root
   directory of the disk image, where the keys are filenames and the
   values are (x, y) tuples. e.g.::

     icon_locations = {
         'TextEdit.app': (100, 100),
         'Applications': (300, 100)
     }

Window Settings
---------------

.. py:data:: background

   A string containing any of the following:

   ================  ================================================
   Example           Meaning
   ================  ================================================
   #3344ff           Web-style RGB color
   #34f              Web-style RGB color, short form (#34f = #3344ff)
   rgb(1,0,0)        RGB color, each value is between 0 and 1
   hsl(120,1,.5)     HSL (Hue Saturation Lightness) color
   hwb(300,0,0)      HWB (Hue Whiteness Blackness) color
   cmyk(0,1,0,0)     CMYK (Cyan Magenta Yellow Black) color
   goldenrod         X11/SVG named color
   /foo/bar/baz.png  The path to an image file
   ================  ================================================

   The hue component in ``hsl()`` and ``hwb()`` may include a unit; it
   defaults to degrees ('deg'), but also supports radians ('rad') and
   gradians ('grad' or 'gon').

   Other color components may be expressed either in the range 0 to 1,
   or as percentages (e.g. 60% is equivalent to 0.6).

   For no background, specify ``None`` instead of a string value.

.. py:data:: show_status_bar
             show_tab_view
             show_toolbar
             show_pathbar
             show_sidebar

   Each of the above controls the display of one of the standard
   window elements.  All of them default to ``False``.

.. py:data:: sidebar_width

   The width of the Finder sidebar.

.. py:data:: window_rect

   The position of the window in ``((x, y), (w, h))`` format.

.. py:data:: default_view

   The default view for the window; should be a string containing one of:

   +-------------+
   | View name   |
   +=============+
   | icon-view   |
   +-------------+
   | list-view   |
   +-------------+
   | column-view |
   +-------------+
   | coverflow   | 
   +-------------+

.. py:data:: show_icon_preview

   Whether or not to show icon previews for the contents of the disk
   image (defaults to ``False``)

.. py:data:: include_icon_view_settings
             include_list_view_settings
   
   Set these to ``True`` to force inclusion of the icon/list view
   settings respectively.  By default, ``dmgbuild`` will only include
   settings for the default view type.

Icon View Settings
------------------


   
