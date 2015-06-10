# -*- coding:utf8 -*-
__author__ = 'Sky'


from datetime import datetime
from flask import render_template, request, jsonify, make_response, redirect, url_for
from myapp import app, kv
import config
import json
from functools import wraps
from upload import get_token
from kvdb_module import decode_dict
import qiniu


@app.before_request
def before_request():
    pass


@app.teardown_request
def teardown_request(func):
    pass


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect(url_for('pic_bed'))


# 显示图片
@app.route('/picbed', methods=['POST', 'GET'])
def pic_bed():
    # 加载更多
    if request.form.get('key'):
        key = request.form.get('key')
        # print key
        key_values = kv.get_by_prefix('picbed_', 10, key)
        # print sorted(kv.getkeys_by_prefix('picbed', 3, key))
        data = tuple(key_values)
        # data = sorted(data, reverse=True)
        print data
        json_data = []
        for item in data:
            tmp = {}
            tmp['key'] = item[0]
            if '\x1e' in item[1]:
                content = decode_dict(item[1])
                # print content
                tmp['url'] = content['url'] + "?imageView2/2/w/400/format/jpg"
                tmp['object'] = content['object']
                tmp['words'] = content['words']
                tmp['upkey'] = content['upkey']
                tmp['author'] = content['author']
            else:
                tmp['url'] = item[1] + "?imageView2/2/w/400/format/jpg"
                tmp['object'] = 'Sunset Lake'
                tmp['words'] = 'A peaceful sunset view...'
                tmp['upkey'] = item[1][-13:]
                tmp['author'] = 'skyway'
            json_data.append(tmp)
        json_str = json.dumps(json_data)
        return json_str
    # 初始加载
    key_values = kv.get_by_prefix('picbed_', 20, None)
    # print sorted(kv.getkeys_by_prefix('picbed', 3, None))
    data = tuple(key_values)
    json_data = []
    for item in data:
        tmp = {}
        tmp['key'] = item[0]
        if '\x1e' in item[1]:
            content = decode_dict(item[1])
            # print content
            tmp['url'] = content['url'] + "?imageView2/2/w/400/format/jpg"
            tmp['object'] = content['object']
            tmp['words'] = content['words']
            tmp['upkey'] = content['upkey']
            tmp['author'] = content['author']
        else:
            tmp['url'] = item[1] + "?imageView2/2/w/400/format/jpg"
            tmp['object'] = 'Sunset Lake'
            tmp['words'] = 'A peaceful sunset view...'
            tmp['upkey'] = item[1][-13:]
            tmp['author'] = 'skyway'
        json_data.append(tmp)
    # data = sorted(data, reverse=True)
    # print data
    return render_template('PicBed.html', data=json_data, domain=config.PIC_DOMAIN)


# 获取uptoken
@app.route('/uptoken', methods=['POST', 'GET'])
def uptoken():
    token = get_token()
    # 上传本地文件
    # retData, respInfo = put_file(token, key, filePath)
    # filePath = "E:/Program/python/new/1/static/bulb_idea.jpg"
    # import time
    # key = time.time()
    # retData, respInfo = qiniu.put_file(token, str(key), filePath)
    # print "%s %s %s" % (token, retData, respInfo)
    return jsonify(uptoken=token)


# 上传文件到七牛
@app.route('/upQiniu', methods=['POST', 'GET'])
def upQiniu():
    if request.form.get('key'):
        url = request.form.get('url')
        upkey = request.form.get('key')
        # 时间差，用于加载排序
        import time
        future_time = int(time.mktime(datetime.strptime('3000-01-01 00:00:00.000', "%Y-%m-%d %H:%M:%S.%f").timetuple()) * 1000)
        uid = future_time - int(upkey)
        # 存入DB
        key = 'picbed_%s' % uid
        object = 'Sunset Lake'
        words = 'A peaceful sunset view...'
        author = 'skyway'
        # print key
        data = {'upkey': upkey, 'object': object, 'words': words, 'author': author, 'url': url}
        kv.set(str(key), data)
        # kv.set_value(str(key), url)
        return 'success'
    # token, key = get_token()
    # filePath = "E:/Program/python/new/1/static/bulb_idea.jpg"
    # retData, respInfo = put_file(token, key, filePath)
    # return render_template('upload.html', domain=config.PIC_DOMAIN)