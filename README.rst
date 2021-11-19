========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |appveyor| |requires|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/demandlib/badge/?style=flat
    :target: https://demandlib.readthedocs.io/
    :alt: Documentation Status

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/oemof/demandlib?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/oemof/demandlib

.. |requires| image:: https://requires.io/github/oemof/demandlib/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/oemof/demandlib/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/oemof/demandlib/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/oemof/demandlib

.. |codecov| image:: https://codecov.io/gh/oemof/demandlib/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/oemof/demandlib

.. |version| image:: https://img.shields.io/pypi/v/demandlib.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/demandlib

.. |wheel| image:: https://img.shields.io/pypi/wheel/demandlib.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/demandlib

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/demandlib.svg
    :alt: Supported versions
    :target: https://pypi.org/project/demandlib

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/demandlib.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/demandlib

.. |commits-since| image:: https://img.shields.io/github/commits-since/oemof/demandlib/v0.1.8.svg
    :alt: Commits since latest release
    :target: https://github.com/oemof/demandlib/compare/v0.1.8...dev



.. end-badges

Creating heat and power demand profiles from annual values.

* Free software: MIT license

Installation
============

::

    pip install demandlib

You can also install the in-development version with::

    pip install https://github.com/oemof/demandlib/archive/master.zip


Documentation
=============


https://demandlib.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
