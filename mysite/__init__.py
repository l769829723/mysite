from __future__ import absolute_import

# PyMySQL
from pymysql import install_as_MySQLdb
install_as_MySQLdb()


# Celery
from .celery import app as celery_app