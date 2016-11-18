#! /usr/bin/env python

"""TODO: Maybe add a docstring containing a long description

  This would double as something we could put int the `long_description`
  parameter for `setup` and it would squelch some complaints pylint has on
  `setup.py`.

"""

from setuptools import setup
import os

setup(name='demandlib',
      version='0.1.2dev',
      author='oemof developing group',
      url='http://github.com/oemof/demandlib',
      license='GPL3',
      author_email='oemof@rl-institut.de',
      description='Demandlib of the open energy modelling framework',
      packages=['demandlib', 'demandlib.examples'],
      package_data = {
          'demandlib': [os.path.join('bdew_data', '*.csv')],
          'demandlib.examples': ['*.csv']},
      install_requires=['numpy >= 1.7.0',
                        'pandas >= 0.18.0',
			'matplotlib']
     )
