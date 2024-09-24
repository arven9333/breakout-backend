import os
import io
import gdal2tiles

from pathlib import Path

from wand.color import Color
from wand.image import Image as WandImage

from settings import SRC_DIR

from utils.file_operations import generate_uuid4_filename, create_dirs

from PIL import Image

MIN_ZOOM = 2
MAX_ZOOM = 5
TILE_SIZE = 256


def generate_tiles(stream: bytes, path: str, format_str: str):
    path = SRC_DIR / path

    create_dirs(path)

    filename = generate_uuid4_filename(f'temp.png')
    temp_file_path = str(path / filename)

    bytes_img = io.BytesIO(stream)

    if format_str == 'svg':
        with WandImage(blob=bytes_img.read()) as image:
            image.format = 'png'
            image.background_color = Color('transparent')
            image.save(filename=f"png32:{temp_file_path}")
    else:
        with Image.open(bytes_img) as orig_world_map:
            orig_world_map.save(temp_file_path)

    try:
        gdal_to_tiles(file_path=temp_file_path, save_dir=path)
    except Exception as e:
        print(e)
    finally:
        #os.remove(temp_file_path)
        print(temp_file_path)
        if os.path.exists(path / 'tilemapresource.xml'):
            os.remove(path / 'tilemapresource.xml')


def gdal_to_tiles(file_path: str, save_dir: Path):
    options = {
        'zoom': (MIN_ZOOM, MAX_ZOOM),
        'tile_size': TILE_SIZE,
        'verbose': True,
        's_srs': "EPSG:3857",
        "profile": "raster",
        "webviewer": None,
    }
    gdal2tiles.generate_tiles(input_file=file_path, output_folder=str(save_dir), **options)
