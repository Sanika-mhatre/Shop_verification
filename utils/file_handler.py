import os
import shutil
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

def save_uploaded_file(file: UploadFile, folder_name: str):
    folder_path = os.path.join(UPLOAD_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path