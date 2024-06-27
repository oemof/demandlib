# -*- coding: utf-8 -*-

import os

from sphinx.ext.autodoc import between

from demandlib import __version__


def setup(app):
    # Register a sphinx.ext.autodoc.between listener to ignore everything
    # between lines that contain the word IGNORE
    app.connect("autodoc-process-docstring", between("^SPDX.*$", exclude=True))
    return app


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.imgmath",
]
source_suffix = ".rst"
master_doc = "index"
project = "demandlib"
year = "2016-2024"
author = "oemof developer group"
copyright = "{0}, {1}".format(year, author)
version = release = __version__

pygments_style = "trac"
templates_path = ["."]
extlinks = {
    "issue": ("https://github.com/oemof/demandlib/issues/%s", "#"),
    "pr": ("https://github.com/oemof/demandlib/pull/%s", "PR #"),
}
# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get("READTHEDOCS", None) == "True"

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = "sphinx_rtd_theme"

html_use_smartypants = True
html_last_updated_fmt = "%b %d, %Y"
html_split_index = False
html_sidebars = {
    "**": ["searchbox.html", "globaltoc.html", "sourcelink.html"],
}
html_short_title = "%s-%s" % (project, version)

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False
nitpicky = False

linkcheck_ignore = [
    r"https://requires.io/.*",
    r"https://www.avacon-netz.de/.*",
]
