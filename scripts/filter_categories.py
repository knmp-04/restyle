from pathlib import Path
import pandas as pd


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MAPPING_FILE = PROJECT_ROOT / "deepfashion_category_mapping.csv"

PARTITION_FILE = (
    PROJECT_ROOT
    / "dataset"
    / "deepfashion"
    / "Eval"
    / "list_eval_partition.txt"
)


# --------------------------------------------------
# Selected Restyle categories
# --------------------------------------------------

SELECTED_CATEGORIES = [
    "Blouse",
    "Hoodie",
    "Jacket",
    "Sweater",
    "Tee",
    "Jeans",
    "Shorts",
    "Skirt",
    "Dress",
    "Jumpsuit"
]


# --------------------------------------------------
# Load category mapping
# --------------------------------------------------

print("\nLoading DeepFashion category mapping...")

df = pd.read_csv(MAPPING_FILE)

print("Total images before filtering:", len(df))


# --------------------------------------------------
# Filter selected categories
# --------------------------------------------------

filtered_df = df[
    df["category"].isin(SELECTED_CATEGORIES)
].copy()


print("\nSelected categories:")

for category in SELECTED_CATEGORIES:

    count = len(
        filtered_df[
            filtered_df["category"] == category
        ]
    )

    print(f"{category:<15}: {count}")


print(
    "\nTotal images after filtering:",
    len(filtered_df)
)


# --------------------------------------------------
# Read train/validation/test partitions
# --------------------------------------------------

print("\nReading dataset partitions...")

partition_data = []

with open(
    PARTITION_FILE,
    "r",
    encoding="utf-8"
) as file:

    for line in file:

        line = line.strip()

        if not line:
            continue

        parts = line.split()

        if len(parts) == 2:

            image_path = parts[0]
            partition = parts[1]

            # Skip header if present
            if partition in [
                "train",
                "val",
                "test"
            ]:

                partition_data.append(
                    (
                        image_path,
                        partition
                    )
                )


partition_df = pd.DataFrame(
    partition_data,
    columns=[
        "image_path",
        "partition"
    ]
)


print(
    "Total partition records:",
    len(partition_df)
)


# --------------------------------------------------
# Merge categories with partitions
# --------------------------------------------------

final_df = filtered_df.merge(
    partition_df,
    on="image_path",
    how="inner"
)


# --------------------------------------------------
# Show partition distribution
# --------------------------------------------------

print("\n" + "=" * 50)
print("PARTITION DISTRIBUTION")
print("=" * 50)

print(
    final_df["partition"]
    .value_counts()
)


print("\nCategory distribution by partition:\n")

print(
    pd.crosstab(
        final_df["category"],
        final_df["partition"]
    )
)


# --------------------------------------------------
# Save final dataset information
# --------------------------------------------------

OUTPUT_FILE = (
    PROJECT_ROOT
    / "restyle_selected_images.csv"
)

final_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n" + "=" * 50)
print("FILTERING COMPLETE")
print("=" * 50)

print("Final dataset records:", len(final_df))

print(
    "\nSaved file:"
)

print(OUTPUT_FILE)

print("\nPreview:")

print(
    final_df.head(10)
)