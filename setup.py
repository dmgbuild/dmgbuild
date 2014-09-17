# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.rst', 'r') as f:
    long_desc = f.read().decode('utf-8')

setup(name='dmgbuild',
      version='1.0.0',
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
      install_requires=['ds_store >= 1.0.1',
                        'mac_alias >= 1.0.0',
                        'six >= 1.4.1'],
      provides=['dmgbuild']
)
