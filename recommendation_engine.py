import pandas as pd


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

# IMPORTANT:
# keep_default_na=False prevents the word "None"
# from being converted into NaN.

df = pd.read_csv(
    "restyle_upcycling_knowledge_base.csv",
    keep_default_na=False
)

print("Knowledge base loaded!")
print("Total recommendations:", len(df))


# ============================================================
# RECOMMENDATION ENGINE
# ============================================================

def get_recommendations(
    clothing_type,
    colour=None,
    condition=None,
    damage_location=None,
    damage_severity=None,
    stain_severity=None,
    hole_severity=None,
    repair_status=None,
    style=None,
    material=None
):

    # --------------------------------------------------------
    # Clean optional values
    # --------------------------------------------------------

    if colour is None:
        colour = ""

    if condition is None:
        condition = ""

    if damage_location is None:
        damage_location = "None"

    if damage_severity is None:
        damage_severity = "None"

    if stain_severity is None:
        stain_severity = "None"

    if hole_severity is None:
        hole_severity = "None"

    if repair_status is None:
        repair_status = ""

    if style is None:
        style = ""

    if material is None:
        material = ""


    # --------------------------------------------------------
    # First filter by clothing type
    # --------------------------------------------------------

    results = df[
        df["clothing_type"].str.lower()
        == clothing_type.lower()
    ].copy()


    if results.empty:
        return results


    # --------------------------------------------------------
    # Create match score
    # --------------------------------------------------------

    results["match_score"] = 0


    # ========================================================
    # IMPORTANT FEATURES
    # ========================================================

    # Clothing type
    results["match_score"] += (
        results["clothing_type"].str.lower()
        == clothing_type.lower()
    ).astype(int) * 30


    # Damage location
    if damage_location:

        results["match_score"] += (
            results["damage_location"].str.lower()
            == damage_location.lower()
        ).astype(int) * 20


    # Damage severity
    if damage_severity:

        results["match_score"] += (
            results["damage_severity"].str.lower()
            == damage_severity.lower()
        ).astype(int) * 15


    # Condition
    if condition:

        results["match_score"] += (
            results["condition"].str.lower()
            == condition.lower()
        ).astype(int) * 10


    # Material
    if material:

        results["match_score"] += (
            results["material"].str.lower()
            == material.lower()
        ).astype(int) * 10


    # Hole severity
    if hole_severity:

        results["match_score"] += (
            results["hole_severity"].str.lower()
            == hole_severity.lower()
        ).astype(int) * 5


    # Stain severity
    if stain_severity:

        results["match_score"] += (
            results["stain_severity"].str.lower()
            == stain_severity.lower()
        ).astype(int) * 5


    # Repair status
    if repair_status:

        results["match_score"] += (
            results["repair_status"].str.lower()
            == repair_status.lower()
        ).astype(int) * 5


    # Style
    if style:

        results["match_score"] += (
            results["style"].str.lower()
            == style.lower()
        ).astype(int) * 3


    # Colour
    if colour:

        results["match_score"] += (
            results["colour"].str.lower()
            == colour.lower()
        ).astype(int) * 2


    # ========================================================
    # SORT BY BEST MATCH
    # ========================================================

    results = results.sort_values(
        by=[
            "match_score",
            "recommendation_priority"
        ],
        ascending=[
            False,
            True
        ]
    )


    # ========================================================
    # REMOVE DUPLICATE RECOMMENDATION TYPES
    # ========================================================

    results = results.drop_duplicates(
        subset=[
            "recommended_action",
            "upcycling_method"
        ]
    )


    # ========================================================
    # RETURN TOP 3
    # ========================================================

    return results.head(3)


# ============================================================
# TEST
# ============================================================

recommendations = get_recommendations(

    clothing_type="Jeans",

    colour="Blue",

    condition="Damaged",

    damage_location="Knee",

    damage_severity="Minor",

    stain_severity="None",

    hole_severity="None",

    repair_status="Needs Repair",

    style="Casual",

    material="Denim"
)


# ============================================================
# DISPLAY
# ============================================================

print()
print("=" * 60)
print("RESTYLE UPCYCLING RECOMMENDATIONS")
print("=" * 60)


if recommendations.empty:

    print()
    print("No recommendation found.")

else:

    for index, (_, row) in enumerate(
        recommendations.iterrows(),
        start=1
    ):

        print()
        print(f"RECOMMENDATION {index}")
        print("-" * 45)

        print(
            "Action:",
            row["recommended_action"]
        )

        print(
            "Method:",
            row["upcycling_method"]
        )

        print(
            "Match Score:",
            row["match_score"]
        )

        print(
            "Difficulty:",
            row["difficulty"]
        )

        print(
            "Reason:",
            row["reason"]
        )

        print(
            "Materials:",
            row["required_materials"]
        )

        print(
            "Estimated Time:",
            row["estimated_time_minutes"],
            "minutes"
        )