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

    filename = generate_uuid4_filename(f'temp.png')
    temp_file_path = str(path / filename)

    bytes_img = io.BytesIO(stream)

    if format_str == 'svg':
        with WandImage(blob=bytes_img.read()) as image:
            image.format = 'png'
            image.save(filename=temp_file_path)
    else:
        with Image.open(bytes_img) as orig_world_map:
            orig_world_map.save(temp_file_path)

    try:
        #gdal_to_tiles(file_path=temp_file_path, save_dir=path)
        image_to_tiles(image_path=temp_file_path, tile_dir=path)
    except Exception as e:
        print(e)
    finally:
        #os.remove(temp_file_path)
        print(temp_file_path)
        if os.path.exists(path / 'tilemapresource.xml'):
            os.remove(path / 'tilemapresource.xml')


# def gdal_to_tiles(file_path: str, save_dir: Path):
#     options = {
#         'zoom': (MIN_ZOOM, MAX_ZOOM),
#         'tile_size': TILE_SIZE,
#         'verbose': True,
#         's_srs': "EPSG:xyz",
#         #"profile": "raster",
#         "webviewer": None,
#     }
#     gdal2tiles.generate_tiles(input_file=file_path, output_folder=str(save_dir), **options)

def image_to_tiles(image_path: str, tile_dir: Path):
    with Image.open(image_path) as orig:
        for z in range(MIN_ZOOM, MAX_ZOOM + 1):
            if z == 0:
                print ("Zoom level", z, "- Generating", 2 ** z * 2 ** z, "256x256 image")
            else:
                print ("Zoom level", z, "- Generating", 2 ** z * 2 ** z, "256x256 images")
            for x in range(2 ** z):
                x_val_dir = os.path.join(tile_dir, str(z), str(x))
                if not os.path.exists(x_val_dir):
                    os.makedirs(x_val_dir)
                for y in range(2 ** z):
                    max_val = 1024
                    size = 1024 * (2 ** (-z))
                    assert size == int(size)
                    size = int(size)
                    resized = orig.resize(
                        (256, 256),
                        box=(
                            x * size,
                            y * size,
                            (x + 1) * size - 1,
                            (y + 1) * size - 1,
                        )
                    )
                    resized.save(os.path.join(x_val_dir, str(y) + ".png"))

#image_to_tiles('/home/ven9/edd0cdf5668043a583ebb1b239622fc0.png', './tiles')