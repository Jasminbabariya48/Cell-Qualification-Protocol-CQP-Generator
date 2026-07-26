import os
import shutil
import tempfile
from fastapi import UploadFile
from contextlib import contextmanager

@contextmanager
def save_upload_to_tempfile(upload_file: UploadFile, suffix: str = ""):
    # Save uploaded file to temp disk location and delete when done
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        with os.fdopen(fd, 'wb') as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
        yield path
    finally:
        if os.path.exists(path):
            os.remove(path)
