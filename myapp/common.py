# -*- coding: utf-8 -*-
__author__ = 'Sky'

import time
from datetime import datetime


# 把时间戳转成字符串形式
def timestamp_to_string(stamp):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(stamp))


# 17位时间戳转字符串
def stamp_to_string(stamp):
    return datetime.fromtimestamp(float(stamp)/10000000.0).strftime("%Y-%m-%d %H:%M:%S")


# 友好显示文件大小:12B，12.2KB， 12.2MB， 13.2GB
def get_nice_filesize(size):
    for (num, unit) in [(1024*1024*1024, 'GB'),
                        (1024*1024, 'MB'),
                        (1024, 'KB')]:
        if size > num:
            return "%.2f %s" % (size * 1.0 / num, unit)
    return "%s %s" % (size, 'B')


