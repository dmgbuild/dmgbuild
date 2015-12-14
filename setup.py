# -*- coding: utf-8 -*-
import sys
from setuptools import setup

with open('README.rst', 'rb') as f:
    long_desc = f.read().decode('utf-8')

# We have to be able to install on Linux to build the docs, even though
# dmgbuild presently won't work there because there's no SetFile
requires=['ds_store >= 1.0.1',
          'mac_alias >= 1.0.0',
          'six >= 1.4.1']

if sys.platform.startswith('darwin'):
    requires.append('pyobjc-framework-Quartz >= 3.0.4')

setup(name='dmgbuild',
      version='1.1.0',
      description='Mac OS X command line utility to build disk images',
      long_description=long_desc,
      author='Alastair Houghton',
      author_email='alastair@alastairs-place.net',
      url='http://alastairs-place.net/projects/dmgbuild',
      license='MIT License',
      platforms='darwin',
      packages=['dmgbuild'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Topic :: Desktop Environment',
          ],
      package_data = {
        'dmgbuild': ['resources/*']
      },
      scripts=['scripts/dmgbuild'],
      install_requires=requires,
      provides=['dmgbuild']
)
