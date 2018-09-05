The **demandlib** is part of the oemof group but works as a standalone application.

.. contents:: `Table of contents`
    :depth: 1
    :local:
    :backlinks: top

Introduction
============

With the demandlib you can create power and heat profiles for various sectors by scaling them to your desired demand. Additionally you can specify a year so that holidays are considered respectively.


Current Release
===============

Install the demandlib using pypi:

::

    pip install demandlib

You can also install the beta version with the most actual changes:

::

    pip install git+https://github.com/oemof/demandlib


Developing Version
==================

Documentation
~~~~~~~~~~~~~

Read the latest documentation at Readthedocs.org

http://demandlib.readthedocs.org


Installation
~~~~~~~~~~~~

Clone the demandlib from github.

::

    git clone git@github.com:oemof/demandlib.git
    

If the project is cloned you can install it using pip with the -e flag. 

::

    pip install -e <path/to/the/demandlib/root/dir>


Developing the demandlib
~~~~~~~~~~~~~~~~~~~~~~~~~

As the demandlib is part of the oemof developer group we use the same developer rules:

http://oemof.readthedocs.io/en/stable/developing_oemof.html

If you have push rights clone this repository to your local system.

::

    git clone git@github.com:oemof/demandlib.git
    
If you want to contribute, fork the project at github, clone your personal fork to your system and send a pull request.
    
  
Example
=======

We provide two examples on how to use the demandlib. One for the heat sector, executable by calling ``demandlib_heat_example``, and one showing how to create electricity demand time series, executable by calling ``demandlib_power_example``. Both examples are callable from anywhere in the command-line.
