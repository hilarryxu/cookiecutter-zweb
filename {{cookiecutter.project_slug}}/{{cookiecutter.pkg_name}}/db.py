# -*- coding: utf-8 -*-

import redis
from zweb.orm import config as orm_config, torndb

from .config import (
    MYSQL_CHARSET,
    MYSQL_DB,
    MYSQL_HOST,
    MYSQL_PWD,
    MYSQL_USER,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PORT,
)

_rdb = None
_db = None

orm_config.db_by_table = lambda table: _db


def setup_model(print_sql=False):
    global _rdb
    global _db

    _rdb = redis.StrictRedis(
        host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
    )

    _db = torndb.Connection(
        host=MYSQL_HOST,
        database=MYSQL_DB,
        user=MYSQL_USER,
        password=MYSQL_PWD,
        charset=MYSQL_CHARSET,
        debug=print_sql,
    )
