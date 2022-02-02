from pathlib import Path

upload_folder = 'uploads'
download_folder = 'downloads'
download_fname = 'ebay_export.csv'
upload_fname = 'shopify_import.csv'
convert_script = 'scripts/ebay_import/app.py'
base_dir = Path(__file__).parent
uploaded_file = base_dir.joinpath(upload_folder, upload_fname)
download_file = base_dir.joinpath(download_folder, download_fname)
download_file_timeout = 60

index_ctx = {
    'base_url' : 'http://localhost:5000',
    'base_download_url' : 'http://localhost:5000/download'
}