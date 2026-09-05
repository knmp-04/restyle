# ============================================================
# INTELLIGENT WARDROBE UTILIZATION SYSTEM
# RESTYLE
# ============================================================

import streamlit as st
import numpy as np
import pandas as pd
import cv2
import torch
import joblib
import gc

from PIL import Image

from rembg import remove, new_session

from sklearn.cluster import KMeans

from transformers import CLIPProcessor, CLIPModel


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(

    page_title="Intelligent Wardrobe Utilization System",

    page_icon="👕",

    layout="wide"

)


# ============================================================
# TITLE
# ============================================================

st.title(
    "👕 Intelligent Wardrobe Utilization System"
)

st.write(
    """
    Upload a clothing image. The system identifies the
    clothing category and colour and uses two Machine
    Learning algorithms to recommend suitable circular
    usage options.
    """
)


# ============================================================
# LOAD LIGHTWEIGHT REMBG MODEL
# ============================================================

@st.cache_resource
def load_background_removal_model():

    # u2netp is much lighter than bria-rmbg
    session = new_session(
        "u2netp"
    )

    return session


try:

    rembg_session = (
        load_background_removal_model()
    )

except Exception as e:

    st.error(
        "Unable to load the background removal model."
    )

    st.exception(e)

    st.stop()


# ============================================================
# LOAD MACHINE LEARNING MODELS
# ============================================================

@st.cache_resource
def load_ml_models():

    rf_model = joblib.load(
        "random_forest_model.pkl"
    )

    gb_model = joblib.load(
        "gradient_boosting_model.pkl"
    )

    preprocessor = joblib.load(
        "preprocessor.pkl"
    )

    selected_feature_indices = joblib.load(
        "selected_feature_indices.pkl"
    )

    feature_columns = joblib.load(
        "feature_columns.pkl"
    )

    return (

        rf_model,

        gb_model,

        preprocessor,

        selected_feature_indices,

        feature_columns

    )


try:

    (
        rf_model,

        gb_model,

        preprocessor,

        selected_feature_indices,

        feature_columns

    ) = load_ml_models()


except Exception as e:

    st.error(
        "Error loading Machine Learning models."
    )

    st.exception(e)

    st.stop()


# ============================================================
# LOAD CLIP MODEL
# ============================================================

@st.cache_resource
def load_clip_model():

    model_name = (
        "openai/clip-vit-base-patch32"
    )

    model = CLIPModel.from_pretrained(
        model_name
    )

    processor = CLIPProcessor.from_pretrained(
        model_name
    )

    model.eval()

    return model, processor


try:

    clip_model, clip_processor = (
        load_clip_model()
    )

except Exception as e:

    st.error(
        "Error loading CLIP model."
    )

    st.exception(e)

    st.stop()


# ============================================================
# CLOTHING CATEGORIES
# ============================================================

clothing_categories = [

    "a t-shirt",

    "a shirt",

    "a pair of jeans",

    "a pair of trousers",

    "a pair of shorts",

    "a dress",

    "a jacket",

    "a skirt",

    "a hoodie",

    "a sweater",

    "a kurta",

    "a saree"

]


# ============================================================
# DETECT CLOTHING CATEGORY
# ============================================================

def detect_clothing(image):

    inputs = clip_processor(

        text=clothing_categories,

        images=image,

        return_tensors="pt",

        padding=True

    )

    with torch.no_grad():

        outputs = clip_model(
            **inputs
        )

        probabilities = (

            outputs
            .logits_per_image
            .softmax(dim=1)

        )

    # Get top 3 categories
    top_values, top_indices = (
        torch.topk(
            probabilities,
            k=3
        )
    )

    results = []

    for i in range(3):

        index = (
            top_indices[0][i]
            .item()
        )

        score = (
            top_values[0][i]
            .item() * 100
        )

        results.append({

            "Category":
                clothing_categories[index],

            "Confidence":
                score

        })


    predicted_index = (
        probabilities.argmax().item()
    )

    predicted_clothing = (
        clothing_categories[
            predicted_index
        ]
    )

    confidence = (

        probabilities[
            0
        ][
            predicted_index
        ].item() * 100

    )

    return (

        predicted_clothing,

        confidence,

        results

    )


# ============================================================
# DOMINANT COLOUR
# ============================================================

