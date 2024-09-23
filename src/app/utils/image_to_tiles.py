from pathlib import Path

from wand.api import library
from wand.color import Color as WandColor
from wand.image import Image as WandImage

from settings import SRC_DIR
import os
from utils.file_operations import generate_uuid4_filename, create_dirs

from PIL import Image
import io
import gdal2tiles

MIN_ZOOM = 2
MAX_ZOOM = 5
TILE_SIZE = 256


def generate_tiles(stream: bytes, path: str, format_str: str):
    path = SRC_DIR / path

    create_dirs(path)

    with open(path / 'test.svg', 'wb') as file:
        file.write(stream)
        print(path / 'test.svg', "СОХРАНЕНО SVG")

    filename = generate_uuid4_filename(f'temp.png')
    temp_file_path = str(path / filename)

    bytes_img = io.BytesIO(stream)
    bytes_img.seek(0)

    if format_str == 'svg':
        with WandImage() as image:
            with WandColor('transparent') as background_color:
                library.MagickSetBackgroundColor(image.wand,
                                                 background_color.resource)
            image.read(blob=bytes_img.read(), format="svg")

            png_image = image.make_blob("png32")
            bytes_img = io.BytesIO(png_image)

    with Image.open(bytes_img) as orig_world_map:
        orig_world_map.save(temp_file_path)
        print(temp_file_path, "СОХРАНИЛ ВРЕМЕННЫЙ ФАЙЛ")

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
