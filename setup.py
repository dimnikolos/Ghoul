from distutils.core import setup
import py2exe, sys, os

setup(windows=[{'script': 'Ghoul.py'}],
    options={
        'py2exe':
        {
            'bundle_files':2
        }
    },
	zipfile = None
)