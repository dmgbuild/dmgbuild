#!/usr/bin/env python
from setuptools import setup

setup()

# # -*- coding: utf-8 -*-
# import sys
# from setuptools import setup
# from setuptools.command.test import test as TestCommand

# class PyTest(TestCommand):
#     def finalize_options(self):
#         TestCommand.finalize_options(self)
#         self.test_args = []
#         self.test_suite = True

#     def run_tests(self):
#         import pytest
#         errno = pytest.main(self.test_args)
#         sys.exit(errno)

# with open('README.rst', 'rb') as f:
#     long_desc = f.read().decode('utf-8')

# # We have to be able to install on Linux to build the docs, even though
# # dmgbuild presently won't work there because there's no SetFile
# requires=['ds_store >= 1.1.0',
#           'mac_alias >= 2.0.1']


# setup(name='dmgbuild',
#       version='1.5.2',
#       packages=['dmgbuild'],
#       package_data = {
#         'dmgbuild': ['resources/*']
#       },
#       entry_points = {
#         'console_scripts': [
#             'dmgbuild = dmgbuild.__main__:main'
#         ],
#       },
#       install_requires=requires,
#       tests_require=tests_require,
#       cmdclass={
#           'test': PyTest
#           },
#       provides=['dmgbuild']
# )