def get_dominant_color(
    image,
    k=3
):

    image_array = np.array(

        image.convert("RGBA")

    )

    rgb = (
        image_array[:, :, :3]
    )

    alpha = (
        image_array[:, :, 3]
    )

    # Only visible pixels
    pixels = rgb[
        alpha > 50
    ]

    if len(pixels) < k:

        return np.array(
            [0, 0, 0]
        )


    # Remove almost-white background
    pixels = pixels[
        ~(
            (pixels[:, 0] > 245) &
            (pixels[:, 1] > 245) &
            (pixels[:, 2] > 245)
        )
    ]


    if len(pixels) < k:

        return np.array(
            [0, 0, 0]
        )


    # Limit pixels for memory
    if len(pixels) > 10000:

        indices = np.random.choice(

            len(pixels),

            10000,

            replace=False

        )

        pixels = pixels[
            indices
        ]


    kmeans = KMeans(

        n_clusters=k,

        random_state=42,

        n_init=10

    )

    labels = kmeans.fit_predict(
        pixels
    )

    counts = np.bincount(
        labels
    )

    dominant_index = np.argmax(
        counts
    )

    dominant_color = (

        kmeans
        .cluster_centers_[
            dominant_index
        ]
        .astype(int)

    )

    return dominant_color


# ============================================================
# RGB TO COLOUR NAME
# ============================================================

def get_color_name(rgb):

    color = np.uint8(
        [[rgb]]
    )

    hsv = cv2.cvtColor(

        color,

        cv2.COLOR_RGB2HSV

    )[0][0]

    h, s, v = hsv


    if v < 50:

        return "Black"


    if s < 30 and v > 180:

        return "White"


    if s < 30:

        return "Grey"


    if h < 10 or h >= 170:

        return "Red"


    if h < 25:

        return "Orange"


    if h < 35:

        return "Yellow"


    if h < 85:

        return "Green"


    if h < 100:

        return "Cyan"


    if h < 130:

        return "Blue"


    if h < 155:

        return "Purple"


    return "Pink"


# ============================================================
# CLEAN CLOTHING TYPE
# ============================================================

def clean_clothing_type(
    clothing_type
):

    value = (
        clothing_type
        .lower()
    )

    value = value.replace(
        "a pair of ",
        ""
    )

    value = value.replace(
        "a ",
        ""
    )

    return value.strip().title()


# ============================================================
# PROBLEM CHECK
# ============================================================

def has_problem(value):

    value = str(
        value
    ).strip().lower()

    no_problem = [

        "none",

        "no",

        "unknown",

        "",

        "nan"

    ]

    if value in no_problem:

        return 0

    return 1


# ============================================================
# GET TOP ML PREDICTIONS
# ============================================================

def get_top_predictions(
    model,
    X,
    number=3
):

    probabilities = (
        model.predict_proba(X)[0]
    )

    classes = (
        model.classes_
    )

    top_indices = np.argsort(
        probabilities
    )[::-1][:number]

    results = []

    for index in top_indices:

        results.append({

            "Recommendation":
                classes[index],

            "Probability":
                probabilities[index] * 100

        })

    return pd.DataFrame(
        results
    )


# ============================================================
# IMAGE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(

    "📷 Upload a clothing image",

    type=[
        "jpg",
        "jpeg",
        "png",
        "webp"
    ]

)


# ============================================================
# PROCESS IMAGE
# ============================================================

