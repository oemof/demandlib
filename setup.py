#! /usr/bin/env python

"""TODO: Maybe add a docstring containing a long description

  This would double as something we could put int the `long_description`
  parameter for `setup` and it would squelch some complaints pylint has on
  `setup.py`.

"""

from setuptools import find_packages, setup

import oemof

setup(name='demandlib',
      version='0.0.1',
      author='oemof developing group',
      author_email='oemof@rl-institut.de',
      description='Demandlib of the open energy modelling framework',
      packages=find_packages(),
      package_dir={'demandlib': 'demandlib'},
      install_requires=[]
     )
