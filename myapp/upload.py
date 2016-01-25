# -*- coding: utf-8 -*-
__author__ = 'Sky'


import qiniu
from datetime import datetime
import config
from qiniu import BucketManager
import urllib2
import json


def get_token():
    q = qiniu.Auth(config.QINIU_ACCESS_KEY, config.QINIU_SECRET_KEY)
    # print str(datetime.now())
    token = q.upload_token(config.PIC_BUCKET)
    return token


def del_pic(upkey):
    q = qiniu.Auth(config.QINIU_ACCESS_KEY, config.QINIU_SECRET_KEY)
    bucket = BucketManager(q)
    ret, info = bucket.delete(config.PIC_BUCKET, upkey)
    return ret, info


class QiniuUpload():
    def __init__(self, bucket = config.PIC_BUCKET, domain = config.PIC_DOMAIN):
        self.qiniuer = qiniu.Auth(config.QINIU_ACCESS_KEY, config.QINIU_SECRET_KEY)
        self.bucket_manager = BucketManager(self.qiniuer)
        self.bucket = bucket
        self.domain = domain

    def get_token(self):
        return self.qiniuer.upload_token(self.bucket)

    def del_file(self, key):
        ret, info = self.bucket_manager.delete(self.bucket, key)
        # 错误处理
        assert ret is None
        assert info.status_code == 612
        return ret, info

    def get_upload_info(self, key):
        ret, info = self.bucket_manager.stat(self.bucket, key)
        assert 'hash' in ret
        return info

    def get_file_info(self, key):
        url = self.domain + key + '?imageInfo'
        try:
            response = urllib2.urlopen(url, timeout=5)
            resp = response.read()
            return resp
        except Exception, e:
            print e
            return None

    def list_all(self, prefix=None, limit=None):
        marker = None
        eof = False
        while eof is False:
            ret, eof, info = self.bucket_manager.list(self.bucket, prefix=prefix, marker=marker, limit=limit)
            marker = ret.get('marker', None)
            for item in ret['items']:
                print(item['key'])
                pass
        if eof is not True:
            # 错误处理
            pass
