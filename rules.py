"""
RESTYLE - Intelligent Wardrobe Utilization System

Generate a rule-based upcycling recommendation knowledge base.

IMPORTANT:
This is a KNOWLEDGE BASE generated from explicit transformation rules.
It is NOT 30,000 independent real-world observations.

The CSV can be used by the Restyle recommendation engine after the
system identifies:
    - clothing type
    - colour
    - condition
    - damage location
    - damage severity
    - stains
    - holes
    - repair status
    - style
    - material
"""

import csv
from itertools import product
from pathlib import Path


# ============================================================
# SETTINGS
# ============================================================

TARGET_ROWS = 30000
MIN_ROWS = 20000
MAX_ROWS = 40000

OUTPUT_FILE = "restyle_upcycling_knowledge_base.csv"


# ============================================================
# POSSIBLE INPUT VALUES
# ============================================================

COLORS = [
    "Black",
    "White",
    "Blue",
    "Navy",
    "Grey",
    "Red",
    "Green",
    "Yellow",
    "Pink",
    "Brown",
    "Beige",
    "Multicolor"
]

STYLES = [
    "Casual",
    "Formal",
    "Sporty",
    "Traditional",
    "Oversized",
    "Vintage"
]

CONDITIONS = [
    "Excellent",
    "Good",
    "Worn",
    "Damaged",
    "Severely Damaged"
]

STAIN_LEVELS = [
    "None",
    "Minor",
    "Major"
]

HOLE_LEVELS = [
    "None",
    "Minor",
    "Major"
]


# ============================================================
# MATERIALS BY CLOTHING TYPE
# ============================================================

MATERIALS = {

    "T-shirt": [
        "Cotton",
        "Polyester",
        "Cotton Blend"
    ],

    "Polo Shirt": [
        "Cotton",
        "Polyester",
        "Cotton Blend"
    ],

    "Tank Top": [
        "Cotton",
        "Polyester",
        "Cotton Blend"
    ],

    "Crop Top": [
        "Cotton",
        "Polyester",
        "Cotton Blend"
    ],

    "Shirt": [
        "Cotton",
        "Linen",
        "Polyester",
        "Cotton Blend"
    ],

    "Blouse": [
        "Cotton",
        "Polyester",
        "Silk",
        "Viscose"
    ],

    "Tunic": [
        "Cotton",
        "Viscose",
        "Linen"
    ],

    "Kurta": [
        "Cotton",
        "Linen",
        "Viscose",
        "Silk"
    ],

    "Kurti": [
        "Cotton",
        "Viscose",
        "Rayon",
        "Linen"
    ],

    "Sweater": [
        "Wool",
        "Acrylic",
        "Cotton Blend"
    ],

    "Cardigan": [
        "Wool",
        "Acrylic",
        "Cotton Blend"
    ],

    "Hoodie": [
        "Cotton",
        "Polyester",
        "Cotton Blend"
    ],

    "Sweatshirt": [
        "Cotton",
        "Polyester",
        "Cotton Blend"
    ],

    "Jacket": [
        "Polyester",
        "Cotton",
        "Nylon",
        "Cotton Blend"
    ],

    "Denim Jacket": [
        "Denim",
        "Cotton Blend"
    ],

    "Blazer": [
        "Wool Blend",
        "Polyester",
        "Cotton Blend"
    ],

    "Coat": [
        "Wool",
        "Wool Blend",
        "Polyester"
    ],

    "Jeans": [
        "Denim",
        "Cotton Blend"
    ],

    "Trousers": [
        "Cotton",
        "Polyester",
        "Wool Blend",
        "Viscose"
    ],

    "Pants": [
        "Cotton",
        "Polyester",
        "Cotton Blend"
    ],

    "Chinos": [
        "Cotton",
        "Cotton Blend"
    ],

    "Leggings": [
        "Polyester",
        "Nylon",
        "Cotton Blend"
    ],

    "Shorts": [
        "Denim",
        "Cotton",
        "Polyester",
        "Cotton Blend"
    ],

    "Skirt": [
        "Cotton",
        "Denim",
        "Polyester",
        "Viscose"
    ],

    "Maxi Skirt": [
        "Cotton",
        "Viscose",
        "Polyester"
    ],

    "Mini Skirt": [
        "Denim",
        "Cotton",
        "Polyester"
    ],

    "Dress": [
        "Cotton",
        "Polyester",
        "Viscose",
        "Silk"
    ],

    "Jumpsuit": [
        "Cotton",
        "Denim",
        "Polyester",
        "Viscose"
    ],

    "Romper": [
        "Cotton",
        "Polyester",
        "Viscose"
    ],

    "Saree": [
        "Cotton",
        "Silk",
        "Polyester",
        "Viscose"
    ],

    "Dupatta": [
        "Cotton",
        "Silk",
        "Viscose",
        "Polyester"
    ],

    "Scarf": [
        "Cotton",
        "Wool",
        "Silk",
        "Polyester"
    ],

    "Shawl": [
        "Wool",
        "Acrylic",
        "Cotton"
    ],

    "Denim Shirt": [
        "Denim",
        "Cotton Blend"
    ],

    "Track Pants": [
        "Polyester",
        "Cotton",
        "Cotton Blend"
    ],

    "Sweatpants": [
        "Cotton",
        "Polyester",
        "Cotton Blend"
    ],

    "Palazzo Pants": [
        "Cotton",
        "Viscose",
        "Polyester"
    ],

    "Cargo Pants": [
        "Cotton",
        "Cotton Blend",
        "Polyester"
    ]
}


