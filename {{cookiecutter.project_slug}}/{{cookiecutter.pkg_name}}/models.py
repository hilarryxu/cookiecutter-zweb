# -*- coding: utf-8 -*-

from zweb.orm.model import Model


class BaseModel(Model):
    class Meta(object):
        abstract = True


class User(BaseModel):
    class Meta(object):
        db_table = '{{cookiecutter.pkg_name}}_user'
