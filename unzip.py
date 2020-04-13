import zipfile

def unzip(path_to_zip,directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)
