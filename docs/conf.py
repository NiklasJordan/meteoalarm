# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'MeteoAlarm library documentation'
author = 'Niklas Jordan'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx_inline_tabs',
]

exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
