from flask import Flask, render_template, request
import os
import uuid

from src.logic.crop_recommendation_engine import (
    recommend_crops
)

from src.logic.fertilizer_engine import (
    recommend_fertilizer
)

from src.logic.agricultural_risk_engine import (
    evaluate_risks
)

from src.logic.disease_detection_engine import (
    detect_disease
)


# ============================================================
# FLASK CONFIGURATION
# ============================================================

app = Flask(__name__)

# Maximum uploaded image size = 10 MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


# ============================================================
# UPLOAD CONFIGURATION
# ============================================================

UPLOAD_FOLDER = os.path.join(
    app.root_path,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}


def allowed_file(filename):
    """
    Check whether uploaded file has a valid image extension.
    """

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ============================================================
# HOME / FIELD ANALYSIS
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    results = None
    risk_result = None
    sensor_data = None

    disease_result = None
    disease_error = None

    if request.method == "POST":

        try:

            # ------------------------------------------------
            # GET FIELD INPUTS
            # ------------------------------------------------

            district = request.form["district"]

            ph = float(
                request.form["ph"]
            )

            nitrogen = int(
                request.form["nitrogen"]
            )

            phosphorus = int(
                request.form["phosphorus"]
            )

            potassium = int(
                request.form["potassium"]
            )

            moisture = float(
                request.form["moisture"]
            )

            humidity = float(
                request.form["humidity"]
            )

            temperature = float(
                request.form["temperature"]
            )

            # ------------------------------------------------
            # CROP RECOMMENDATION
            # ------------------------------------------------

            output = recommend_crops(

                district=district,

                ph=ph,

                nitrogen=nitrogen,

                phosphorus=phosphorus,

                potassium=potassium,

                moisture=moisture,

                humidity=humidity,

                temperature=temperature
            )

            results = output.get(
                "recommended_crops",
                []
            )

            # ------------------------------------------------
            # FIND TOP RECOMMENDED CROP
            # ------------------------------------------------

            selected_crop = None

            if results:

                first_crop = results[0]

                if isinstance(
                    first_crop,
                    dict
                ):

                    selected_crop = (
                        first_crop.get("crop")
                        or
                        first_crop.get("crop_name")
                        or
                        first_crop.get("name")
                    )

                else:

                    selected_crop = str(
                        first_crop
                    )

            # ------------------------------------------------
            # AGRICULTURAL RISK ASSESSMENT
            # ------------------------------------------------

            if selected_crop:

                risk_result = evaluate_risks(

                    district=district,

                    crop=selected_crop,

                    moisture=moisture,

                    temperature=temperature,

                    humidity=humidity
                )

            # ------------------------------------------------
            # FIELD CONDITIONS
            # ------------------------------------------------

            sensor_data = {

                "nitrogen": nitrogen,

                "phosphorus": phosphorus,

                "potassium": potassium,

                "ph": ph,

                "moisture": moisture,

                "humidity": humidity,

                "temperature": temperature
            }

        except Exception as e:

            print(
                "Field Analysis Error:",
                e
            )

            disease_error = (
                "Field analysis failed: "
                + str(e)
            )

    return render_template(

        "index.html",

        results=results,

        risk_result=risk_result,

        sensor_data=sensor_data,

        disease_result=disease_result,

        disease_error=disease_error
    )


# ============================================================
# DISEASE DETECTION
# ============================================================

