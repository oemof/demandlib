#! /usr/bin/env python

"""TODO: Maybe add a docstring containing a long description

  This would double as something we could put int the `long_description`
  parameter for `setup` and it would squelch some complaints pylint has on
  `setup.py`.

"""

from setuptools import setup

setup(name='demandlib',
      version='0.0.1',
      author='oemof developing group',
      url='http://github.com/oemof/demandlib',
      license='GPL3',
      author_email='oemof@rl-institut.de',
      description='Demandlib of the open energy modelling framework',
      packages=['demandlib'],
      package_dir={'demandlib': 'demandlib'},
      install_requires=[]
      )
