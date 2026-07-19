# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

import time

project = 'MFI Digital Data Backbone'
author = 'Carnegie Mellon University, Manufacturing Futures Institute'
copyright = '{}, {}'.format(time.strftime('%Y'), author)
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'myst_parser',
    'sphinx_copybutton',
    'sphinx.ext.mathjax',
    'sphinxcontrib.mermaid',
    'sphinx_design',
]

myst_enable_extensions = ["colon_fence"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

mathjax_path = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'pages/parked']


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
}
html_logo = 'files/ddb_logo.png'
# html_favicon = 'files/white-logo.ico'
html_favicon = 'files/ddb_logo.ico'
html_static_path = ['_static']

html_css_files = [
    'custom.css',
    'equipment.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css',
]

# -- top-right github link configuration -------------------------------------

html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "cmu-mfi", # Username
    "github_repo": "ddb", # Repo name
    "github_version": "main", # Version
    "conf_py_path": "/doc/", # Path in the checkout to the docs root
}

# -- MyST navigation ---------------------------------------------------------

myst_enable_extensions = [
    "colon_fence",
    "substitution",
]