# -*- coding:utf8 -*-
__author__ = 'Sky'

import json
from datetime import datetime
from flask import render_template, request, jsonify, make_response, redirect, url_for
from functools import wraps

import config
from kvdb_module import decode_dict
from myapp import app, kv
from upload import get_token, del_pic, QiniuUpload


# 允许跨域请求
def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'POST'
        allow_headers = 'Content-Type'
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun


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


# 修改锚点位置
def change_anchor(content, suffix):
    data = content.split('#')
    if len(data) == 1:
        return content + suffix
    else:
        return data[0] + suffix + "#" + data[1]


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
                # 修改锚点位置
                tmp['url'] = change_anchor(content['url'], "?imageView2/2/w/400/format/jpg")
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
            # 修改锚点位置
            tmp['url'] = change_anchor(content['url'], "?imageView2/2/w/400/format/jpg")
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


# 显示图片
@app.route('/bucket', methods=['POST', 'GET'])
def bucket():
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
                # 修改锚点位置
                tmp['url'] = change_anchor(content['url'], "?imageView2/2/w/400/format/jpg")
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
            # 修改锚点位置
            tmp['url'] = change_anchor(content['url'], "?imageView2/2/w/400/format/jpg")
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
    return render_template('index.html', data=json_data, domain=config.PIC_DOMAIN)


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
@app.route('/upQiniu', methods=['POST'])
def upQiniu():
    if request.form.get('subject'):
        upkeys = json.loads(request.form.get('key'))
        subject = request.form.get('subject')
        if subject is None:
            subject = 'Sunset Lake'
        content = request.form.get('content')
        import re
        items = re.findall(r'#(.+?)#', content)
        if len(items):
            author = items[0]
        else:
            author = 'skyway'
        # 时间差，用于加载排序
        import time
        future_time = int(time.mktime(datetime.strptime('3000-01-01 00:00:00.000', "%Y-%m-%d %H:%M:%S.%f").timetuple()) * 1000)
        from upload import QiniuUpload
        qn = QiniuUpload()
        for upkey in upkeys:
            # 去掉扩展名
            uid = future_time - int(upkey.split('.')[0])
            # 存入DB
            key = 'picbed_%s' % uid
            # 获取长宽信息
            info = qn.get_file_info(upkey)
            data = json.loads(info)
            width = data.get('width')
            height = data.get('height')
            url = config.PIC_DOMAIN + str(upkey) + '#width-' + str(width) + '-height-' + str(height)
            data = {'upkey': upkey, 'object': subject, 'words': content, 'author': author, 'url': url}
            kv.set(str(key), data)
        return 'success'
    # token, key = get_token()
    # filePath = "E:/Program/python/new/1/static/bulb_idea.jpg"
    # retData, respInfo = put_file(token, key, filePath)
    # return render_template('upload.html', domain=config.PIC_DOMAIN)


# 删除七牛文件
@app.route('/delQiniu', methods=['POST'])
def delQiniu():
    if request.form.get('key'):
        upkey = request.form.get('key')
        ret, info = del_pic(upkey)
        return 'success'


# 显示文件
@app.route('/files', methods=['GET', 'POST'])
def file_view():
    get_top_folder('SkyWatcher/Document/')
    return 'success'


# 提取文件夹及文件信息
def get_top_folder(prefix):
    qn = QiniuUpload(config.DISK_BUCKET, config.DISK_DOMAIN)
    files_info = qn.list_all(prefix=prefix, limit=None)
    # for item in files_info:
    #     print "type:%s size:%s path:%s time:%s" % (item['mimeType'], item['fsize'], item['key'], item['putTime'])
    # 提取顶级文件夹
    folders = set([])
    top_folders = []
    top_files = []
    json_data = []
    from myapp.common import get_nice_filesize, stamp_to_string
    for item in files_info:
        tmp = {}
        key = item['key'].replace(prefix, '', 1)
        path = key.split('/')
        # 文件
        if len(path) == 1:
            # top_files.add(key)
            tmp['type'] = 'file'
            tmp['name'] = key
            size = get_nice_filesize(int(item['fsize']))
            tmp['size'] = size
            # 17位时间戳
            put_time = stamp_to_string(item['putTime'])
            tmp['time'] = put_time
            top_files.append(tmp)
        # 文件夹
        else:
            if path[0] not in folders:
                tmp['type'] = 'folder'
                tmp['name'] = path[0]
                top_folders.append(tmp)
                folders.add(path[0])
    for i in top_folders:
        json_data.append(i)
    for j in top_files:
        json_data.append(j)
    print json_data
    for i in json_data:
        if i['type'] == 'file':
            print "name:%s size:%s time:%s" % (i['name'], i['size'], i['time'])
        else:
            print "name:%s" % i['name']