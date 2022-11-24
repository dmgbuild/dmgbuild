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

If any ``-D key=value`` settings have been made on the command line,
they are visible in a dictionary named ``defines`` within the settings
file.

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

   If defined, specifies the size of the filesystem within the image.
   If this is not defined, ``dmgbuild`` will attempt to determine a
   reasonable size for the image.

   If you set this, you should set it large enough to hold the files you
   intend to copy into the image.  The syntax is the same as for the ``-size``
   argument to ``hdiutil``, i.e. you can use the suffixes 'b', 'k', 'm', 'g',
   't', 'p' and 'e' for bytes, kilobytes, megabytes, gigabytes, terabytes,
   exabytes and petabytes respectively.

Content Settings
----------------

.. py:data:: files

   A list of files (or folders) to copy into the image.  Each of these
   is copied to the root of the image; folders are copied
   recursively. e.g.::

     files = [ '/Applications/TextEdit.app' ]

   The items in this list may be a tuple consisting of the path to copy
   from and the name to copy to. e.g.::

     files = [ ('/Applications/TextEdit.app', 'Editor.app') ]

.. py:data:: symlinks

   A dictionary specifying symbolic links to create in the image.  For
   example::

     symlinks = { 'Applications': '/Applications' }

.. py:data:: hide

   A list of files or folders that should be hidden from the user.
   The names in this list are relative to the root of the disk image.
   e.g.::

     hide = [ 'Secret.data' ]

.. py:data:: hide_extensions

   A list of files or folders whose extensions should be hidden.
   The names in this list are relative to the root of the disk image.
   e.g.::

     hide_extensions = [ 'README.rst' ]

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

   The use of badge icons requires that ``dmg_build`` be installed with the
   ``badge_icons`` extra; i.e., you need to install dmg_build using::

      pip install "dmg_build[badge_icons]"

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
   builtin-arrow     A simple blue arrow image (retina enabled)
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

   The position of the window in ``((x, y), (w, h))`` format, with y
   co-ordinates running from bottom to top.  The Finder makes sure that the
   window will be on the user's display, so if you want your window at the top
   left of the display you could use ``(0, 100000)`` as the x, y
   co-ordinates.  Unfortunately it doesn't appear to be possible to position
   the window relative to the top left or relative to the centre of the user's
   screen.

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

.. py:data:: arrange_by

   If set, indicates that the Finder should arrange the icons in the
   icon view according to the specified field.  Allowable settings
   are:

   +------------------+
   | Field name       |
   +==================+
   | name             |
   +------------------+
   | date-modified    |
   +------------------+
   | date-created     |
   +------------------+
   | date-added       |
   +------------------+
   | date-last-opened |
   +------------------+
   | size             |
   +------------------+
   | kind             |
   +------------------+
   | label            |
   +------------------+

   Any other value disables automatic icon arrangement (which is the
   default, since the main use-case for ``dmgbuild`` is building
   application distribution images, where icon positioning is an
   important part of the design).

.. py:data:: grid_offset

   Specifies the grid offset for automatic arrangement.

.. py:data:: grid_spacing

   Specifies the grid spacing for automatic arrangement.

   .. warning:: As of Mac OS X Yosemite (v10.10), Finder checks to make sure
                that grid_spacing is less than 100.  If it is over that
                value, it will reject the saved settings.

.. py:data:: scroll_position

   An (x, y) tuple specifying the scroll position; this is only
   relevant if you position icons outside of the window area.

.. py:data:: label_pos

   Specifies the position of the icons' labels.  Choose 'bottom' or
   'right' (defaults to 'bottom').

.. py:data:: text_size

   Specifies the point size of the label text.  Default is 16pt.

.. py:data:: icon_size

   Specifies the size of icon to use.  Default is 128pt.

.. py:data:: icon_locations
   :noindex:

   If :data:`arrange_by` is not set, a dictionary mapping the names of
   items in the root of the volume to an (x, y) tuple specifying their
   location in points.

List View Settings
------------------

In list view, the following columns are available:

   +------------------+
   | Field name       |
   +==================+
   | name             |
   +------------------+
   | date-modified    |
   +------------------+
   | date-created     |
   +------------------+
   | date-added       |
   +------------------+
   | date-last-opened |
   +------------------+
   | size             |
   +------------------+
   | kind             |
   +------------------+
   | label            |
   +------------------+
   | version          |
   +------------------+
   | comments         |
   +------------------+

.. py:data:: list_icon_size

   Sets the size of the icon in list view.  Default is 16pt.

.. py:data:: list_text_size

   Sets the size of the text in list view.  Default is 12pt.

.. py:data:: list_scroll_position

   Specifies the scroll position, assuming there are enough items to
   make the view scroll.

.. py:data:: list_sort_by

   Specifies which column the Finder should sort the display by.
   Defaults to 'name'.

.. py:data:: list_use_relative_dates

   If ``True``, formats dates using words like "Today" or "Yesterday"
   where possible; otherwise they will be displayed as a full date.
   Defaults to ``True``.

