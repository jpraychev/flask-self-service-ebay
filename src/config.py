from pathlib import Path

# File variables
upload_folder = 'uploads'
download_folder = 'downloads'
download_fname = 'ebay_export.csv'
upload_fname = 'shopify_import.csv'
convert_script = 'scripts/ebay_import/app.py'
base_dir = Path(__file__).parent
uploaded_file = base_dir.joinpath(upload_folder, upload_fname)
download_file = base_dir.joinpath(download_folder, download_fname)
download_file_timeout = 60

# Service variables
DEV_ENV = True
SERVER_IP = 'localhost' if DEV_ENV else '192.46.239.37'
SERVER_PORT = 5000
DEBUG = True if DEV_ENV else False

# Template context
index_ctx = {
    'base_url' : f'http://{SERVER_IP}:{SERVER_PORT}',
    'base_download_url' : f'http://{SERVER_IP}:{SERVER_PORT}/download'
}