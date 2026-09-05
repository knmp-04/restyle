import pandas as pd


# Load knowledge base
df = pd.read_csv("restyle_upcycling_knowledge_base.csv")

print("Knowledge base loaded!")
print("Total recommendations:", len(df))


def get_recommendations(
    clothing_type,
    colour,
    condition,
    damage_location,
    damage_severity,
    stain_severity,
    hole_severity,
    repair_status,
    style,
    material
):

    results = df[
        (df["clothing_type"] == clothing_type) &
        (df["colour"] == colour) &
        (df["condition"] == condition) &
        (df["damage_location"] == damage_location) &
        (df["damage_severity"] == damage_severity) &
        (df["stain_severity"] == stain_severity) &
        (df["hole_severity"] == hole_severity) &
        (df["repair_status"] == repair_status) &
        (df["style"] == style) &
        (df["material"] == material)
    ]

    # Sort by recommendation priority
    results = results.sort_values(
        by="recommendation_priority"
    )

    return results


# ---------------------------------------------------------
# TEST INPUT
# ---------------------------------------------------------

recommendations = get_recommendations(
    clothing_type="Jeans",
    colour="Blue",
    condition="Damaged",
    damage_location="Knee",
    damage_severity="Minor",
    stain_severity="None",
    hole_severity="Minor",
    repair_status="Needs Repair",
    style="Casual",
    material="Denim"
)


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

if recommendations.empty:

    print()
    print("No exact recommendation found.")

else:

    print()
    print("RECOMMENDATIONS")
    print("-" * 50)

    for _, row in recommendations.head(3).iterrows():

        print()
        print("Action:", row["recommended_action"])
        print("Method:", row["upcycling_method"])
        print("Difficulty:", row["difficulty"])
        print("Reason:", row["reason"])
        print(
            "Required materials:",
            row["required_materials"]
        )
        print(
            "Estimated time:",
            row["estimated_time_minutes"],
            "minutes"
        )