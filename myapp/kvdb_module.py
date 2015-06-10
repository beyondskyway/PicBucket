# -*- coding: utf-8 -*-
__author__ = 'Sky'

import sae
import json
import sae.kvdb


class KvdbStorage():
    # 初始化kvdb
    def __init__(self):
        self.kv = sae.kvdb.KVClient()

    # 获取value
    def get_value(self, key):
        return self.kv.get(key)

    # 获取dict_value
    def get(self, key):
        string_value = self.kv.get(key)
        if string_value is None:
            return None
        return decode_dict(string_value)

    # 设置value
    def set_value(self, key, value):
        self.kv.set(key, value)

    # 设置dict_value
    def set(self, key, dict_value):
        string_value = encode_dict(dict_value)
        self.kv.set(key, string_value)

    # 批量获取key
    def getkeys_by_prefix(self, prefix, limit=100, marker=None):
        return list(self.kv.getkeys_by_prefix(prefix, limit=limit, marker=marker))

    # 批量获取key/value
    def get_by_prefix(self, prefix, limit=100, marker=None):
        return self.kv.get_by_prefix(prefix, limit=limit, marker=marker)

    # 删除key
    def delete(self, key):
        self.kv.delete(key)


# 编码字典
def encode_dict(my_dict):
    return "\x1e".join("%s\x1f%s" % x for x in my_dict.iteritems())


# 解码字典
def decode_dict(my_string):
    return dict(x.split("\x1f") for x in my_string.split("\x1e"))


