from flask import (
    Flask,
    render_template,
    request
)

from src.logic.crop_recommendation_engine import (
    recommend_crops
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])

def home():

    results = None

    if request.method == "POST":

        district = request.form["district"]

        ph = float(request.form["ph"])

        nitrogen = int(
            request.form["nitrogen"]
        )

        phosphorus = int(
            request.form["phosphorus"]
        )

        potassium = int(
            request.form["potassium"]
        )

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

        results = output[
            "recommended_crops"
        ]

    return render_template(

        "index.html",

        results=results
    )


if __name__ == "__main__":

    app.run(debug=True)