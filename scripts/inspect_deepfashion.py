from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ANNO_PATH = PROJECT_ROOT / "dataset" / "deepfashion" / "Anno"
EVAL_PATH = PROJECT_ROOT / "dataset" / "deepfashion" / "Eval"

CATEGORY_FILE = ANNO_PATH / "list_category_cloth.txt"
IMAGE_CATEGORY_FILE = ANNO_PATH / "list_category_img.txt"
PARTITION_FILE = EVAL_PATH / "list_eval_partition.txt"

print("\nChecking DeepFashion files...\n")

for file in [CATEGORY_FILE, IMAGE_CATEGORY_FILE, PARTITION_FILE]:
    if file.exists():
        print("FOUND:", file)
    else:
        print("MISSING:", file)

print("\n" + "=" * 60)
print("CLOTHING CATEGORIES")
print("=" * 60)

categories = []

with open(CATEGORY_FILE, "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()

    if not line:
        continue

    parts = line.split()

    # Skip header/count lines
    if len(parts) >= 2 and parts[-1].isdigit():
        category_name = " ".join(parts[:-1])
        category_type = int(parts[-1])

        # Avoid count/header lines
        if category_name.lower() not in ["category_name category_type"]:
            categories.append((len(categories) + 1, category_name, category_type))

print("\nID   Category                      Type")
print("-" * 50)

for category_id, category_name, category_type in categories:
    print(f"{category_id:<4} {category_name:<30} {category_type}")

print("\nTotal categories:", len(categories))

category_dict = {
    category_id: category_name
    for category_id, category_name, _ in categories
}

print("\n" + "=" * 60)
print("IMAGE → CATEGORY")
print("=" * 60)

image_data = []

with open(IMAGE_CATEGORY_FILE, "r", encoding="utf-8") as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()

    if not line:
        continue

    parts = line.split()

    if len(parts) == 2:
        image_path = parts[0]

        try:
            category_id = int(parts[1])

            if image_path.startswith("img/"):
                image_data.append((image_path, category_id))

        except ValueError:
            pass

print("Total labelled images:", len(image_data))

print("\nFirst 20 examples:\n")

for image_path, category_id in image_data[:20]:
    category_name = category_dict.get(category_id, "Unknown")
    print(f"{image_path} -> {category_name}")

print("\n" + "=" * 60)
print("IMAGES PER CATEGORY")
print("=" * 60)

category_counts = {}

for _, category_id in image_data:
    category_counts[category_id] = category_counts.get(category_id, 0) + 1

for category_id, count in sorted(category_counts.items()):
    category_name = category_dict.get(category_id, "Unknown")
    print(f"{category_name:<30}: {count}")

df = pd.DataFrame(
    image_data,
    columns=["image_path", "category_id"]
)

df["category"] = df["category_id"].map(category_dict)

output_file = PROJECT_ROOT / "deepfashion_category_mapping.csv"

df.to_csv(output_file, index=False)

print("\nCSV created successfully:")
print(output_file)