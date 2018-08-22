# -*- coding: utf-8 -*-

import redis
from zweb.orm import config as orm_config
from zweb.orm import torndb

from .config import (
    REDIS_HOST, REDIS_PORT, REDIS_DB,
    MYSQL_HOST, MYSQL_DB,
    MYSQL_USER, MYSQL_PWD, MYSQL_CHARSET
)

_rdb = None
_db = None

orm_config.db_by_table = lambda table: _db


def setup_model(print_sql=False):
    global _rdb
    global _db

    redis_pool = redis.ConnectionPool(
        host=REDIS_HOST, port=REDIS_PORT,
        db=REDIS_DB
    )
    _rdb = redis.StrictRedis(connection_pool=redis_pool)

    _db = torndb.Connection(
        host=MYSQL_HOST, database=MYSQL_DB,
        user=MYSQL_USER, password=MYSQL_PWD,
        charset=MYSQL_CHARSET, debug=print_sql
    )
