import os
from flask import Flask, render_template, request, url_for, redirect, send_from_directory, json, after_this_request
from werkzeug import secure_filename
import transferer
import uuid


UPLOAD_FOLDER = 'static'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        source = request.files['source']
        target = request.files['target']
        if file:
            source_name = secure_filename(source.filename)
            target_name = secure_filename(target.filename)
            source_path = os.path.join(app.config['UPLOAD_FOLDER'], source_name)
            target_path = os.path.join(app.config['UPLOAD_FOLDER'], target_name)
            source.save(source_path)
            target.save(target_path)
            return redirect(url_for('transfer', source=source_name, target=target_name))
    else:
        return render_template('index.html')


@app.route('/transfer')
def transfer():
    source_name = request.args['source']
    target_name = request.args['target']
    source_path = os.path.join(app.config['UPLOAD_FOLDER'], source_name)
    target_path = os.path.join(app.config['UPLOAD_FOLDER'], target_name)
    transfer_path = os.path.join(app.config['UPLOAD_FOLDER'], "%s.png" % str(uuid.uuid4()))
    transferer.transfer(source_path, target_path, transfer_path)
    images = {'source': source_path,
              'target': target_path,
              'transfer': transfer_path}
    return render_template('transfer.html', images=images)


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run()
