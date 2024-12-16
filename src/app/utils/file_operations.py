import shutil
import os
from pathlib import Path
from settings import SRC_DIR
from starlette.datastructures import UploadFile

import uuid


def create_dirs(path: Path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_upload_file(upload_file: UploadFile, destination: Path) -> str:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()
    return str(destination).split(str(SRC_DIR))[-1][1:]


def generate_uuid4_filename(filename):
    discard, ext = filename.rsplit('.', 1)
    basename = uuid.uuid4().hex
    return '.'.join([basename, ext])


async def upload_file(file: UploadFile, path: Path):
    path.mkdir(parents=True, exist_ok=True)

    path = path / generate_uuid4_filename(file.filename)
    save_upload_file(file, path)
    return str(path).split(str(SRC_DIR))[-1][1:]


async def delete_file(path: Path):
    str_path = str(path)

    if os.path.exists(str_path):
        if os.path.isfile(str_path):
            os.remove(str_path)
        elif os.path.isdir(str_path):
            shutil.rmtree(str_path)
