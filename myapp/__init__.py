# -*- coding:utf8 -*-
__author__ = 'Sky'

from flask import Flask
from kvdb_module import KvdbStorage


app = Flask(__name__)
app.config.from_object('config')

# 初始化kvdb
kv = KvdbStorage()

# 导入view，否则not found
import views