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
    print(temp_file_path)
    return
    try:
        gdal_to_tiles(file_path=temp_file_path, save_dir=path)
        #image_to_tiles(image_path=temp_file_path, tile_dir='./tiles')
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


def image_to_tiles(image_path: str, tile_dir: Path):
    with Image.open(image_path) as orig_world_map:
        for z in range(MIN_ZOOM, MAX_ZOOM + 1):
            if z == 0:
                print("Zoom level", z, "- Generating", 2 ** z * 2 ** z, "256x256 image")
            else:
                print("Zoom level", z, "- Generating", 2 ** z * 2 ** z, "256x256 images")

            tiles_per_dimension = 2 ** z
            # Zoom the world map to be big enough for the number of tiles given the size of the tiles
            zoomed_world_map = orig_world_map.resize((
                tiles_per_dimension * TILE_SIZE,
                tiles_per_dimension * TILE_SIZE,
            ))
            for x in range(tiles_per_dimension):
                x_val_dir = os.path.join(tile_dir, str(z), str(x))
                if not os.path.exists(x_val_dir):
                    os.makedirs(x_val_dir)
                for y in range(tiles_per_dimension):
                    cropped = zoomed_world_map.crop((
                        x * TILE_SIZE,
                        y * TILE_SIZE,
                        (x + 1) * TILE_SIZE - 1,
                        (y + 1) * TILE_SIZE - 1,
                    ))
                    cropped.save(os.path.join(x_val_dir, str(y) + ".png"))


#image_to_tiles('/home/ven9/edd0cdf5668043a583ebb1b239622fc0.png', './tiles')
#image_to_tiles('/home/ven9/edd0cdf5668043a583ebb1b239622fc0.png', './tiles')
#gdal_to_tiles('/home/ven9/projects/Ilkhom/tarkov_fixed/breakout-backend/src/images/maps/4/102/tiles/ecb216f6cb8a482483da3a6bea112dcf.png', './tiles')
