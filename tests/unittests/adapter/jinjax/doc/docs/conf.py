# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../../../../.."))


# -- Project information -----------------------------------------------------

project = "Dummy"
author = "Dummy"
copyright = author

# The short X.Y version
version = "1.0"
# The full version, including alpha/beta/rc tags
release = version

# fastapi_tag = pkg_meta["dependencies"]["fastapi"].lstrip("^")


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "fastlife.adapters.jinjax.jinjax_ext.jinjax_doc",
]

jinjax_doc_output_dir = "components"
jinjax_template_search_path = "fastlife_app:templates"
