from pathlib import Path

from src.logic.disease_detection_engine import detect_disease


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

HEALTHY_DIR = (
    BASE_DIR
    / "datasets"
    / "plant_disease"
    / "healthy"
)


# ============================================================
# FIND AN IMAGE AUTOMATICALLY
# ============================================================

image_extensions = [
    "*.jpg",
    "*.JPG",
    "*.jpeg",
    "*.JPEG",
    "*.png",
    "*.PNG"
]

image_files = []

for extension in image_extensions:
    image_files.extend(
        HEALTHY_DIR.glob(extension)
    )


if not image_files:

    print("=" * 60)
    print("AGRORA DISEASE DETECTION TEST")
    print("=" * 60)
    print("No image found in:")
    print(HEALTHY_DIR)
    print("=" * 60)

else:

    # Use the first available image
    image_path = image_files[0]

    print("=" * 60)
    print("AGRORA DISEASE DETECTION TEST")
    print("=" * 60)

    print("Testing image:")
    print(image_path)

    print()

    # ========================================================
    # RUN DISEASE DETECTION
    # ========================================================

    result = detect_disease(image_path)

    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    if result["success"]:

        prediction = result["prediction"]

        print("Disease       :", prediction["disease"])
        print("Class         :", prediction["class_name"])
        print("Confidence    :", prediction["confidence"], "%")
        print("Severity      :", prediction["severity"])

        print()
        print("Action        :")
        print(prediction["action"])

        print()
        print("Prevention    :")
        print(prediction["prevention"])

    else:

        print("Disease Detection Failed")
        print("Error:", result["error"])

    print()
    print("=" * 60)