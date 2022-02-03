import io
import os
import subprocess

import config as cfg

from flask import Flask, render_template, redirect
from flask import request, make_response
from flask import send_file, url_for

from threading import Thread
from time import sleep

from werkzeug.wrappers import Response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index() -> "Response":
    """ Upon file uploading, convert the file from shopify to ebay format.
        If successful sets a cookie with name 'download', which tracks users
        that are eligble to download the file.

    Raises:
        Exception: If file convertion fails, we throw an exception. Maybe we should
        redirect the user to a error page instead.

    Returns:
        Response - HTTP Response object with additional downlaod cookie
    """
    if request.method == 'GET':
        return render_template('index.html', context=cfg.index_ctx)

    if request.method == 'POST':
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
        
        Thread(target=delete_file).start()
        
        resp = make_response(render_template('success.html', context=cfg.index_ctx))
        resp.set_cookie(key='download', value='True', max_age=60)
        return resp

def delete_file():
    sleep(cfg.download_file_timeout)
    cfg.download_file.unlink()

@app.route('/download', methods=['GET'])
def download() -> io.BytesIO:
    """ Users are able to download their file through this API route only if they have
        the download cookie flag set to True. In order users to be able to download their
        file, we convert them to a BytesIO stored in memory and serve that as their
        download. The actual files are emmediately triggered to be deleted after 60 seconds,
        after being generated (clean up procedure)

    Returns:
        [io.BytesIO]: BytesIO copy of the original file
    """    
    if request.method == 'GET':     
        download_allowed = request.cookies.get('download')
        if not download_allowed:
            """ Download is not allowed because the cookie was never set 
                Redire the user to index page instead. """
            return 'You are not allowed to access this page directly!'
            return redirect(url_for('index'))
        try:
            with open(cfg.download_file, 'rb') as f:
                download_data = io.BytesIO()
                download_data.write(f.read())
                download_data.seek(0)
        except FileNotFoundError:
            return "File has been already deleted. Please generate new one!"
            return redirect(url_for('index'))
    return send_file(download_data, mimetype='text/csv', download_name=cfg.download_fname)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)