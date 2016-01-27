# -*- coding:utf8 -*-
__author__ = 'Sky'

# flask-app密钥
SECRET_KEY = 'app-secret-key'
# 启用防止跨域请求
CSRF_ENABLED = True
# 启用debug
DEBUG = True

# 七牛access-key和secret-key
QINIU_ACCESS_KEY = 'access-key'
QINIU_SECRET_KEY = 'secret-key'

# 七牛空间名
PIC_BUCKET = 'bucket-name'
# 七牛域名
PIC_DOMAIN = 'domain-url'

# 网盘存储空间及域名
DISK_BUCKET = 'bucket-name'
DISK_DOMAIN = 'domain-url'

# MYSQL配置信息
MYSQL_USER = ''
MYSQL_PASS = ''
MYSQL_HOST = '127.0.0.1'
MYSQL_HOST_S = '127.0.0.1'
MYSQL_PORT = '3306'
MYSQL_DB = 'bucket'

SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s?charset=utf8' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)