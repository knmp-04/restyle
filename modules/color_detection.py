import numpy as np
from sklearn.cluster import KMeans

COLOR_REFERENCES = {
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Grey": (128, 128, 128),
    "Red": (220, 20, 60),
    "Maroon": (128, 0, 0),
    "Green": (0, 128, 0),
    "Olive": (128, 128, 0),
    "Blue": (0, 90, 200),
    "Navy": (0, 0, 128),
    "Sky Blue": (135, 206, 235),
    "Yellow": (255, 215, 0),
    "Orange": (255, 140, 0),
    "Purple": (128, 0, 128),
    "Pink": (255, 105, 180),
    "Brown": (139, 69, 19),
    "Beige": (222, 205, 170),
    "Cream": (255, 253, 208)
}

def get_dominant_color(pixels, k=3, sample_size=15000):
    pixels = np.asarray(pixels)

    if len(pixels) == 0:
        raise ValueError("No pixels supplied for colour detection.")

    if len(pixels) > sample_size:
        rng = np.random.default_rng(42)
        indices = rng.choice(len(pixels), sample_size, replace=False)
        pixels = pixels[indices]

    unique_count = len(np.unique(pixels, axis=0))
    cluster_count = min(k, unique_count)

    if cluster_count < 1:
        raise ValueError("Unable to find enough colour information.")

    kmeans = KMeans(
        n_clusters=cluster_count,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(pixels)
    counts = np.bincount(labels)
    dominant_index = np.argmax(counts)

    return kmeans.cluster_centers_[dominant_index].astype(int)

def get_color_name(rgb):
    rgb = np.asarray(rgb, dtype=float)
    closest_name = None
    minimum_distance = float("inf")

    for name, reference_rgb in COLOR_REFERENCES.items():
        reference_rgb = np.asarray(reference_rgb, dtype=float)
        distance = np.linalg.norm(rgb - reference_rgb)

        if distance < minimum_distance:
            minimum_distance = distance
            closest_name = name

    return closest_name
