import os
import requests
import py7zr

def download_and_extract(url, extract_path):
    file_name = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with py7zr.SevenZipFile(file_name, mode='r') as z:
        z.extractall(path=extract_path)
    os.remove(file_name)

urls = [
    'https://s3.amazonaws.com/wikia_xml_dumps/y/ya/yakuza_pages_current.xml.7z',
    'https://s3.amazonaws.com/wikia_xml_dumps/y/ya/yakuza_pages_full.xml.7z'
]

for url in urls:
    download_and_extract(url, './Data')
