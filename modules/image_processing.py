import cv2
import numpy as np
from PIL import Image

def load_image(image_path: str) -> Image.Image:
    return Image.open(image_path).convert("RGB")

def preprocess_image(image: Image.Image, size=(224, 224)) -> np.ndarray:
    image_array = np.array(image)
    return cv2.resize(image_array, size)
