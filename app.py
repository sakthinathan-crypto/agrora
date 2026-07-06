from flask import (
    Flask,
    render_template,
    request
)

from src.logic.crop_recommendation_engine import (
    recommend_crops
)

from src.logic.fertilizer_engine import (
    recommend_fertilizer
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    results = None

    ph = ""
    nitrogen = ""
    phosphorus = ""
    potassium = ""

    if request.method == "POST":

        district = request.form["district"]

        ph = float(request.form["ph"])

        nitrogen = int(request.form["nitrogen"])

        phosphorus = int(request.form["phosphorus"])

        potassium = int(request.form["potassium"])

        moisture = request.form["moisture"]

        humidity = request.form["humidity"]

        temperature = float(
            request.form["temperature"]
        )

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

        results = output["recommended_crops"]

    return render_template(

        "index.html",

        results=results,

        ph=ph,

        nitrogen=nitrogen,

        phosphorus=phosphorus,

        potassium=potassium
    )


@app.route("/fertilizer", methods=["POST"])
def fertilizer():

    crop = request.form["crop"]

    ph = float(request.form["ph"])

    nitrogen = int(request.form["nitrogen"])

    phosphorus = int(request.form["phosphorus"])

    potassium = int(request.form["potassium"])

    result = recommend_fertilizer(

        crop=crop,

        nitrogen=nitrogen,

        phosphorus=phosphorus,

        potassium=potassium,

        ph=ph
    )

    return render_template(

        "fertilizer.html",

        crop=crop,

        fertilizers=result[
            "recommended_fertilizers"
        ],

        soil_status=result[
            "soil_status"
        ]
    )


if __name__ == "__main__":
    app.run(debug=True)