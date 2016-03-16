# -*- coding: utf-8 -*-
from flask import Flask,render_template, request, jsonify
from werkzeug.utils import secure_filename
from wtforms import Form

from qiniu import Auth, put_file
import qiniu.config

app = Flask(__name__)


@app.route('/')
def hello_world():

    #files = file_list()
    return render_template('index.html')
    #return file_list()
    #return "hello"

"""
返回bucket中的文件列表
"""
@app.route('/data')
def file_list():
    from sae.storage import Bucket
    bucket = Bucket('t')
    bucket.put()
    res = []
    id = 1
    import time
    for item in bucket.list():
        """  hash,last_modified,bytes,name,content_type
        """
        tmp = {}
        tmp['id'] = id
        tmp['name'] = item.name
        tmp['time'] = bucket.stat_object(item.name).metadata['time']
        tmp['ptime'] = str(item)
        tmp['bytes'] = item.bytes
        tmp['type'] = item.content_type
        #tmp['data'] = str(bucket.stat_object(item.name))
        id = id + 1
        res.append(tmp)
    #return res
    return jsonify({'data':res})

"""
返回主页
"""
def homepage():
    return render_template("index.html")

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/upload/', methods=('GET', 'POST'))
def upload():
    if request.method == 'POST':
        f = request.files['file']
        sae_bucket_store(f)
        #sae_stor(f)
        #f.save('/file.png')
        #store('/file.png')
    return f.filename


def sae_bucket_store(f):
    from sae.storage import Bucket
    import time
    tm = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    bucket = Bucket('t')
    bucket.put()
    bucket.put_object(f.filename,f,metadata={"time":tm})


def sae_stor(content):
    import sae.const
    ak = sae.const.ACCESS_KEY
    sk = sae.const.SECRET_KEY
    appname = sae.const.APP_NAME
    domain_name = content.name #刚申请的domain

    import sae.storage
    s = sae.storage.Client()
    ob = sae.storage.Object(content.read())
    url = s.put(domain_name,content.name,ob)
    return "success"

def store(localfile):
    #需要填写你的 Access Key 和 Secret Key
    access_key = 'GkYbeSGvXnC1utr0lxFv5BuM8-0pP4Q5P-QdzY5j'
    secret_key = 'PZbppOQ91tTTMzTR9UITDWI7GtGOcpV2NO4Yc3DZ'

    #构建鉴权对象
    q = Auth(access_key, secret_key)

    #要上传的空间
    bucket_name = 'baogao'

    #上传到七牛后保存的文件名
    filename = '1.png'

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, filename, 3600)
    ret, info = put_file(token, filename, localfile)
    return info


if __name__ == '__main__':
    app.debug = True
    app.run()