from pathlib import Path

from settings import SRC_DIR
import os
from utils.file_operations import generate_uuid4_filename, create_dirs
from wand.image import Image as WandImage
from PIL import Image
import io
import gdal2tiles

MIN_ZOOM = 2
MAX_ZOOM = 5
TILE_SIZE = 256


def generate_tiles(stream: bytes, path: str, format_str: str):
    path = SRC_DIR / path

    create_dirs(path)

    temp_file_path = str(path / generate_uuid4_filename('temp.png'))

    bytes_img = io.BytesIO(stream)
    bytes_img.seek(0)

    if format_str == 'svg':
        with WandImage(blob=bytes_img.read(), format="svg") as image:
            png_image = image.make_blob("png")
            bytes_img = io.BytesIO(png_image)
            bytes_img.seek(0)

    with Image.open(bytes_img) as orig_world_map:
        orig_world_map.save(temp_file_path)

    try:
        gdal_to_tiles(file_path=temp_file_path, save_dir=path)
    except Exception as e:
        print(e)
    finally:
        os.remove(temp_file_path)
        if os.path.exists(path / 'tilemapresource.xml'):
            os.remove(path / 'tilemapresource.xml')


def gdal_to_tiles(file_path: str, save_dir: Path):
    options = {
        'zoom': (MIN_ZOOM, MAX_ZOOM),
        'tile_size': TILE_SIZE,
        'resume': True,
        'verbose': True,
        #'s_srs': "EPSG:3857",
        "profile": "raster",
        "webviewer": None,
    }
    gdal2tiles.generate_tiles(input_file=file_path, output_folder=str(save_dir), **options)
