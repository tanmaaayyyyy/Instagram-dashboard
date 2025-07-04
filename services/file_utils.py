import os
import requests
from datetime import datetime

DOWNLOAD_FOLDER = os.path.join("downloads", datetime.now().strftime("%Y-%m-%d"))
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return filepath
    return None
