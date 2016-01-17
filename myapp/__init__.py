# -*- coding:utf8 -*-
__author__ = 'Sky'

from flask import Flask
from kvdb_module import KvdbStorage
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy()

login_manager = LoginManager()
# 初始化kvdb
kv = KvdbStorage()

# 导入view，否则not found
import views