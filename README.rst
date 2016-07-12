The demandlib is part of the oemof group but works as a standalone application.

.. contents:: `Table of contents`
    :depth: 1
    :local:
    :backlinks: top

Introduction
============

With the demandlib you can create power and heat profiles for various sectors by scaling them to your desired demand. Additionally you can specify a year so that holidays are considered respectively.


Actual Release
~~~~~~~~~~~~~~


Developing Version
~~~~~~~~~~~~~~~~~~

Clone/Fork: https://github.com/oemof/demandlib

As the demandlib is part of the oemof developer group we use the same developer rules:
http://oemof.readthedocs.io/en/stable/developer_notes.html

Installation
============

Developing the demandlib
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have push rights clone this repository to your local system.

::

    git clone git@github.com:oemof/demandlib.git
    
If you do not have push rights, fork the project at github, clone your personal fork to your system and send a pull request.

If the project is cloned you can install it using pip3 (or pip2) with the -e flag. Using this installation, every change is applied directly.

::

    sudo pip3 install -e <path/to/the/demandlib/root/dir>
    
  
Optional Packages
~~~~~~~~~~~~~~~~~

To see the plots of the example file one should install the matplotlib package.

Matplotlib can be installed using pip but some Linux users reported that it is easier and more stable to use the pre-built packages of your Linux distribution.

http://matplotlib.org/users/installing.html

Example
~~~~~~~~~~~~~~~~~~~~~~~~

Execute the example files for power and heat:
https://github.com/oemof/demandlib/tree/master/examples

Basic Usage
===========

*Power profiles*

You need to specify the year and the annual demand per sector like the following:

year = 2013

ann_el_demand_per_sector = {
    'g0': 3000,
    'h0': 3000,
    'i0': 3000,
    'g6': 5000}

Note: i0 is not a BDEW profile.
   
*Heat profiles*
