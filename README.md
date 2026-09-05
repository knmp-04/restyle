# Restyle Modular Clothing Analysis

Current pipeline:

1. Load clothing image
2. Preprocess/resize image
3. Remove background with rembg
4. Create foreground mask
5. Detect dominant colour with K-Means
6. Detect clothing type using zero-shot CLIP
7. Save the background-removed image

## Project structure

restyle_modular_project/
- app.py
- requirements.txt
- modules/
  - image_processing.py
  - background_removal.py
  - color_detection.py
  - clothing_detection.py
- uploads/
- outputs/

## VS Code setup

Create environment:

python -m venv venv

If PowerShell blocks activation:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Activate:

.\venv\Scripts\Activate.ps1

Install:

python -m pip install --upgrade pip
pip install -r requirements.txt

Put an image in uploads/, for example:

uploads/jeans.jpg

Run:

python app.py uploads/jeans.jpg

The first CLIP run downloads model files. Later runs use the local cache.

## Limitations

- rembg is foreground segmentation, not clothing-specific segmentation.
- If a person is visible, foreground pixels may include skin, hair and other clothes.
- CLIP is zero-shot and has not yet been fine-tuned for Restyle.
- CLIP confidence is relative to the category list, not a guarantee of correctness.

## Planned modules

- pattern_detection.py
- condition_detection.py
- material_analysis.py
- brand_detection.py
- upcycling_engine.py
