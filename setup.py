#!/usr/bin/env python

import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='djtemps',
    version='0.1.1',
    description='Easy Django - Jinja2 Templates Integration',
    author='Ozgur Sefik Altunyurt',
    author_email='altunyurt@gmail.com',
    url='http://github.com/altunyurt/djtemps',
    packages=['djtemps', 'djtemps/translation' ],
    long_description=read('README'),
    license = 'GPL',
    classifiers = [
        "Development Status :: 4 - Beta",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Text Processing :: Markup :: HTML"
    ]
)
