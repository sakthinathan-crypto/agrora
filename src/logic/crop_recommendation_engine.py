import pandas as pd

from src.logic.soil_analysis import (
    get_nitrogen_status,
    get_phosphorus_status,
    get_potassium_status
)

# -----------------------------------------
# LOAD TAMIL NADU DATASET
# -----------------------------------------

crop_data = pd.read_csv(
    "datasets/crop_recommendation_dataset.csv"
)

# -----------------------------------------
# DISTRICT METADATA
# -----------------------------------------

DISTRICT_CONTEXT = {

    "THANJAVUR": {
        "district_category": "DELTA",
        "climate_zone": "HUMID",
        "water_source_type": "CANAL"
    },

    "TIRUVARUR": {
        "district_category": "DELTA",
        "climate_zone": "HUMID",
        "water_source_type": "CANAL"
    },

    "NAGAPATTINAM": {
        "district_category": "COASTAL",
        "climate_zone": "HUMID",
        "water_source_type": "CANAL"
    },

    "ERODE": {
        "district_category": "SEMI_ARID",
        "climate_zone": "HOT",
        "water_source_type": "BOREWELL"
    },

    "COIMBATORE": {
        "district_category": "WESTERN_ZONE",
        "climate_zone": "MODERATE",
        "water_source_type": "BOREWELL"
    },

    "SALEM": {
        "district_category": "SEMI_ARID",
        "climate_zone": "HOT",
        "water_source_type": "BOREWELL"
    },

    "NILGIRIS": {
        "district_category": "HILL",
        "climate_zone": "COOL",
        "water_source_type": "RAINFED"
    },

    "RAMANATHAPURAM": {
        "district_category": "DRY_ZONE",
        "climate_zone": "DRY",
        "water_source_type": "BOREWELL"
    },

    "SIVAGANGAI": {
        "district_category": "DRY_ZONE",
        "climate_zone": "DRY",
        "water_source_type": "BOREWELL"
    },

    "TRICHY": {
        "district_category": "CENTRAL_ZONE",
        "climate_zone": "HOT",
        "water_source_type": "CANAL"
    }
}

# -----------------------------------------
# PARTIAL MATCH SCORING
# -----------------------------------------

def partial_match_score(input_value, crop_value):

    input_value = str(input_value).upper()
    crop_value = str(crop_value).upper()

    if input_value == crop_value:
        return 10

    compatibility = {

        "HIGH": {
            "MEDIUM": 5,
            "LOW": 0
        },

        "MEDIUM": {
            "HIGH": 5,
            "LOW": 5
        },

        "LOW": {
            "MEDIUM": 5,
            "HIGH": 0
        }
    }

    return compatibility.get(
        input_value,
        {}
    ).get(crop_value, 0)

# -----------------------------------------
# MAIN ENGINE
# -----------------------------------------

