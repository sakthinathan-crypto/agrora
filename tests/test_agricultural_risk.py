import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.logic.agricultural_risk_engine import evaluate_risks



def run_test(name, district, crop, moisture, temperature, humidity):
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    try:
        result = evaluate_risks(
            district=district,
            crop=crop,
            moisture=moisture,
            temperature=temperature,
            humidity=humidity
        )

        print("Overall Status :", result["overall_status"])
        print("Severity       :", result["overall_severity"])
        print("Risk Count     :", result["risk_count"])

        if result["risks"]:
            for risk in result["risks"]:
                print("\nRisk           :", risk["risk_type"])
                print("Severity       :", risk["severity"])
                print("Reason         :", risk["reason"])
                print("Action         :", risk["recommended_action"])
        else:
            print("Risk           : NONE")

        print("\nRecommendation :")
        print(result["overall_recommendation"])

    except ValueError as error:
        print("Input Error:", error)


# ------------------------------------------------------------
# TEST 1 - NORMAL CONDITION
# ------------------------------------------------------------

run_test(
    name="TEST 1 - Normal",
    district="Thanjavur",
    crop="Paddy",
    moisture=60,
    temperature=29,
    humidity=55
)


# ------------------------------------------------------------
# TEST 2 - LOW MOISTURE
# ------------------------------------------------------------

run_test(
    name="TEST 2 - Drought Stress",
    district="Thanjavur",
    crop="Paddy",
    moisture=25,
    temperature=30,
    humidity=50
)


# ------------------------------------------------------------
# TEST 3 - HIGH TEMPERATURE
# ------------------------------------------------------------

run_test(
    name="TEST 3 - Heat Stress",
    district="Salem",
    crop="Paddy",
    moisture=55,
    temperature=37,
    humidity=45
)


# ------------------------------------------------------------
# TEST 4 - VERY HIGH TEMPERATURE
# ------------------------------------------------------------

run_test(
    name="TEST 4 - Severe Heat",
    district="Madurai",
    crop="Groundnut",
    moisture=40,
    temperature=42,
    humidity=45
)


# ------------------------------------------------------------
# TEST 5 - WATERLOGGING
# ------------------------------------------------------------

run_test(
    name="TEST 5 - Waterlogging",
    district="Cuddalore",
    crop="Paddy",
    moisture=90,
    temperature=29,
    humidity=90
)


# ------------------------------------------------------------
# TEST 6 - MULTIPLE RISKS
# ------------------------------------------------------------

run_test(
    name="TEST 6 - Multiple Risks",
    district="Madurai",
    crop="Groundnut",
    moisture=25,
    temperature=38,
    humidity=50
)


# ------------------------------------------------------------
# TEST 7 - INVALID INPUT
# ------------------------------------------------------------

run_test(
    name="TEST 7 - Invalid Moisture",
    district="Thanjavur",
    crop="Paddy",
    moisture=150,
    temperature=29,
    humidity=55
)