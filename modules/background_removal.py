import numpy as np
from PIL import Image
from rembg import remove

def remove_background(image: Image.Image) -> Image.Image:
    return remove(image.convert("RGBA"))

def create_foreground_mask(background_removed: Image.Image):
    rgba_array = np.array(background_removed)
    foreground_rgb = rgba_array[:, :, :3]
    alpha_channel = rgba_array[:, :, 3]
    mask = alpha_channel > 20
    foreground_pixels = foreground_rgb[mask]

    if len(foreground_pixels) == 0:
        raise ValueError("No foreground pixels were detected.")

    return foreground_rgb, mask, foreground_pixels
