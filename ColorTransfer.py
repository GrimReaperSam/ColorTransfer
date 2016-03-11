import os
from flask import Flask, render_template, request, url_for, redirect, send_from_directory, json, after_this_request
from werkzeug import secure_filename
import transferer
import uuid

import urllib, cStringIO
from PIL import Image
import numpy as np
import cv2
from PIL import Image
import base64


UPLOAD_FOLDER = 'static'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/transfer', methods=['POST'])
def transfer():
    source = request.files['source']
    target = request.files['target']
    source = _fs_to_cv2(source)
    target = _fs_to_cv2(target)
    cvim = transferer.transfer_cv2(source, target)

    pil_im = Image.fromarray(cv2.cvtColor(cvim, cv2.COLOR_BGR2RGB))
    buff = cStringIO.StringIO()
    pil_im.save(buff, format="JPEG")
    b64 = base64.b64encode(buff.getvalue())
    return json.dumps({'status': 'OK', 'img': b64})


def _fs_to_cv2(image):
    sfile = cStringIO.StringIO()
    image.save(sfile)
    sfile.reset()
    img = Image.open(sfile)
    nip = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
    return cv2.cvtColor(nip, cv2.COLOR_RGB2BGR)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run()