.. py:data:: list_calculate_all_sizes

   If ``True``, forces the Finder to compute all of the item sizes;
   normally this is set to ``False`` because it can be expensive
   calculating the sizes of deeply nested folders.  Defaults to
   ``False``.

.. py:data:: list_columns

   A list or tuple of strings containing the names of columns, in the
   order you want them to appear.

.. py:data:: list_column_widths

   A dictionary specifying the width, in points, for each of the
   columns.  There are default widths for every column, so you may not
   need to set this variable in practice.

.. py:data:: list_column_sort_directions

   A dictionary specifying the sort direction (either 'ascending', or
   'descending') for each column.  Again, there are individual
   defaults for each column, so you may not need to touch this unless
   you wish to override the default behaviour.

License Settings
----------------

``dmgbuild`` can attach license text to your disk image; this will be
displayed automatically when the user tries to open your disk image.

Note that license text is either RTF, or it must be encoded in the legacy Mac
encoding matching its language; ``dmgbuild`` will *try* to do this, but the
built-in set of codecs in Python doesn't cover all the Mac encodings, so in
some cases you will need to encode the data and use a byte string.

.. py:data:: license

   If defined, a dictionary specifying the details of the license to display.
   It has the following keys:

   +------------------+----------+-------------------------------------------+
   | Key              | Optional | Value                                     |
   +==================+==========+===========================================+
   | default-language | No       | The name of the default language to       |
   |                  |          | display if there is no license matching   |
   |                  |          | the system language.                      |
   +------------------+----------+-------------------------------------------+
   | licenses         | No       | A dictionary mapping language names to    |
   |                  |          | license text (either RTF data or plain    |
   |                  |          | text) or paths to files containing the    |
   |                  |          | license text.                             |
   +------------------+----------+-------------------------------------------+
   | buttons          | Yes      | A dictionary mapping language names to    |
   |                  |          | a sequence of user interface strings.     |
   +------------------+----------+-------------------------------------------+

   Recognized languages are:

     af_ZA, ar, be_BY, bg_BG, bn, bo, br, ca_ES, cs_CZ, cy, da_DK, de_AT, de_CH,
     de_DE, dz_BT, el_CY, el_GR, en_AU, en_CA, en_GB, en_IE, en_SG, en_US, eo,
     es_419, es_ES, et_EE, fa_IR, fi_FI, fo_FO, fr_001, fr_BE, fr_CA, fr_CH,
     fr_FR, ga-Latg_IE, ga_IE, gd, grc, gu_IN, gv, he_IL, hi_IN, hr_HR, hu_HU,
     hy_AM, is_IS, it_CH, it_IT, iu_CA, ja_JP, ka_GE, kl, ko_KR, lt_LT, lv_LV,
     mk_MK, mr_IN, mt_MT, nb_NO, ne_NP, nl_BE, nl_NL, nn_NO, pa, pl_PL, pt_BR,
     pt_PT, ro_RO, ru_RU, se, sk_SK, sl_SI, sr_RS, sv_SE, th_TH, to_TO, tr_TR,
     uk_UA, ur_IN, ur_PK, uz_UZ, vi_VN, zh_CN, zh_TW

   The user interface strings are as follows:

   +-------+-----------------------+-----------------------------------------+
   | Index | Comment               | Typical English text                    |
   +=======+=======================+=========================================+
   |   0   | Language name         | English                                 |
   +-------+-----------------------+-----------------------------------------+
   |   1   | Agree button label    | Agree                                   |
   +-------+-----------------------+-----------------------------------------+
   |   2   | Disagree button label | Disagree                                |
   +-------+-----------------------+-----------------------------------------+
   |   3   | Print button label    | Print                                   |
   +-------+-----------------------+-----------------------------------------+
   |   4   | Save button label     | Save                                    |
   +-------+-----------------------+-----------------------------------------+
   |   5   | Instruction text      | If you agree with the terms of this     |
   |       |                       | license, press "Agree" to install the   |
   |       |                       | software.  If you do not agree, press   |
   |       |                       | "Disagree".                             |
   +-------+-----------------------+-----------------------------------------+

   There are built-in user interface strings for the following languages:

     English (en_US), German (de_DE), Spanish (es_ES), French (fr_FR),
     Italian (it_IT), Japanese (ja_JP), Dutch (nl_NL), Swedish (sv_SE),
     Brazilian Portuguese (pt_BR), Simplified Chinese (zh_CN),
     Traditional Chinese (zh_TW), Danish (da_DK), Finnish (fi_FI),
     Korean (ko_KR), Norwegian (nb_NO)

   For other languages, if you don't specify a suitable set, ``dmgbuild`` will
   use the English defaults instead.

   ``dmgbuild`` will auto-detect RTF data by looking for the string ``{\rtf1``
   at the start of the data.  If it does not find this string, it will assume
   that you have supplied plain text.
