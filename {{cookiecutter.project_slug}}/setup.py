#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import re
from setuptools import setup, find_packages

kwargs = {}

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('{{cookiecutter.pkg_name}}/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r"__version__ = \'(.*?)\'", f.read()).group(1)

setup(
    name='{{cookiecutter.project_slug}}',
    version=version,
    description='{{cookiecutter.project_short_description}}',
    long_description=readme,
    author='{{cookiecutter.full_name}}',
    author_email='{{cookiecutter.email}}',
    url='https://github.com/hilarryxu/{{cookiecutter.project_slug}}',
    license='BSD',
    packages=find_packages(exclude=['test*', 'docs', 'examples']),
    **kwargs
)
