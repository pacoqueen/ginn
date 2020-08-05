#!/usr/bin/env python
"""Distutils setup file"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Metadata
PACKAGE_NAME = "simplegeneric"
PACKAGE_VERSION = "0.8.1"

def get_description():
    # Get our long description from the documentation
    f = open('README.txt')
    lines = []
    for line in f:
        if not line.strip():
            break     # skip to first blank line
    for line in f:
        if line.startswith('.. contents::'):
            break     # read to table of contents
        lines.append(line)
    f.close()
    return ''.join(lines)

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description= "Simple generic functions (similar to Python's own len(), "
        "pickle.dump(), etc.)",
    long_description = get_description(),
    url = "http://cheeseshop.python.org/pypi/simplegeneric",
    author="Phillip J. Eby",
    author_email="peak@eby-sarna.com",
    license="ZPL 2.1",
    test_suite = 'simplegeneric.test_suite',
    py_modules = ['simplegeneric'],
    classifiers = [
        line.strip() for line in open('classifiers.txt') if line.strip()
    ],
)