# ============================================================
# CSV COLUMNS
# ============================================================

FIELDS = [
    "recommendation_id",
    "rule_id",
    "clothing_type",
    "colour",
    "condition",
    "damage_location",
    "damage_severity",
    "stain_severity",
    "hole_severity",
    "repair_status",
    "style",
    "material",
    "recommended_action",
    "upcycling_method",
    "difficulty",
    "reason",
    "required_materials",
    "estimated_time_minutes",
    "recommendation_priority",
    "rule_basis"
]


# ============================================================
# RULES
# ============================================================
#
# Format:
#
# (
#     rule_id,
#     clothing_types,
#     damage_locations,
#     damage_levels,
#     conditions,
#     recommended_action,
#     upcycling_method,
#     difficulty,
#     reason,
#     required_materials,
#     estimated_time,
#     priority
# )
#
# ============================================================

RULES = [

    # --------------------------------------------------------
    # JEANS
    # --------------------------------------------------------

    (
        "J01",
        ["Jeans"],
        ["Bottom", "Hem", "Leg"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Convert into denim shorts",
        "Shortening",
        "Easy",
        "The lower portion can be removed while preserving usable denim.",
        "Scissors, measuring tape, sewing machine or needle and thread",
        45,
        1
    ),

    (
        "J02",
        ["Jeans"],
        ["Knee", "Thigh", "Seat"],
        ["Minor"],
        ["Worn", "Damaged"],
        "Apply visible patches",
        "Visible mending",
        "Easy",
        "Localized minor damage can be strengthened and redesigned with a patch.",
        "Denim patch, thread, needle or sewing machine",
        30,
        1
    ),

    (
        "J03",
        ["Jeans"],
        ["Pocket", "Waist"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Reuse usable denim sections for an accessory",
        "Material reuse",
        "Medium",
        "Undamaged denim sections can be recovered for smaller products.",
        "Scissors, thread, needle or sewing machine",
        90,
        2
    ),

    (
        "J04",
        ["Jeans"],
        ["Multiple Areas"],
        ["Major"],
        ["Damaged", "Severely Damaged"],
        "Create denim patchwork",
        "Patchwork",
        "Medium",
        "Multiple damaged areas make patchwork more practical than a full garment redesign.",
        "Scissors, denim scraps, thread and sewing machine",
        180,
        1
    ),

    # --------------------------------------------------------
    # T-SHIRT FAMILY
    # --------------------------------------------------------

    (
        "T01",
        ["T-shirt", "Polo Shirt", "Tank Top", "Crop Top"],
        ["Sleeve", "Cuff", "Shoulder"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Redesign into a sleeveless top",
        "Sleeve removal",
        "Easy",
        "Removing a damaged sleeve can preserve the main body of the garment.",
        "Scissors, measuring tape, needle and thread",
        40,
        1
    ),

    (
        "T02",
        ["T-shirt", "Polo Shirt", "Tank Top", "Crop Top"],
        ["Bottom", "Hem"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Crop and finish the lower edge",
        "Cropping",
        "Easy",
        "A damaged lower edge can be removed and the garment shortened.",
        "Scissors, measuring tape, needle and thread",
        30,
        1
    ),

    (
        "T03",
        ["T-shirt", "Polo Shirt", "Tank Top", "Crop Top"],
        ["Front", "Back"],
        ["Minor"],
        ["Worn", "Damaged"],
        "Cover the damaged area with an appliqué or patch",
        "Appliqué",
        "Easy",
        "A localized damaged area can be covered while adding a decorative element.",
        "Fabric patch, fabric adhesive or thread",
        30,
        1
    ),

    (
        "T04",
        ["T-shirt"],
        ["Multiple Areas"],
        ["Major"],
        ["Damaged", "Severely Damaged"],
        "Recover usable fabric for small accessories",
        "Fabric recovery",
        "Medium",
        "When the shirt is heavily damaged, intact fabric can still be reused.",
        "Scissors, thread and sewing supplies",
        90,
        1
    ),

    # --------------------------------------------------------
    # SHIRT / BLOUSE / KURTA FAMILY
    # --------------------------------------------------------

    (
        "S01",
        ["Shirt", "Blouse", "Denim Shirt", "Tunic", "Kurta", "Kurti"],
        ["Sleeve", "Cuff"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Convert into a sleeveless top",
        "Sleeve removal",
        "Medium",
        "Removing damaged sleeves can retain the main body of the garment.",
        "Scissors, thread, needle or sewing machine",
        60,
        1
    ),

    (
        "S02",
        ["Shirt", "Blouse", "Denim Shirt", "Tunic", "Kurta", "Kurti"],
        ["Collar"],
        ["Minor"],
        ["Worn", "Damaged"],
        "Replace or redesign the collar",
        "Collar redesign",
        "Medium",
        "A damaged collar can be replaced or converted into a new neckline.",
        "Replacement fabric, interfacing, thread and sewing tools",
        75,
        1
    ),

    (
        "S03",
        ["Shirt", "Blouse", "Denim Shirt", "Tunic", "Kurta", "Kurti"],
        ["Front", "Back"],
        ["Minor"],
        ["Worn", "Damaged"],
        "Add a decorative fabric panel or appliqué",
        "Panel insertion",
        "Medium",
        "A localized damaged area can be reinforced and visually redesigned.",
        "Fabric panel, thread, needle or sewing machine",
        60,
        2
    ),

    (
        "S04",
        ["Shirt", "Blouse", "Denim Shirt", "Tunic", "Kurta", "Kurti"],
        ["Multiple Areas"],
        ["Major"],
        ["Damaged", "Severely Damaged"],
        "Recover intact fabric sections for smaller products",
        "Material recovery",
        "Medium",
        "Heavily damaged garments can still provide usable fabric pieces.",
        "Scissors, measuring tape and sewing supplies",
        120,
        1
    ),

    # --------------------------------------------------------
    # DRESSES
    # --------------------------------------------------------

    (
        "D01",
        ["Dress"],
        ["Bottom", "Hem"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Shorten the dress and refinish the hem",
        "Length alteration",
        "Easy",
        "A damaged lower edge can be removed while retaining the upper garment.",
        "Scissors, measuring tape and sewing tools",
        60,
        1
    ),

    (
        "D02",
        ["Dress"],
        ["Sleeve", "Shoulder"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Redesign into a sleeveless dress",
        "Sleeve removal",
        "Medium",
        "Removing damaged sleeves can preserve the dress body.",
        "Scissors, thread, needle or sewing machine",
        75,
        1
    ),

    (
        "D03",
        ["Dress"],
        ["Multiple Areas"],
        ["Major"],
        ["Damaged", "Severely Damaged"],
        "Recover usable fabric for a skirt or accessories",
        "Fabric recovery",
        "Medium",
        "Intact sections can be separated from damaged areas and reused.",
        "Scissors, measuring tape and sewing supplies",
        120,
        1
    ),

    # --------------------------------------------------------
    # SKIRTS
    # --------------------------------------------------------

    (
        "SK01",
        ["Skirt", "Maxi Skirt", "Mini Skirt"],
        ["Bottom", "Hem"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Shorten and refinish the skirt",
        "Length alteration",
        "Easy",
        "Damaged lower fabric can be removed and the hem reconstructed.",
        "Scissors, measuring tape and sewing tools",
        45,
        1
    ),

    (
        "SK02",
        ["Skirt", "Maxi Skirt", "Mini Skirt"],
        ["Waist"],
        ["Minor"],
        ["Worn", "Damaged"],
        "Replace or reinforce the waistband",
        "Waistband repair",
        "Medium",
        "A damaged waistband can be repaired without replacing the entire garment.",
        "Elastic or waistband fabric, thread and sewing tools",
        60,
        1
    ),

    # --------------------------------------------------------
    # JACKETS / OUTERWEAR
    # --------------------------------------------------------

    (
        "O01",
        ["Jacket", "Denim Jacket", "Blazer", "Coat"],
        ["Sleeve", "Cuff", "Elbow"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Convert into a sleeveless vest",
        "Sleeve removal",
        "Medium",
        "Removing damaged sleeves can create a wearable vest from the main body.",
        "Scissors, thread and sewing machine",
        90,
        1
    ),

    (
        "O02",
        ["Jacket", "Denim Jacket", "Blazer", "Coat"],
        ["Pocket", "Front"],
        ["Minor"],
        ["Worn", "Damaged"],
        "Add a decorative patch or pocket redesign",
        "Patch or pocket redesign",
        "Medium",
        "A localized damaged area can be reinforced while adding a functional feature.",
        "Patch fabric, thread and sewing tools",
        60,
        1
    ),

    (
        "O03",
        ["Jacket", "Denim Jacket", "Blazer", "Coat"],
        ["Multiple Areas"],
        ["Major"],
        ["Damaged", "Severely Damaged"],
        "Recover usable panels for accessories",
        "Material recovery",
        "Medium",
        "Intact outerwear panels can be reused when the full garment is no longer practical.",
        "Scissors, measuring tape and sewing supplies",
        150,
        1
    ),

    # --------------------------------------------------------
    # HOODIES / SWEATERS
    # --------------------------------------------------------

    (
        "K01",
        ["Hoodie", "Sweatshirt", "Sweater", "Cardigan"],
        ["Sleeve", "Cuff", "Elbow"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Convert into a sleeveless vest",
        "Sleeve removal",
        "Medium",
        "Removing damaged sleeves can preserve the central body and create a vest.",
        "Scissors, thread and sewing tools",
        75,
        1
    ),

    (
        "K02",
        ["Hoodie", "Sweatshirt", "Sweater", "Cardigan"],
        ["Front", "Back"],
        ["Minor"],
        ["Worn", "Damaged"],
        "Add a fabric patch or decorative panel",
        "Patchwork",
        "Easy",
        "A patch can reinforce localized damage and extend garment life.",
        "Fabric patch, thread or fabric adhesive",
        35,
        1
    ),

    (
        "K03",
        ["Hoodie", "Sweatshirt", "Sweater", "Cardigan"],
        ["Multiple Areas"],
        ["Major"],
        ["Damaged", "Severely Damaged"],
        "Recover intact fabric for accessories",
        "Fabric recovery",
        "Medium",
        "Usable sections can be separated from heavily damaged areas.",
        "Scissors, thread and sewing supplies",
        100,
        1
    ),

    # --------------------------------------------------------
    # TROUSERS / PANTS
    # --------------------------------------------------------

    (
        "P01",
        [
            "Trousers",
            "Pants",
            "Chinos",
            "Track Pants",
            "Sweatpants",
            "Palazzo Pants",
            "Cargo Pants"
        ],
        ["Bottom", "Leg", "Hem"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Convert into shorts",
        "Shortening",
        "Easy",
        "Damaged lower sections can be removed to preserve the upper garment.",
        "Scissors, measuring tape and sewing tools",
        45,
        1
    ),

    (
        "P02",
        [
            "Trousers",
            "Pants",
            "Chinos",
            "Track Pants",
            "Sweatpants",
            "Palazzo Pants",
            "Cargo Pants"
        ],
        ["Knee", "Thigh", "Seat"],
        ["Minor"],
        ["Worn", "Damaged"],
        "Repair and reinforce with a patch",
        "Visible mending",
        "Easy",
        "Localized damage can be reinforced instead of discarding the garment.",
        "Fabric patch, thread, needle or sewing machine",
        40,
        1
    ),

    # --------------------------------------------------------
    # LEGGINGS
    # --------------------------------------------------------

    (
        "L01",
        ["Leggings"],
        ["Bottom", "Leg"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Convert into shorter leggings",
        "Length alteration",
        "Easy",
        "Damaged lower sections can be removed while retaining usable fabric.",
        "Scissors, measuring tape and sewing tools",
        30,
        1
    ),

    (
        "L02",
        ["Leggings"],
        ["Multiple Areas"],
        ["Major"],
        ["Damaged", "Severely Damaged"],
        "Recover fabric for small textile accessories",
        "Material recovery",
        "Medium",
        "Intact sections may still be useful for smaller textile products.",
        "Scissors and sewing supplies",
        75,
        1
    ),

    # --------------------------------------------------------
    # SHORTS
    # --------------------------------------------------------

    (
        "SH01",
        ["Shorts"],
        ["Hem", "Bottom"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Refinish or redesign the hem",
        "Hem redesign",
        "Easy",
        "The damaged edge can be reconstructed without replacing the whole garment.",
        "Scissors, thread and sewing tools",
        30,
        1
    ),

    # --------------------------------------------------------
    # JUMPSUIT / ROMPER
    # --------------------------------------------------------

    (
        "R01",
        ["Jumpsuit", "Romper"],
        ["Bottom", "Leg"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Convert into a shorter romper or playsuit",
        "Length alteration",
        "Medium",
        "Removing damaged lower sections can preserve the upper garment structure.",
        "Scissors, measuring tape and sewing tools",
        90,
        1
    ),

    (
        "R02",
        ["Jumpsuit", "Romper"],
        ["Sleeve", "Shoulder"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Redesign into a sleeveless style",
        "Sleeve removal",
        "Medium",
        "Damaged sleeves can be removed while preserving the main garment.",
        "Scissors, thread and sewing tools",
        75,
        1
    ),

    # --------------------------------------------------------
    # SAREE / DUPATTA / SCARF / SHAWL
    # --------------------------------------------------------

    (
        "SA01",
        ["Saree", "Dupatta", "Scarf", "Shawl"],
        ["Edge", "Bottom", "Hem"],
        ["Minor", "Major"],
        ["Worn", "Damaged"],
        "Trim the damaged edge and create a smaller accessory",
        "Edge recovery",
        "Medium",
        "A damaged edge can be removed while preserving a large amount of usable fabric.",
        "Scissors, measuring tape and finishing thread",
        60,
        1
    ),

    (
        "SA02",
        ["Saree", "Dupatta", "Scarf", "Shawl"],
        ["Multiple Areas"],
        ["Major"],
        ["Damaged", "Severely Damaged"],
        "Recover intact fabric for accessories or patchwork",
        "Fabric recovery",
        "Medium",
        "Intact sections can be separated and reused when the original item is heavily damaged.",
        "Scissors, measuring tape and sewing supplies",
        120,
        1
    )
]


# ============================================================
# VALIDATION
# ============================================================

def is_valid(row):
    """
    Check whether a generated record makes logical sense.
    """

    # Damage must have a location.
    if row["damage_severity"] != "None":
        if row["damage_location"] == "None":
            return False

    # No damage should have no damage location.
    if row["damage_severity"] == "None":
        if row["damage_location"] != "None":
            return False

    # Excellent clothing should not have major damage.
    if row["condition"] == "Excellent":
        if row["damage_severity"] != "None":
            return False

    # Major hole requires major damage.
    if row["hole_severity"] == "Major":
        if row["damage_severity"] != "Major":
            return False

    # Severe damage should lead to material recovery.
    if row["condition"] == "Severely Damaged":
        if row["upcycling_method"] not in [
            "Material recovery",
            "Fabric recovery"
        ]:
            return False

    # No Repair cannot be used for unresolved damage.
    if row["repair_status"] == "No Repair":

        if row["damage_severity"] != "None":
            return False

        if row["hole_severity"] != "None":
            return False

    return True


# ============================================================
# CREATE A ROW
# ============================================================

def create_row(
    rule_id,
    clothing_type,
    colour,
    condition,
    damage_location,
    damage_severity,
    stain_severity,
    hole_severity,
    repair_status,
    style,
    material,
    action,
    method,
    difficulty,
    reason,
    materials,
    minutes,
    priority
):

    return {
        "recommendation_id": None,

        "rule_id": rule_id,

        "clothing_type": clothing_type,

        "colour": colour,

        "condition": condition,

        "damage_location": damage_location,

        "damage_severity": damage_severity,

        "stain_severity": stain_severity,

        "hole_severity": hole_severity,

        "repair_status": repair_status,

        "style": style,

        "material": material,

        "recommended_action": action,

        "upcycling_method": method,

        "difficulty": difficulty,

        "reason": reason,

        "required_materials": materials,

        "estimated_time_minutes": minutes,

        "recommendation_priority": priority,

        "rule_basis":
            "Rule-based circular fashion/upcycling transformation"
    }


# ============================================================
# GENERATE DAMAGE-BASED RECORDS
# ============================================================

def generate_damage_records():

    rows = []

    print("Generating damage-based recommendations...")

    for rule in RULES:

        (
            rule_id,
            clothing_types,
            locations,
            damage_levels,
            conditions,
            action,
            method,
            difficulty,
            reason,
            required_materials,
            estimated_time,
            priority
        ) = rule

        for clothing_type in clothing_types:

            material_options = MATERIALS[clothing_type]

            for (
                location,
                damage,
                condition,
                colour,
                style,
                material
            ) in product(
                locations,
                damage_levels,
                conditions,
                COLORS,
                STYLES,
                material_options
            ):

                # ------------------------------------------------
                # Stain options
                # ------------------------------------------------

                if damage == "Major":

                    stain_options = [
                        "None",
                        "Minor",
                        "Major"
                    ]

                else:

                    stain_options = [
                        "None",
                        "Minor"
                    ]

                # ------------------------------------------------
                # Hole options
                # ------------------------------------------------

                if damage == "Major":

                    hole_options = [
                        "None",
                        "Minor",
                        "Major"
                    ]

                else:

                    hole_options = [
                        "None",
                        "Minor"
                    ]

                for stain, hole in product(
                    stain_options,
                    hole_options
                ):

                    # ------------------------------------------------
                    # Repair status
                    # ------------------------------------------------

                    has_problem = (
                        damage != "None"
                        or stain != "None"
                        or hole != "None"
                    )

                    if has_problem:

                        repair_options = [
                            "Needs Repair",
                            "Previously Repaired"
                        ]

                    else:

                        repair_options = [
                            "No Repair",
                            "Previously Repaired"
                        ]

                    for repair_status in repair_options:

                        row = create_row(
                            rule_id,
                            clothing_type,
                            colour,
                            condition,
                            location,
                            damage,
                            stain,
                            hole,
                            repair_status,
                            style,
                            material,
                            action,
                            method,
                            difficulty,
                            reason,
                            required_materials,
                            estimated_time,
                            priority
                        )

                        if is_valid(row):

                            rows.append(row)

    return rows


# ============================================================
# NORMAL / NO-DAMAGE RESTYLING RULES
# ============================================================

def generate_normal_records():

    rows = []

    normal_rules = [

        (
            "N01",
            [
                "T-shirt",
                "Polo Shirt",
                "Tank Top"
            ],
            "Convert into a reusable fabric tote",
            "Tote conversion",
            "Easy",
            "A usable knit top can be repurposed into a simple reusable bag.",
            "Scissors, thread and sewing supplies",
            60
        ),

        (
            "N02",
            [
                "Shirt",
                "Blouse",
                "Denim Shirt"
            ],
            "Convert into a reusable fabric tote",
            "Tote conversion",
            "Easy",
            "A button-up garment can be repurposed while retaining useful fabric.",
            "Scissors, thread and sewing supplies",
            75
        ),

        (
            "N03",
            [
                "Jeans",
                "Denim Jacket"
            ],
            "Create a small denim accessory from unused fabric sections",
            "Denim reuse",
            "Medium",
            "Denim provides durable fabric suitable for smaller accessories.",
            "Scissors, denim fabric, thread and sewing tools",
            90
        ),

        (
            "N04",
            [
                "Saree",
                "Dupatta",
                "Scarf",
                "Shawl"
            ],
            "Create a smaller accessory from the existing fabric",
            "Accessory conversion",
            "Medium",
            "Large textile pieces can be redesigned into smaller useful accessories.",
            "Scissors, measuring tape and finishing supplies",
            60
        ),

        (
            "N05",
            [
                "Dress",
                "Skirt",
                "Kurta",
                "Kurti"
            ],
            "Redesign the silhouette through length alteration",
            "Silhouette redesign",
            "Medium",
            "A usable garment can receive a new silhouette instead of being discarded.",
            "Scissors, measuring tape and sewing supplies",
            75
        )
    ]

    print("Generating normal-garment restyling recommendations...")

    for (
        rule_id,
        clothing_types,
        action,
        method,
        difficulty,
        reason,
        materials,
        minutes
    ) in normal_rules:

        for clothing_type in clothing_types:

            for (
                colour,
                style,
                material,
                condition
            ) in product(
                COLORS,
                STYLES,
                MATERIALS[clothing_type],
                [
                    "Excellent",
                    "Good",
                    "Worn"
                ]
            ):

                if condition == "Worn":

                    repair_status = "Previously Repaired"

                else:

                    repair_status = "No Repair"

                row = create_row(
                    rule_id,
                    clothing_type,
                    colour,
                    condition,
                    "None",
                    "None",
                    "None",
                    "None",
                    repair_status,
                    style,
                    material,
                    action,
                    method,
                    difficulty,
                    reason,
                    materials,
                    minutes,
                    2
                )

                if is_valid(row):

                    rows.append(row)

    return rows


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(rows):

    print("Removing duplicate records...")

    seen = set()

    unique_rows = []

    for row in rows:

        key = tuple(
            row[field]
            for field in FIELDS
            if field != "recommendation_id"
        )

        if key not in seen:

            seen.add(key)

            unique_rows.append(row)

    return unique_rows


# ============================================================
# BALANCE DATASET
# ============================================================

def balance_dataset(rows):

    print("Balancing dataset...")

    if len(rows) < MIN_ROWS:

        raise RuntimeError(
            f"Only {len(rows):,} valid records were generated. "
            f"At least {MIN_ROWS:,} are required."
        )

    # Group records by rule.
    groups = {}

    for row in rows:

        rule_id = row["rule_id"]

        if rule_id not in groups:

            groups[rule_id] = []

        groups[rule_id].append(row)

    rule_ids = sorted(groups.keys())

    selected = []

    position = 0

    # Round-robin selection prevents one rule from dominating.
    while len(selected) < TARGET_ROWS:

        added_this_round = False

        for rule_id in rule_ids:

            if position < len(groups[rule_id]):

                selected.append(
                    groups[rule_id][position]
                )

                added_this_round = True

                if len(selected) >= TARGET_ROWS:

                    break

        if not added_this_round:

            break

        position += 1

    if len(selected) < MIN_ROWS:

        raise RuntimeError(
            f"Balanced dataset contains only "
            f"{len(selected):,} records."
        )

    return selected


# ============================================================
# ASSIGN RECOMMENDATION IDs
# ============================================================

def assign_ids(rows):

    for index, row in enumerate(rows, start=1):

        row["recommendation_id"] = (
            f"REC{index:06d}"
        )

    return rows


# ============================================================
# SAVE CSV
# ============================================================

def save_csv(rows):

    output_path = Path(OUTPUT_FILE)

    print("Saving CSV...")

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS
        )

        writer.writeheader()

        writer.writerows(rows)

    return output_path


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print()
    print("=" * 70)
    print("RESTYLE UPSCYCLING KNOWLEDGE BASE GENERATOR")
    print("=" * 70)

    # --------------------------------------------------------
    # Generate records
    # --------------------------------------------------------

    rows = generate_damage_records()

    print(
        f"Damage-based records generated: "
        f"{len(rows):,}"
    )

    normal_rows = generate_normal_records()

    print(
        f"Normal/restyling records generated: "
        f"{len(normal_rows):,}"
    )

    rows.extend(normal_rows)

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    rows = remove_duplicates(rows)

    print(
        f"Unique valid records: "
        f"{len(rows):,}"
    )

    # --------------------------------------------------------
    # Balance to target
    # --------------------------------------------------------

    rows = balance_dataset(rows)

    # --------------------------------------------------------
    # Assign IDs
    # --------------------------------------------------------

    rows = assign_ids(rows)

    # --------------------------------------------------------
    # Final validation
    # --------------------------------------------------------

    if not MIN_ROWS <= len(rows) <= MAX_ROWS:

        raise RuntimeError(
            f"Final dataset contains {len(rows):,} records. "
            f"Required range is {MIN_ROWS:,}-{MAX_ROWS:,}."
        )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    output_path = save_csv(rows)

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    rule_count = len(
        set(
            row["rule_id"]
            for row in rows
        )
    )

    clothing_count = len(
        set(
            row["clothing_type"]
            for row in rows
        )
    )

    print()
    print("=" * 70)
    print("DATASET CREATED SUCCESSFULLY")
    print("=" * 70)

    print(
        f"CSV file: {output_path.resolve()}"
    )

    print(
        f"Rows: {len(rows):,}"
    )

    print(
        f"Columns: {len(FIELDS)}"
    )

    print(
        f"Rules represented: {rule_count}"
    )

    print(
        f"Clothing types represented: {clothing_count}"
    )

    print()
    print("Important:")
    print(
        "This is a rule-based knowledge base, "
        "not 30,000 independent real-world observations."
    )

    print(
        "Use the knowledge base as the recommendation "
        "layer of the Restyle system."
    )

    print("=" * 70)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()