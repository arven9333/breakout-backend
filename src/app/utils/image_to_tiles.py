from pathlib import Path
from settings import SRC_DIR
import os
from PIL import Image
import io

MIN_ZOOM = 2
MAX_ZOOM = 5
TILE_SIZE = 512


def generate_tiles(stream: bytes, path: str):

    path = SRC_DIR / path

    with Image.open(io.BytesIO(stream)) as orig_world_map:
        for z in range(MIN_ZOOM, MAX_ZOOM + 1):
            if z == 0:
                print("Zoom level", z, "- Generating", 2 ** z * 2 ** z, "256x256 image")
            else:
                print("Zoom level", z, "- Generating", 2 ** z * 2 ** z, "256x256 images")

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
