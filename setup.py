from setuptools import setup

setup(name='dmgbuild',
      version='1.0',
      description='Mac OS X command line utility to build disk images',
      author='Alastair Houghton',
      author_email='alastair@alastairs-place.net',
      url='http://alastairs-place.net/projects/dmgbuild',
      packages=['dmgbuild'],
      scripts=['scripts/dmgbuild'],
      install_requires=['ds_store>=1.0.0',
                        'mac_alias>=1.0.0']
)