@app.route(
    "/detect-disease",
    methods=["POST"]
)
def detect_disease_route():

    results = None
    risk_result = None
    sensor_data = None

    disease_result = None
    disease_error = None

    image_path = None

    try:

        # ----------------------------------------------------
        # CHECK IMAGE FIELD
        # ----------------------------------------------------

        if "image" not in request.files:

            disease_error = (
                "No image was uploaded."
            )

            return render_template(

                "index.html",

                results=results,

                risk_result=risk_result,

                sensor_data=sensor_data,

                disease_result=None,

                disease_error=disease_error
            )

        # ----------------------------------------------------
        # GET IMAGE
        # ----------------------------------------------------

        image = request.files["image"]

        # ----------------------------------------------------
        # CHECK EMPTY IMAGE
        # ----------------------------------------------------

        if image.filename == "":

            disease_error = (
                "Please select a crop image."
            )

            return render_template(

                "index.html",

                results=results,

                risk_result=risk_result,

                sensor_data=sensor_data,

                disease_result=None,

                disease_error=disease_error
            )

        # ----------------------------------------------------
        # CHECK EXTENSION
        # ----------------------------------------------------

        if not allowed_file(
            image.filename
        ):

            disease_error = (
                "Invalid image format. "
                "Please upload JPG, JPEG, PNG or WEBP."
            )

            return render_template(

                "index.html",

                results=results,

                risk_result=risk_result,

                sensor_data=sensor_data,

                disease_result=None,

                disease_error=disease_error
            )

        # ----------------------------------------------------
        # CREATE UNIQUE FILE NAME
        # ----------------------------------------------------

        extension = (
            image.filename
            .rsplit(".", 1)[1]
            .lower()
        )

        filename = (
            uuid.uuid4().hex
            + "."
            + extension
        )

        image_path = os.path.join(

            UPLOAD_FOLDER,

            filename
        )

        # ----------------------------------------------------
        # SAVE IMAGE
        # ----------------------------------------------------

        image.save(
            image_path
        )

        print()
        print("=" * 60)
        print("DISEASE DETECTION")
        print("=" * 60)

        print(
            "Image received:",
            image_path
        )

        # ----------------------------------------------------
        # CALL DISEASE ENGINE
        # ----------------------------------------------------

        disease_response = detect_disease(
            image_path
        )

        print(
            "Disease Detection Response:"
        )

        print(
            disease_response
        )

        # ====================================================
        # IMPORTANT RESPONSE HANDLING
        # ====================================================

        if isinstance(
            disease_response,
            dict
        ):

            # -----------------------------------------------
            # SUCCESS
            # -----------------------------------------------

            if disease_response.get(
                "success"
            ) is True:

                prediction = (
                    disease_response.get(
                        "prediction"
                    )
                )

                if isinstance(
                    prediction,
                    dict
                ):

                    # ONLY prediction is sent
                    # to the HTML template.
                    disease_result = prediction

                    print(
                        "Disease Prediction:"
                    )

                    print(
                        disease_result
                    )

                else:

                    disease_error = (
                        "Disease detection returned "
                        "an invalid prediction."
                    )

            # -----------------------------------------------
            # FAILURE
            # -----------------------------------------------

            else:

                disease_error = (
                    disease_response.get(
                        "error",
                        "Disease detection failed."
                    )
                )

        else:

            disease_error = (
                "Invalid response received "
                "from disease detection engine."
            )

        # ----------------------------------------------------
        # DELETE TEMPORARY IMAGE
        # ----------------------------------------------------

        try:

            if (
                image_path
                and
                os.path.exists(
                    image_path
                )
            ):

                os.remove(
                    image_path
                )

                image_path = None

        except Exception as cleanup_error:

            print(
                "Image cleanup warning:",
                cleanup_error
            )

        print("=" * 60)
        print()

        # ----------------------------------------------------
        # SEND RESULT TO HTML
        # ----------------------------------------------------

        return render_template(

            "index.html",

            results=results,

            risk_result=risk_result,

            sensor_data=sensor_data,

            disease_result=disease_result,

            disease_error=disease_error
        )

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        print(
            "Disease Detection Error:",
            e
        )

        disease_error = str(e)

        # ----------------------------------------------------
        # CLEANUP IMAGE
        # ----------------------------------------------------

        try:

            if (
                image_path
                and
                os.path.exists(
                    image_path
                )
            ):

                os.remove(
                    image_path
                )

        except Exception as cleanup_error:

            print(
                "Cleanup error:",
                cleanup_error
            )

        return render_template(

            "index.html",

            results=results,

            risk_result=risk_result,

            sensor_data=sensor_data,

            disease_result=None,

            disease_error=disease_error
        )


# ============================================================
# FERTILIZER RECOMMENDATION
# ============================================================

@app.route(
    "/fertilizer",
    methods=["POST"]
)
def fertilizer():

    try:

        crop = request.form[
            "crop"
        ]

        ph = float(
            request.form["ph"]
        )

        nitrogen = int(
            request.form["nitrogen"]
        )

        phosphorus = int(
            request.form["phosphorus"]
        )

        potassium = int(
            request.form["potassium"]
        )

        # ----------------------------------------------------
        # CALL FERTILIZER ENGINE
        # ----------------------------------------------------

        result = recommend_fertilizer(

            crop=crop,

            nitrogen=nitrogen,

            phosphorus=phosphorus,

            potassium=potassium,

            ph=ph
        )

        # ----------------------------------------------------
        # DISPLAY RESULT
        # ----------------------------------------------------

        return render_template(

            "fertilizer.html",

            crop=crop,

            fertilizers=result.get(
                "recommended_fertilizers",
                []
            )
        )

    except Exception as e:

        print(
            "Fertilizer Error:",
            e
        )

        return render_template(

            "fertilizer.html",

            crop=request.form.get(
                "crop",
                "Unknown"
            ),

            fertilizers=[],

            error=str(e)
        )


# ============================================================
# FILE TOO LARGE
# ============================================================

@app.errorhandler(413)
def file_too_large(error):

    return render_template(

        "index.html",

        results=None,

        risk_result=None,

        sensor_data=None,

        disease_result=None,

        disease_error=(
            "Image is too large. "
            "Maximum file size is 10 MB."
        )

    ), 413


# ============================================================
# START FLASK
# ============================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True
    )