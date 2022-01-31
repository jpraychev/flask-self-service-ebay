from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory, send_file
from werkzeug.utils import secure_filename
import subprocess
import io
import os
import config as cfg
app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
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
        return render_template("success.html")

@app.route('/download', methods=['GET'])
def downloads():
    download_data = io.BytesIO()
    with open(cfg.download_file, 'rb') as f:
        download_data.write(f.read())
        download_data.seek(0)

    cfg.download_file.unlink()
    return send_file(download_data, mimetype='text/csv', download_name=cfg.download_fname)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0')