if uploaded_file is not None:

    try:

        # ====================================================
        # LOAD IMAGE
        # ====================================================

        original_image = (

            Image
            .open(uploaded_file)
            .convert("RGBA")

        )


        # ====================================================
        # RESIZE IMAGE
        # ====================================================

        MAX_SIZE = 600

        width, height = (
            original_image.size
        )

        if max(
            width,
            height
        ) > MAX_SIZE:

            ratio = (

                MAX_SIZE /
                max(width, height)

            )

            new_width = int(
                width * ratio
            )

            new_height = int(
                height * ratio
            )

            original_image = (

                original_image.resize(

                    (
                        new_width,
                        new_height
                    ),

                    Image.LANCZOS

                )

            )


        # ====================================================
        # BACKGROUND REMOVAL
        # ====================================================

        with st.spinner(

            "Removing background..."

        ):

            processed_image = remove(

                original_image,

                session=rembg_session

            )

            gc.collect()


        # ====================================================
        # DISPLAY IMAGES
        # ====================================================

        st.divider()

        image_col1, image_col2 = (
            st.columns(2)
        )


        with image_col1:

            st.subheader(
                "Original Image"
            )

            st.image(

                original_image,

                use_container_width=True

            )


        with image_col2:

            st.subheader(
                "Background Removed"
            )

            st.image(

                processed_image,

                use_container_width=True

            )


        # ====================================================
        # IMAGE ANALYSIS
        # ====================================================

        with st.spinner(

            "Analysing clothing image..."

        ):

            clip_image = (

                processed_image
                .convert("RGB")

            )


            (

                clothing_type,

                clothing_confidence,

                clothing_results

            ) = detect_clothing(
                clip_image
            )


            dominant_rgb = (

                get_dominant_color(
                    processed_image
                )

            )


            detected_colour = (

                get_color_name(
                    dominant_rgb
                )

            )


        # ====================================================
        # DISPLAY DETECTION RESULTS
        # ====================================================

        st.divider()

        st.header(
            "🔍 Image Analysis"
        )


        result1, result2, result3 = (
            st.columns(3)
        )


        with result1:

            st.metric(

                "Clothing Category",

                clothing_type

            )


        with result2:

            st.metric(

                "Detected Colour",

                detected_colour

            )


        with result3:

            st.metric(

                "Category Confidence",

                f"{clothing_confidence:.2f}%"

            )


        # ====================================================
        # TOP 3 CLIP CATEGORIES
        # ====================================================

        with st.expander(

            "View Clothing Detection Scores"

        ):

            clip_df = pd.DataFrame(
                clothing_results
            )

            clip_df["Confidence"] = (
                clip_df["Confidence"]
                .round(2)
            )

            st.dataframe(

                clip_df,

                use_container_width=True

            )


        # ====================================================
        # ADDITIONAL INFORMATION
        # ====================================================

        st.divider()

        st.header(
            "👕 Clothing Information"
        )

        st.write(

            """
            The category and colour are automatically
            extracted from the uploaded image.

            Provide the remaining information required
            by the Machine Learning model.
            """

        )


        col1, col2 = (
            st.columns(2)
        )


        # ====================================================
        # COLUMN 1
        # ====================================================

        with col1:

            condition = st.selectbox(

                "Condition",

                [

                    "New",

                    "Good",

                    "Fair",

                    "Poor",

                    "Unknown"

                ]

            )


            pattern = st.selectbox(

                "Pattern",

                [

                    "Plain",

                    "Striped",

                    "Printed",

                    "Checked",

                    "Unknown"

                ]

            )


            pilling = st.selectbox(

                "Pilling",

                [

                    "None",

                    "Low",

                    "Medium",

                    "High"

                ]

            )


            material = st.selectbox(

                "Material",

                [

                    "Cotton",

                    "Denim",

                    "Polyester",

                    "Wool",

                    "Silk",

                    "Linen",

                    "Unknown"

                ]

            )


        # ====================================================
        # COLUMN 2
        # ====================================================

        with col2:

            damage = st.selectbox(

                "Damage",

                [

                    "None",

                    "Minor",

                    "Major"

                ]

            )


            stains = st.selectbox(

                "Stains",

                [

                    "None",

                    "Minor",

                    "Major"

                ]

            )


            holes = st.selectbox(

                "Holes",

                [

                    "None",

                    "Minor",

                    "Major"

                ]

            )


            smell = st.selectbox(

                "Smell",

                [

                    "None",

                    "Mild",

                    "Strong"

                ]

            )


        # ====================================================
        # PREDICTION BUTTON
        # ====================================================

        if st.button(

            "♻️ Generate Recommendations",

            use_container_width=True

        ):

            # =================================================
            # CLEAN CATEGORY
            # =================================================

            clean_type = (
                clean_clothing_type(
                    clothing_type
                )
            )


            # =================================================
            # ENGINEERED FEATURES
            # =================================================

            has_damage_value = (
                has_problem(damage)
            )

            has_stains_value = (
                has_problem(stains)
            )

            has_holes_value = (
                has_problem(holes)
            )

            has_smell_value = (
                has_problem(smell)
            )

            has_pilling_value = (
                has_problem(pilling)
            )


            issue_score = (

                has_damage_value +

                has_stains_value +

                has_holes_value +

                has_smell_value +

                has_pilling_value

            )


            # =================================================
            # CREATE MODEL INPUT
            # =================================================

            user_input = pd.DataFrame([{

                "type":
                    clean_type,

                "colors":
                    detected_colour,

                "condition":
                    condition,

                "pattern":
                    pattern,

                "pilling":
                    pilling,

                "damage":
                    damage,

                "stains":
                    stains,

                "holes":
                    holes,

                "smell":
                    smell,

                "material":
                    material,

                "has_damage":
                    has_damage_value,

                "has_stains":
                    has_stains_value,

                "has_holes":
                    has_holes_value,

                "has_smell":
                    has_smell_value,

                "has_pilling":
                    has_pilling_value,

                "issue_score":
                    issue_score

            }])


            # =================================================
            # MATCH TRAINING FEATURES
            # =================================================

            user_input = (

                user_input.reindex(

                    columns=feature_columns,

                    fill_value="Unknown"

                )

            )


            # =================================================
            # SHOW INPUT
            # =================================================

            with st.expander(

                "View Final Input Used By ML Models"

            ):

                st.dataframe(

                    user_input,

                    use_container_width=True

                )


            # =================================================
            # PREPROCESS
            # =================================================

            try:

                encoded_input = (

                    preprocessor.transform(
                        user_input
                    )

                )


                # ---------------------------------------------
                # SPARSE → DENSE
                # ---------------------------------------------

                if hasattr(

                    encoded_input,

                    "toarray"

                ):

                    encoded_input = (

                        encoded_input.toarray()

                    )


                # ---------------------------------------------
                # NUMERICAL ARRAY
                # ---------------------------------------------

                encoded_input = np.asarray(

                    encoded_input,

                    dtype=np.float64

                )


                # ---------------------------------------------
                # FEATURE SELECTION
                # ---------------------------------------------

                selected_input = (

                    encoded_input[

                        :,

                        selected_feature_indices

                    ]

                )


                selected_input = np.asarray(

                    selected_input,

                    dtype=np.float64

                )


                # =================================================
                # CHECK FEATURES
                # =================================================

                if (

                    selected_input.shape[1]

                    != rf_model.n_features_in_

                ):

                    raise ValueError(

                        f"""
                        Random Forest expects
                        {rf_model.n_features_in_}
                        features but received
                        {selected_input.shape[1]}.
                        """

                    )


                if (

                    selected_input.shape[1]

                    != gb_model.n_features_in_

                ):

                    raise ValueError(

                        f"""
                        Gradient Boosting expects
                        {gb_model.n_features_in_}
                        features but received
                        {selected_input.shape[1]}.
                        """

                    )


                # =================================================
                # RANDOM FOREST
                # =================================================

                rf_prediction = (

                    rf_model.predict(
                        selected_input
                    )[0]

                )


                rf_probability = (

                    rf_model.predict_proba(
                        selected_input
                    )[0]

                )


                rf_confidence = (

                    rf_probability.max()
                    * 100

                )


                rf_top3 = (

                    get_top_predictions(

                        rf_model,

                        selected_input,

                        3

                    )

                )


                # =================================================
                # GRADIENT BOOSTING
                # =================================================

                gb_prediction = (

                    gb_model.predict(
                        selected_input
                    )[0]

                )


                gb_probability = (

                    gb_model.predict_proba(
                        selected_input
                    )[0]

                )


                gb_confidence = (

                    gb_probability.max()
                    * 100

                )


                gb_top3 = (

                    get_top_predictions(

                        gb_model,

                        selected_input,

                        3

                    )

                )


            except Exception as e:

                st.error(

                    "Machine Learning prediction failed."

                )

                st.exception(e)

                st.stop()


            # ====================================================
            # RESULTS
            # ====================================================

            st.divider()

            st.header(
                "♻️ Machine Learning Predictions"
            )


            # ====================================================
            # TWO MODEL RESULTS
            # ====================================================

            model1, model2 = (
                st.columns(2)
            )


            # ====================================================
            # RANDOM FOREST
            # ====================================================

            with model1:

                st.subheader(
                    "🌲 Random Forest"
                )

                st.success(

                    f"""
                    **Prediction:**

                    {rf_prediction}
                    """

                )

                st.metric(

                    "Confidence",

                    f"{rf_confidence:.2f}%"

                )


                st.write(
                    "Top 3 Predictions"
                )


                rf_display = (
                    rf_top3.copy()
                )

                rf_display["Probability"] = (

                    rf_display["Probability"]
                    .round(2)
                    .astype(str)
                    + "%"

                )


                st.dataframe(

                    rf_display,

                    hide_index=True,

                    use_container_width=True

                )


            # ====================================================
            # GRADIENT BOOSTING
            # ====================================================

            with model2:

                st.subheader(
                    "📈 Gradient Boosting"
                )

                st.success(

                    f"""
                    **Prediction:**

                    {gb_prediction}
                    """

                )

                st.metric(

                    "Confidence",

                    f"{gb_confidence:.2f}%"

                )


                st.write(
                    "Top 3 Predictions"
                )


                gb_display = (
                    gb_top3.copy()
                )

                gb_display["Probability"] = (

                    gb_display["Probability"]
                    .round(2)
                    .astype(str)
                    + "%"

                )


                st.dataframe(

                    gb_display,

                    hide_index=True,

                    use_container_width=True

                )


            # ====================================================
            # VISUALIZATION
            # ====================================================

            st.divider()

            st.header(
                "📊 Model Prediction Visualization"
            )


            # ====================================================
            # CHART 1
            # ====================================================

            st.subheader(
                "Prediction Confidence"
            )


            confidence_data = pd.DataFrame({

                "Model": [

                    "Random Forest",

                    "Gradient Boosting"

                ],

                "Confidence": [

                    rf_confidence,

                    gb_confidence

                ]

            })


            st.bar_chart(

                confidence_data.set_index(
                    "Model"
                )

            )


            # ====================================================
            # CHART 2
            # ====================================================

            st.subheader(
                "Top 3 Predictions - Random Forest"
            )


            rf_chart_data = (

                rf_top3
                .set_index(
                    "Recommendation"
                )

            )


            st.bar_chart(

                rf_chart_data[
                    "Probability"
                ]

            )


            # ====================================================
            # CHART 3
            # ====================================================

            st.subheader(
                "Top 3 Predictions - Gradient Boosting"
            )


            gb_chart_data = (

                gb_top3
                .set_index(
                    "Recommendation"
                )

            )


            st.bar_chart(

                gb_chart_data[
                    "Probability"
                ]

            )


            # ====================================================
            # FINAL COMPARISON
            # ====================================================

            st.divider()

            st.header(
                "🏆 Model Comparison"
            )


            comparison = pd.DataFrame({

                "Model": [

                    "Random Forest",

                    "Gradient Boosting"

                ],

                "Prediction": [

                    rf_prediction,

                    gb_prediction

                ],

                "Confidence (%)": [

                    round(
                        rf_confidence,
                        2
                    ),

                    round(
                        gb_confidence,
                        2
                    )

                ]

            })


            st.dataframe(

                comparison,

                hide_index=True,

                use_container_width=True

            )


            # ====================================================
            # FINAL RECOMMENDATION
            # ====================================================

            st.divider()

            st.header(
                "⭐ Final Recommendation"
            )


            if (

                rf_prediction
                == gb_prediction

            ):

                st.success(

                    f"""
                    Both algorithms agree.

                    **Recommended Circular Usage:**
                    {rf_prediction}
                    """

                )

                st.info(

                    f"""
                    Random Forest confidence:
                    {rf_confidence:.2f}%

                    Gradient Boosting confidence:
                    {gb_confidence:.2f}%
                    """

                )


            elif (

                rf_confidence
                > gb_confidence

            ):

                st.success(

                    f"""
                    **Recommended Circular Usage:**
                    {rf_prediction}
                    """

                )

                st.info(

                    f"""
                    Random Forest produced the
                    higher-confidence prediction.

                    Random Forest:
                    {rf_confidence:.2f}%

                    Gradient Boosting:
                    {gb_confidence:.2f}%
                    """

                )


            else:

                st.success(

                    f"""
                    **Recommended Circular Usage:**
                    {gb_prediction}
                    """

                )

                st.info(

                    f"""
                    Gradient Boosting produced the
                    higher-confidence prediction.

                    Random Forest:
                    {rf_confidence:.2f}%

                    Gradient Boosting:
                    {gb_confidence:.2f}%
                    """

                )


            # ====================================================
            # TECHNICAL DETAILS
            # ====================================================

            with st.expander(
                "🔧 Technical Details"
            ):

                st.write(
                    "ML input shape:",
                    selected_input.shape
                )

                st.write(
                    "ML input data type:",
                    selected_input.dtype
                )

                st.write(
                    "Random Forest features:",
                    rf_model.n_features_in_
                )

                st.write(
                    "Gradient Boosting features:",
                    gb_model.n_features_in_
                )


    except Exception as e:

        st.error(
            "An error occurred while processing "
            "the uploaded image."
        )

        st.exception(e)


else:

    st.info(
        "👆 Upload a clothing image to start."
    )