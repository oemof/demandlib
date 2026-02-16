========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |tox-pytest| |tox-checks| |coveralls|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations| |commits-since| |packaging|


.. |tox-pytest| image:: https://github.com/oemof/oemof-demand/workflows/tox%20pytests/badge.svg
     :target: https://github.com/oemof/oemof-demand/actions?query=workflow%3A%22tox+checks%22

.. |tox-checks| image:: https://github.com/oemof/oemof-demand/workflows/tox%20checks/badge.svg?branch=dev
     :target: https://github.com/oemof/oemof-demand/actions?query=workflow%3A%22tox+checks%22

.. |packaging| image:: https://github.com/oemof/oemof-demand/workflows/packaging/badge.svg?branch=dev
     :target: https://github.com/oemof/oemof-demand/actions?query=workflow%3Apackaging

.. |docs| image:: https://readthedocs.org/projects/oemof-demand/badge/?style=flat
    :target: https://oemof-demand.readthedocs.io/
    :alt: Documentation Status

.. |coveralls| image:: https://coveralls.io/repos/oemof/oemof-demand/badge.svg?branch=dev&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/github/oemof/oemof-demand?branch=dev

.. |version| image:: https://img.shields.io/pypi/v/oemof-demand.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/oemof-demand

.. |wheel| image:: https://img.shields.io/pypi/wheel/oemof-demand.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/oemof-demand

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/oemof-demand.svg
    :alt: Supported versions
    :target: https://pypi.org/project/oemof-demand

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/oemof-demand.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/oemof-demand

.. |commits-since| image:: https://img.shields.io/github/commits-since/oemof/oemof-demand/latest/dev
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof-demand/compare/master...dev



.. end-badges

Creating heat and power demand profiles from annual values.

* Free software: MIT license

Installation
============

::

    pip install oemof-demand

You can also install the in-development version with::

    pip install https://github.com/oemof/oemof-demand/archive/master.zip


Documentation
=============


https://oemof-demand.readthedocs.io/


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
