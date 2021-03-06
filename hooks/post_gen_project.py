#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_it(filepath):
    file_or_dir = os.path.join(PROJECT_DIRECTORY, filepath)
    if os.path.isfile(file_or_dir):
        os.remove(file_or_dir)
    else:
        shutil.rmtree(file_or_dir)


def main():
    to_delete = []

    if '{{ cookiecutter.use_bumpversion }}' == 'no':
        to_delete.append('.bumpversion.cfg')

    for file_or_dir in to_delete:
        remove_it(file_or_dir)


if __name__ == '__main__':
    main()
