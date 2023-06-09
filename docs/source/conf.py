# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath('.'))
print(sys.path)
import gops
import myst_parser

verison = gops.__version__ 

project = 'GOPS'
copyright = '2023, Intelligent Driving Lab'
author = 'Intelligent Driving Lab'
release = '1.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'myst_parser']
myst_enable_extensions = {"colon_fence"}
html_theme = "classic"

lates_path = ['_templates']
exclude_patterns = []


source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
}
html_logo = 'figures&videos/GOPS_LOGO.png'

html_static_path = ['_static']
html_css_files = ['custom.css']


latex_engine = 'xelatex'
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
}
