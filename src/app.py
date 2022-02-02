import io
import os
import subprocess
import config as cfg
from flask import Flask
from flask import request
from flask import send_file
from flask import render_template
from threading import Thread
from time import sleep

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', context=cfg.index_ctx)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file-upload' not in request.files:
            return
        f = request.files.get('file-upload')
        f.save(cfg.uploaded_file)
        os.chdir(cfg.base_dir)
        cmd = f'python {cfg.convert_script}'
        try:
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            raise Exception('Something went wrong', e)
        thr = Thread(target=delete_file)
        thr.start()
        return render_template("success.html", context=cfg.index_ctx)

def delete_file():
    sleep(cfg.download_file_timeout)
    cfg.download_file.unlink()

@app.route('/download', methods=['GET'])
def downloads():

    try:
        with open(cfg.download_file, 'rb') as f:
            download_data = io.BytesIO()
            download_data.write(f.read())
            download_data.seek(0)
    except FileNotFoundError:
        return render_template("index.html", context=cfg.index_ctx)

    cfg.download_file.unlink()
    return send_file(download_data, mimetype='text/csv', download_name=cfg.download_fname)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)