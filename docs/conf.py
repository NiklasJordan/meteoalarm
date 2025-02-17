# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'MeteoAlarm library documentation'
author = 'Niklas Jordan'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx_inline_tabs',
    'sphinx_external_toc',
]

exclude_patterns = []
external_toc_path = '_toc.yml'
templates_path = ['_templates']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
