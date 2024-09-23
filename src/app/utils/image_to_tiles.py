from settings import SRC_DIR
import os
from wand.image import Image as WandImage
from PIL import Image
import io

MIN_ZOOM = 2
MAX_ZOOM = 5
TILE_SIZE = 512


def generate_tiles(stream: bytes, path: str, format_str: str):
    path = SRC_DIR / path

    bytes_img = io.BytesIO(stream)
    bytes_img.seek(0)

    if format_str == 'svg':
        with WandImage(blob=bytes_img.read(), format="svg") as image:
            png_image = image.make_blob("png")
            bytes_img = io.BytesIO(png_image)
            bytes_img.seek(0)

    with Image.open(bytes_img) as orig_world_map:
        for z in range(MIN_ZOOM, MAX_ZOOM + 1):
            tiles_per_dimension = 2 ** z

            zoomed_world_map = orig_world_map.resize((
                tiles_per_dimension * TILE_SIZE,
                tiles_per_dimension * TILE_SIZE,
            ))
            for x in range(tiles_per_dimension):

                x_val_dir = path / str(z) / str(x)
                if not os.path.exists(x_val_dir):
                    os.makedirs(x_val_dir)
                for y in range(tiles_per_dimension):
                    cropped = zoomed_world_map.crop((
                        x * TILE_SIZE,
                        y * TILE_SIZE,
                        (x + 1) * TILE_SIZE - 1,
                        (y + 1) * TILE_SIZE - 1,
                    ))
                    cropped.save(x_val_dir / (str(y) + ".png"))
