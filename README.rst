========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |tox-pytest| |tox-checks| |coverage|
    * - package
      - | |version| |wheel| |supported-versions| |commits-since|


.. |tox-pytest| image:: https://github.com/oemof/oemof-demand/workflows/tox%20pytests/badge.svg
    :target: https://github.com/oemof/oemof-demand/actions?query=workflow%3A%22tox+checks%22

.. |tox-checks| image:: https://github.com/oemof/oemof-demand/workflows/tox%20checks/badge.svg?branch=dev
    :target: https://github.com/oemof/oemof-demand/actions?query=workflow%3A%22tox+checks%22

.. |coverage| image:: https://raw.githubusercontent.com/oemof/oemof-demand/python-coverage-comment-action-data/badge.svg
    :target: https://htmlpreview.github.io/?https://github.com/oemof/oemof-demand/blob/python-coverage-comment-action-data/htmlcov/index.html

.. |docs| image:: https://readthedocs.org/projects/oemof-demand/badge/?style=flat
    :target: https://oemof-demand.readthedocs.io/
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/oemof-demand.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/oemof-demand

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/oemof-demand.svg
    :alt: Supported versions
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

    pip install oemof.demand

You can also install the in-development version with::

    pip install https://github.com/oemof/oemof-demand/archive/dev.zip


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