def recommend_crops(

    district,

    ph,

    nitrogen,

    phosphorus,

    potassium,

    moisture,

    humidity,

    temperature
):

    recommendations = []

    district = district.upper()

    # -----------------------------------------
    # DISTRICT CONTEXT
    # -----------------------------------------

    district_info = DISTRICT_CONTEXT.get(
        district,
        {}
    )

    district_category = district_info.get(
        "district_category",
        ""
    )

    climate_zone = district_info.get(
        "climate_zone",
        ""
    )

    water_source_type = district_info.get(
        "water_source_type",
        ""
    )

    # -----------------------------------------
    # SOIL ANALYSIS
    # -----------------------------------------

    nitrogen_status = get_nitrogen_status(
        nitrogen
    )

    phosphorus_status = get_phosphorus_status(
        phosphorus
    )

    potassium_status = get_potassium_status(
        potassium
    )

    nitrogen_level = nitrogen_status.replace(
        "_NITROGEN",
        ""
    )

    phosphorus_level = phosphorus_status.replace(
        "_PHOSPHORUS",
        ""
    )

    potassium_level = potassium_status.replace(
        "_POTASSIUM",
        ""
    )

    # -----------------------------------------
    # FILTER DATASET BY DISTRICT
    # -----------------------------------------

    filtered_data = crop_data[

        crop_data["district_support"]
        .str.contains(
            district,
            case=False,
            na=False
        )
    ]

    # -----------------------------------------
    # LOOP THROUGH FILTERED CROPS
    # -----------------------------------------

    for _, row in filtered_data.iterrows():

        score = 0

        recommendation_reasons = []

        crop_name = str(
            row["crop_name"]
        )

        # -----------------------------------------
        # pH COMPATIBILITY
        # -----------------------------------------

        ph_min = float(
            row["soil_ph_min"]
        )

        ph_max = float(
            row["soil_ph_max"]
        )

        if ph_min <= ph <= ph_max:

            score += 20

            recommendation_reasons.append(
                "Suitable soil pH"
            )

        # -----------------------------------------
        # NPK MATCHING
        # -----------------------------------------

        nitrogen_score = partial_match_score(

            nitrogen_level,

            row["nitrogen_requirement"]
        )

        phosphorus_score = partial_match_score(

            phosphorus_level,

            row["phosphorus_requirement"]
        )

        potassium_score = partial_match_score(

            potassium_level,

            row["potassium_requirement"]
        )

        score += (
            nitrogen_score
            + phosphorus_score
            + potassium_score
        )

        # -----------------------------------------
        # MOISTURE MATCH
        # -----------------------------------------

        moisture_score = partial_match_score(

            moisture,

            row["moisture_requirement"]
        )

        score += moisture_score * 2

        if moisture_score > 0:

            recommendation_reasons.append(
                "Moisture compatible"
            )

        # -----------------------------------------
        # HUMIDITY MATCH
        # -----------------------------------------

        humidity_score = partial_match_score(

            humidity,

            row["humidity_requirement"]
        )

        score += humidity_score

        # -----------------------------------------
        # TEMPERATURE MATCH
        # -----------------------------------------

        temp_min = float(
            row["temperature_min"]
        )

        temp_max = float(
            row["temperature_max"]
        )

        if temp_min <= temperature <= temp_max:

            score += 25

            recommendation_reasons.append(
                "Temperature suitable"
            )

        # -----------------------------------------
        # DISTRICT CATEGORY VALIDATION
        # -----------------------------------------

        crop_category = str(
            row["district_category"]
        ).upper()

        if crop_category == district_category:

            score += 20

            recommendation_reasons.append(
                "District geography compatible"
            )

        # -----------------------------------------
        # CLIMATE VALIDATION
        # -----------------------------------------

        crop_climate = str(
            row["climate_zone"]
        ).upper()

        if crop_climate == climate_zone:

            score += 15

            recommendation_reasons.append(
                "Climate suitable"
            )

        # -----------------------------------------
        # WATER SOURCE VALIDATION
        # -----------------------------------------

        crop_water = str(
            row["water_source_type"]
        ).upper()

        if crop_water == water_source_type:

            score += 15

            recommendation_reasons.append(
                "Water source compatible"
            )

        # -----------------------------------------
        # PRIORITY SCORE
        # -----------------------------------------

        try:

            priority = int(
                row["district_priority_score"]
            )

            score += priority * 0.2

        except:

            pass

        # -----------------------------------------
        # CONFIDENCE THRESHOLD
        # -----------------------------------------

        if score < 70:
            continue

        # -----------------------------------------
        # FINAL OUTPUT
        # -----------------------------------------

        recommendations.append({

            "crop_name":
                crop_name,

            "suitability_score":
                round(score, 2),

            "district":
                district,

            "growing_season":
                row["growing_season"],

            "expected_growth_days":
                row["expected_growth_days"],

            "water_requirement":
                row["water_requirement"],

            "yield_category":
                row["yield_category"],

            "recommendation_reasons":
                recommendation_reasons
        })

    # -----------------------------------------
    # SORT RESULTS
    # -----------------------------------------

    recommendations.sort(

        key=lambda x: x["suitability_score"],

        reverse=True
    )

    # -----------------------------------------
    # RETURN TOP 3
    # -----------------------------------------

    return {

        "district": district,

        "soil_analysis": {

            "nitrogen_status":
                nitrogen_status,

            "phosphorus_status":
                phosphorus_status,

            "potassium_status":
                potassium_status
        },

        "recommended_crops":
            recommendations[:3]
    }