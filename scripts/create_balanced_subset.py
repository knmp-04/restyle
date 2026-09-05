from pathlib import Path
import pandas as pd


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "restyle_selected_images.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "restyle_balanced_subset.csv"
)


# --------------------------------------------------
# Configuration
# --------------------------------------------------

RANDOM_STATE = 42

SAMPLES_PER_CATEGORY = {
    "train": 2100,
    "val": 450,
    "test": 450
}


# --------------------------------------------------
# Load filtered dataset
# --------------------------------------------------

print("\nLoading selected DeepFashion records...")

df = pd.read_csv(INPUT_FILE)

print("Total records:", len(df))


# --------------------------------------------------
# Create balanced subset
# --------------------------------------------------

balanced_data = []

categories = sorted(
    df["category"].unique()
)


for category in categories:

    print("\n" + "=" * 50)
    print("Processing:", category)
    print("=" * 50)

    category_df = df[
        df["category"] == category
    ]

    for partition, required_samples in (
        SAMPLES_PER_CATEGORY.items()
    ):

        partition_df = category_df[
            category_df["partition"] == partition
        ]

        available = len(partition_df)

        print(
            f"{partition:<6} "
            f"Available: {available:<6} "
            f"Selected: {required_samples}"
        )

        # Check sufficient images are available
        if available < required_samples:

            print(
                f"WARNING: {category} does not have "
                f"enough {partition} images."
            )

            # Use all available images
            sampled_df = partition_df

        else:

            sampled_df = partition_df.sample(
                n=required_samples,
                random_state=RANDOM_STATE
            )

        balanced_data.append(sampled_df)


# --------------------------------------------------
# Combine all categories
# --------------------------------------------------

balanced_df = pd.concat(
    balanced_data,
    ignore_index=True
)


# --------------------------------------------------
# Shuffle dataset
# --------------------------------------------------

balanced_df = balanced_df.sample(
    frac=1,
    random_state=RANDOM_STATE
).reset_index(drop=True)


# --------------------------------------------------
# Save result
# --------------------------------------------------

balanced_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\n" + "=" * 60)
print("BALANCED DATASET CREATED")
print("=" * 60)

print(
    "\nTotal selected images:",
    len(balanced_df)
)

print("\nPartition distribution:")

print(
    balanced_df["partition"]
    .value_counts()
)

print("\nImages per category:")

print(
    balanced_df["category"]
    .value_counts()
    .sort_index()
)

print("\nCategory × Partition:")

print(
    pd.crosstab(
        balanced_df["category"],
        balanced_df["partition"]
    )
)

print(
    "\nSaved to:"
)

print(OUTPUT_FILE)