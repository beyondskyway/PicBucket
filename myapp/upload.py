# -*- coding: utf-8 -*-
__author__ = 'Sky'


import qiniu
from datetime import datetime
import config


def get_token():
    q = qiniu.Auth(config.QINIU_ACCESS_KEY, config.QINIU_SECRET_KEY)
    # print str(datetime.now())
    token = q.upload_token(config.PIC_BUCKET)
    return token

