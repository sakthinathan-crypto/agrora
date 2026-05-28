import pandas as pd

from src.logic.soil_analysis import (
    get_nitrogen_status,
    get_phosphorus_status,
    get_potassium_status
)
fertilizer_data = pd.read_csv(
    "datasets/fertilizer_dataset.csv"
)


def recommend_fertilizer(
    crop,
    nitrogen,
    phosphorus,
    potassium,
    ph
):
    nitrogen_status = get_nitrogen_status(nitrogen)

    phosphorus_status = get_phosphorus_status(phosphorus)

    potassium_status = get_potassium_status(potassium)

    recommendations = []

    crop = crop.lower()
    for _, row in fertilizer_data.iterrows():

        score = 0

        supported_crops = str(
            row["supported_crops"]
        ).lower()

        suitable_for = str(
            row["suitable_for"]
        ).upper()

        fertilizer_category = str(
            row["fertilizer_category"]
        ).upper()

        soil_ph_range = str(
            row["soil_ph_range"]
        )

        crop_match = crop in supported_crops

        if crop_match:
            score += 40

        nutrient_match = False
        if suitable_for == nitrogen_status:

            nutrient_match = True

            score += 30

            score += min(
                int(row["nitrogen"]),
                20
            )
        elif suitable_for == phosphorus_status:

            nutrient_match = True

            score += 30

            score += min(
                int(row["phosphorus"]),
                20
            )
        elif suitable_for == potassium_status:

            nutrient_match = True

            score += 30

            score += min(
                int(row["potassium"]),
                20
            )

        if (
            "NITROGEN" in fertilizer_category
            and nitrogen_status == "LOW_NITROGEN"
        ):
            score += 15

        if (
            "PHOSPHORUS" in fertilizer_category
            and phosphorus_status == "LOW_PHOSPHORUS"
        ):
            score += 15

        if (
            "POTASSIUM" in fertilizer_category
            and potassium_status == "LOW_POTASSIUM"
        ):
            score += 15

        try:

            ph_min, ph_max = map(
                float,
                soil_ph_range.split("-")
            )

            if ph_min <= ph <= ph_max:
                score += 10

        except:
            pass

        if crop_match and nutrient_match:

            recommendations.append({

                "score": score,

                "fertilizer_name":
                    row["fertilizer_name"],

                "type":
                    row["type"],

                "fertilizer_category":
                    row["fertilizer_category"],

                "NPK":
                    f'{row["nitrogen"]}-'
                    f'{row["phosphorus"]}-'
                    f'{row["potassium"]}',

                "best_growth_stage":
                    row["best_growth_stage"],

                "soil_ph_range":
                    row["soil_ph_range"]
            })
    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )
    top_recommendations = recommendations[:3]

    return {

        "crop": crop,

        "soil_status": {

            "nitrogen": nitrogen_status,

            "phosphorus": phosphorus_status,

            "potassium": potassium_status
        },

        "recommended_fertilizers":
            top_recommendations
    }