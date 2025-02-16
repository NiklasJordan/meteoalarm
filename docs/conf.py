# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'MeteoAlarm library documentation'
author = 'Niklas Jordan'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_inline_tabs',
    'sphinx_examples',
    'sphinx_proof',
    'sphinx_hoverxref',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']

# -- Options for LaTeX output ------------------------------------------------

latex_documents = [
    ('index', 'meteoalarm.tex', 'MeteoAlarm library documentation',
     'Niklas Jordan', 'manual'),
]