# Release History

<!-- towncrier release notes start -->

## 1.6.7 (2026-01-16)

### Bugfixes

* Background images are now displayed correctly on macOS 26.2 (Tahoe). ([#273](https://github.com/dmgbuild/dmgbuild/issues/273))

### Misc

* [#272](https://github.com/dmgbuild/dmgbuild/issues/272)

## 1.6.6 (2025-12-04)

### Features

* Support for Python 3.15 was added. ([#260](https://github.com/dmgbuild/dmgbuild/issues/260))

### Bugfixes

* The `badge_icons` installation extra was restored. ([#214](https://github.com/dmgbuild/dmgbuild/issues/214))
* The `ret` and `output` keys passed to the callback at the end of `hdiutil::detach` no longer contain a trailing colon. ([#259](https://github.com/dmgbuild/dmgbuild/issues/259))

### Backward Incompatible Changes

* Support for Python 3.9 was dropped. ([#260](https://github.com/dmgbuild/dmgbuild/issues/260))

### Misc

* [#256](https://github.com/dmgbuild/dmgbuild/issues/256)

## 1.6.5 (2025-03-21)

### Bugfixes

* Output from `hdiutil` that is parsed as a plist no longer includes content written to stderr. ([#197](https://github.com/dmgbuild/dmgbuild/issues/197))

### Misc

* [#199](https://github.com/dmgbuild/dmgbuild/issues/199)

## 1.6.4 (2025-01-10)

### Bugfixes

* Retries when detaching the disk image now use exponential backoff, as intended.

## 1.6.3 (2025-01-10)

### Features

* Detaching the disk image is now more resilient, and errors from `hdiutil` are captured and reported. ([#180](https://github.com/dmgbuild/dmgbuild/issues/180))
* Support for Python 3.14 was added. ([#180](https://github.com/dmgbuild/dmgbuild/issues/180))

### Bugfixes

* The default window position and size are now used correctly when they aren't specified in a JSON configuration file. ([#142](https://github.com/dmgbuild/dmgbuild/issues/142))

### Backward Incompatible Changes

* Support for Python 3.8 was dropped. ([#160](https://github.com/dmgbuild/dmgbuild/issues/160))

### Misc

* [#132](https://github.com/dmgbuild/dmgbuild/issues/132), [#133](https://github.com/dmgbuild/dmgbuild/issues/133)

## 1.6.2 (2024-08-04)

### Features

* A `--detach-retries` option was added to the command line interface. ([#128](https://github.com/dmgbuild/dmgbuild/issues/128))
* The `dmgbuild` script now explicitly uses `python3` as its interpreter. ([#67](https://github.com/dmgbuild/dmgbuild/issues/67))
* Support for Python 3.13 was added. ([#68](https://github.com/dmgbuild/dmgbuild/issues/68))

### Bugfixes

* The length of license buttons is no longer hard-coded. ([#61](https://github.com/dmgbuild/dmgbuild/issues/61))
* License agreement resources are now generated dynamically, rather than being hard-coded. This corrects the handling of a number of languages, including Russian and Italian. ([#56](https://github.com/dmgbuild/dmgbuild/issues/56))
* The default background `.tiff` files are now included in the distribution package.

### Backward Incompatible Changes

* Support for Python 3.7 was dropped. ([#68](https://github.com/dmgbuild/dmgbuild/issues/68))

### Misc

* [#56](https://github.com/dmgbuild/dmgbuild/issues/56), [#63](https://github.com/dmgbuild/dmgbuild/issues/63), [#68](https://github.com/dmgbuild/dmgbuild/issues/68), [#75](https://github.com/dmgbuild/dmgbuild/issues/75), [#108](https://github.com/dmgbuild/dmgbuild/issues/108)

## 1.6.1 (2023-04-20)

### Features

* Disk images can now be created using the APFS filesystem, and with ULMO (LZMA) compression. ([#53](https://github.com/dmgbuild/dmgbuild/issues/53))

### Bugfixes

* dmgbuild no longer depends on the deprecated `pkg_resources` module from setuptools. ([#58](https://github.com/dmgbuild/dmgbuild/issues/58))

### Misc

* [#54](https://github.com/dmgbuild/dmgbuild/issues/54)

## 1.6.0 (2022-11-24)

### Features

* Licenses are now added to disk images using `hdiutil udifrez`. ([#43](https://github.com/dmgbuild/dmgbuild/issues/43))
* A `badge_icons` installation extra was added to install the dependencies needed to badge icons. ([#50](https://github.com/dmgbuild/dmgbuild/issues/50))

### Bugfixes

* The English license buttons were corrected, and a default set of buttons is now used if no buttons are defined for a language. ([#43](https://github.com/dmgbuild/dmgbuild/issues/43))

### Backward Incompatible Changes

* Support for Python 2, and Python 3 versions prior to 3.7 was dropped. ([#47](https://github.com/dmgbuild/dmgbuild/issues/47))

### Misc

* [#38](https://github.com/dmgbuild/dmgbuild/issues/38), [#47](https://github.com/dmgbuild/dmgbuild/issues/47), [#48](https://github.com/dmgbuild/dmgbuild/issues/48), [#49](https://github.com/dmgbuild/dmgbuild/issues/49), [#51](https://github.com/dmgbuild/dmgbuild/issues/51)

## 1.5.2 (2021-06-01)

### Bugfixes

* The `dmgbuild` console script entry point, and the top-level package exports, were corrected. ([#41](https://github.com/dmgbuild/dmgbuild/issues/41))

## 1.5.1 (2021-05-31)

### Bugfixes

* A problem in the command line interface introduced in 1.5.0 was corrected.

## 1.5.0 (2021-05-31)

### Features

* A `callback` argument was added to `build_dmg()`, allowing progress of the build to be monitored. ([#30](https://github.com/dmgbuild/dmgbuild/issues/30))
* dmgbuild can now be invoked as `python -m dmgbuild`; the `dmgbuild` command is now installed as a console script entry point. ([#28](https://github.com/dmgbuild/dmgbuild/issues/28))

### Bugfixes

* Pending writes are now flushed before detaching the disk image, avoiding slowdowns when detaching. ([#39](https://github.com/dmgbuild/dmgbuild/issues/39))

## 1.4.2 (2020-10-16)

### Bugfixes

* `/usr/bin/SetFile` is no longer invoked when there are no files to hide, avoiding spurious error messages. ([#25](https://github.com/dmgbuild/dmgbuild/issues/25))

## 1.4.1 (2020-10-15)

### Bugfixes

* `plistlib` is now used in preference to `biplist` on Python 3.4+, correcting a compatibility problem with Python 3.9.

## 1.4.0 (2020-10-11)

### Features

* `hide` and `hide_extensions` settings were added, allowing files, or their extensions, to be hidden. ([#9](https://github.com/dmgbuild/dmgbuild/issues/9))
* The number of attempts made to detach the disk image can now be configured with the `detach_retries` argument. ([#22](https://github.com/dmgbuild/dmgbuild/issues/22))

### Bugfixes

* The `-noidme` option is no longer passed to `hdiutil` on macOS 10.15 (Catalina) and later. ([#20](https://github.com/dmgbuild/dmgbuild/issues/20))
* Disk image size calculations now use base-10 units, consistent with `hdiutil`. ([#18](https://github.com/dmgbuild/dmgbuild/issues/18))
* RTF licenses specified as a file path are now handled correctly. ([#16](https://github.com/dmgbuild/dmgbuild/issues/16))

### Misc

* [#17](https://github.com/dmgbuild/dmgbuild/issues/17)

## 1.3.3 (2019-10-07)

### Features

* Detaching the disk image is now retried if it fails. ([#10](https://github.com/dmgbuild/dmgbuild/issues/10))

### Bugfixes

* Licensing now works on Python 3. ([#12](https://github.com/dmgbuild/dmgbuild/issues/12))
* A Python 2.7 compatibility problem was corrected.

## 1.3.2 (2017-10-13)

### Bugfixes

* A number of Python 3 compatibility problems were corrected. ([#2](https://github.com/dmgbuild/dmgbuild/issues/2))

### Misc

* [#3](https://github.com/dmgbuild/dmgbuild/issues/3), [#5](https://github.com/dmgbuild/dmgbuild/issues/5)

## 1.3.1 (2017-07-27)

### Features

* Settings can now be overridden directly when calling `build_dmg()`.
* A disk image compression level can now be specified.
* Badged icons can now be specified in JSON settings files.
* License files can be specified as file paths in the `licenses` map.
* The handling of background images was refactored.
* `hdiutil` output is now suppressed when flattening and unflattening the disk image.

### Bugfixes

* Window bounds in JSON settings files are now handled correctly.
* Web-style RGB colors are now handled correctly.
* License handling for non-English languages was corrected.
* The unnecessary `pyobjc-framework-Quartz` and `six` dependencies were removed.
* A Python 3 compatibility problem was corrected.

## 1.3.0 (2017-04-28)

### Features

* The size of the disk image is now calculated automatically if it isn't specified.
* License agreements can now be added to disk images.

### Bugfixes

* The `contents` property of an appdmg-style JSON settings file is no longer ignored.

## 1.2.1 (2016-12-05)

### Bugfixes

* The minimum required version of `ds_store` was increased.

## 1.2.0 (2016-12-02)

### Features

* Bookmarks are now included for background images, so that disk image backgrounds are displayed on macOS 10.12 (Sierra).

## 1.1.0 (2015-12-14)

### Features

* HiDPI background images are now automatically compiled from `@2x` image variants.
* Files are now copied using the system `ditto` command, preserving code signatures and other metadata.
* The `.Trashes` folder is now removed automatically.

### Bugfixes

* Bit depth is now taken into account when badging icons.
* The default grid spacing is now 100; the documentation now notes that `grid_spacing` must be 100 or less.
* Values in the icon view settings are now stored with the correct types.
* Copied files now retain their permissions (e.g., the executable bit).
* `defines` now work as expected.
* The writable temporary disk image is now created as a true temporary file, and disk images are detached when an error occurs.
* dmgbuild no longer fails when given a relative path with no directory component.
* The previously undeclared `pyobjc-framework-Quartz` dependency was added.
* The `six` dependency was removed.
* A Python 3 problem in the setup script was corrected.

## 1.0.0 (2014-02-17)

* Initial release.
