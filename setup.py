#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ) as fh:
        return fh.read()


setup(
    name="demandlib",
    version="0.1.9",
    license="MIT",
    description="Creating heat and power demand profiles from annual values.",
    long_description="%s"
    % (
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.rst")
        )
    ),
    long_description_content_type="text/x-rst",
    author="oemof developer group",
    author_email="contact@oemof.org",
    url="https://github.com/oemof/demandlib",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ],
    project_urls={
        "Documentation": "https://demandlib.readthedocs.io/",
        "Changelog": "https://demandlib.readthedocs.io/en/latest/changelog.html",
        "Issue Tracker": "https://github.com/oemof/demandlib/issues",
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires=">=3.6",
    install_requires=["numpy >= 1.17.0", "pandas >= 1.0"],
    package_data={
        "demandlib": [join("bdew_data", "*.csv")],
    },
    extras_require={
        "dev": ["pytest", "sphinx", "sphinx_rtd_theme", "matplotlib"],
        "examples": ["matplotlib", "workalendar"],
        "geometry": ["shapely", "geopandas"],
    },
)
