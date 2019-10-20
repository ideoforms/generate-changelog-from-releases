import os
from distutils.core import setup

setup(
    name = 'generate-changelog-from-releases',
    description = 'Generate a CHANGELOG.md from GitHub releases',
    version = '0.0.1',
    author = 'Daniel Jones',
    author_email = 'dan-code@erase.net',
    scripts = [ 'generate-changelog-from-releases.py' ],
    install_requires = [ 'pygithub' ]
)
