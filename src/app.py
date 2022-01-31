from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory, send_file
from werkzeug.utils import secure_filename
from pathlib import Path
import subprocess
import io
import os

app = Flask(__name__)
upload_folder = 'uploads'
download_folder = 'downloads'
download_fname = 'ebay_export.csv'
upload_fname = 'shopify_import.csv'
convert_script = 'scripts/ebay_import/app.py'
base_dir = Path(__file__).parent
# upload_dir = base_dir.joinpath(upload_folder)
uploaded_file = base_dir.joinpath(upload_folder, upload_fname)
download_file = base_dir.joinpath(download_folder, download_fname)
# download_dir = base_dir.joinpath('download/ebay_import.csv')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file-upload' not in request.files:
            return
        f = request.files.get('file-upload')
        fname = secure_filename(f.filename)
        f.save(uploaded_file)
        os.chdir(base_dir)
        cmd = f'python {convert_script}'
        try:
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            raise Exception('Something went wrong', e)
        return render_template("success.html")

@app.route('/download', methods=['GET'])
def downloads():
    download_data = io.BytesIO()
    with open(download_file, 'rb') as f:
        download_data.write(f.read())
        download_data.seek(0)

    download_file.unlink()
    return send_file(download_data, mimetype='text/csv', download_name=download_fname)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0')