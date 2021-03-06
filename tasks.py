#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import shutil

from invoke import task

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'cookiecutter.json'), 'r') as fp:
    COOKIECUTTER_SETTINGS = json.load(fp)
COOKIE = os.path.join(HERE, COOKIECUTTER_SETTINGS['project_slug'])
REQUIREMENTS = os.path.join(COOKIE, 'requirements', 'dev.txt')


@task
def build(ctx):
    """Build the cookiecutter."""
    ctx.run('cookiecutter {0} --no-input'.format(HERE))


@task
def clean(ctx):
    """Clean out generated cookiecutter."""
    if os.path.exists(COOKIE):
        shutil.rmtree(COOKIE)
        print('Removed {0}'.format(COOKIE))
    else:
        print('App directory does not exist. Skipping.')
