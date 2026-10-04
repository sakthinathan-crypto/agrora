
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "models" / "disease_model.h5"


# ============================================================
# MODEL CONFIGURATION
# ============================================================

IMAGE_SIZE = (224, 224)

CLASS_NAMES = [
    "healthy",
    "leaf_blight",
    "other_disease",
]


# ============================================================
# LOAD MODEL
# ============================================================

_model = None


def load_disease_model():
    """
    Load the disease detection model only once.
    """

    global _model

    if _model is None:

        if not MODEL_PATH.exists():

            raise FileNotFoundError(
                f"Disease model not found: {MODEL_PATH}"
            )

        _model = tf.keras.models.load_model(
            MODEL_PATH,
            compile=False
        )

    return _model


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_image(image_path):
    """
    Prepare image for the trained model.
    """

    image_path = Path(image_path)

    if not image_path.exists():

        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    try:

        image = Image.open(image_path)

        image = image.convert("RGB")

        image = image.resize(IMAGE_SIZE)

        image_array = np.asarray(
            image,
            dtype=np.float32
        )

        image_array = image_array / 255.0

        image_array = np.expand_dims(
            image_array,
            axis=0
        )

        return image_array

    except Exception as exc:

        raise ValueError(
            f"Unable to process image: {exc}"
        )


# ============================================================
# DISEASE INFORMATION
# ============================================================

def get_disease_information(disease_name):
    """
    Return farmer-friendly information
    for the predicted disease class.
    """

    disease_name = (
        disease_name
        .lower()
        .strip()
    )

    information = {

        "healthy": {

            "display_name":
                "Healthy Crop",

            "severity":
                "NONE",

            "action":
                (
                    "No immediate disease action "
                    "is required. Continue regular "
                    "crop monitoring."
                ),

            "prevention":
                (
                    "Maintain proper irrigation, "
                    "nutrition, field sanitation and "
                    "regular crop inspection."
                ),
        },

        "leaf_blight": {

            "display_name":
                "Leaf Blight",

            "severity":
                "HIGH",

            "action":
                (
                    "Inspect affected leaves and "
                    "monitor the spread of symptoms. "
                    "Remove severely affected plant "
                    "material where appropriate and "
                    "follow crop-specific disease "
                    "management practices."
                ),

            "prevention":
                (
                    "Avoid prolonged leaf wetness, "
                    "maintain field sanitation and "
                    "monitor nearby plants for new "
                    "symptoms."
                ),
        },

        "other_disease": {

            "display_name":
                "Other Disease",

            "severity":
                "MEDIUM",

            "action":
                (
                    "Inspect the crop carefully and "
                    "monitor symptoms. Consider "
                    "crop-specific diagnosis before "
                    "applying any treatment."
                ),

            "prevention":
                (
                    "Maintain field hygiene, "
                    "appropriate irrigation and "
                    "regular crop health monitoring."
                ),
        },
    }

    return information.get(

        disease_name,

        {

            "display_name":
                "Unknown Condition",

            "severity":
                "UNKNOWN",

            "action":
                (
                    "Inspect the crop manually and "
                    "verify the result before taking "
                    "corrective action."
                ),

            "prevention":
                "Continue regular crop monitoring.",
        }
    )


# ============================================================
# DISEASE PREDICTION
# ============================================================

def predict_disease(image_path):
    """
    Predict disease from a crop image.

    Returns:
        Dictionary containing:
            disease
            class_name
            confidence
            severity
            action
            prevention
    """

    model = load_disease_model()

    image = preprocess_image(
        image_path
    )

    try:

        prediction = model.predict(
            image,
            verbose=0
        )

    except Exception as exc:

        raise RuntimeError(
            f"Disease model prediction failed: {exc}"
        )

    # --------------------------------------------------------
    # Convert model output to flat array
    # --------------------------------------------------------

    probabilities = np.asarray(
        prediction[0]
    ).flatten()

    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    if len(probabilities) != len(
        CLASS_NAMES
    ):

        raise ValueError(
            "Model output classes do not match "
            "the configured disease classes."
        )

    # --------------------------------------------------------
    # Get highest probability class
    # --------------------------------------------------------

    predicted_index = int(
        np.argmax(probabilities)
    )

    confidence = float(
        probabilities[predicted_index]
    ) * 100.0

    disease_name = CLASS_NAMES[
        predicted_index
    ]

    # --------------------------------------------------------
    # Get disease information
    # --------------------------------------------------------

    information = get_disease_information(
        disease_name
    )

    # --------------------------------------------------------
    # Final prediction result
    # --------------------------------------------------------

    return {

        "disease":
            information["display_name"],

        "class_name":
            disease_name,

        "confidence":
            round(
                confidence,
                2
            ),

        "severity":
            information["severity"],

        "action":
            information["action"],

        "prevention":
            information["prevention"],
    }


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def detect_disease(image_path):
    """
    Public interface for AGRORA.

    Returns:

        {
            "success": True,
            "prediction": {
                ...
            }
        }
    """

    try:

        result = predict_disease(
            image_path
        )

        return {

            "success":
                True,

            "prediction":
                result,
        }

    except FileNotFoundError as exc:

        return {

            "success":
                False,

            "error":
                str(exc),
        }

    except (
        ValueError,
        RuntimeError,
        OSError
    ) as exc:

        return {

            "success":
                False,

            "error":
                str(exc),
        }

    except Exception as exc:

        return {

            "success":
                False,

            "error":
                (
                    "Unexpected disease detection "
                    f"error: {exc}"
                ),
        }


# ============================================================
# TEST MODE
# ============================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "AGRORA DISEASE DETECTION ENGINE"
    )

    print("=" * 60)

    print(
        f"Model path : {MODEL_PATH}"
    )

    print(
        f"Image size : {IMAGE_SIZE}"
    )

    print(
        f"Classes    : {CLASS_NAMES}"
    )

    try:

        model = load_disease_model()

        print()

        print(
            "Model loaded successfully."
        )

        print(
            f"Input shape  : {model.input_shape}"
        )

        print(
            f"Output shape : {model.output_shape}"
        )

        print()

        print(
            "Disease detection engine is ready."
        )

    except Exception as exc:

        print()

        print(
            "Model loading failed."
        )

        print(
            f"Error: {exc}"
        )