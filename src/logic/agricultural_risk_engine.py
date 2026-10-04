"""
AGRORA Agricultural Risk Engine

Purpose:
    Detect agricultural/environmental risks using field conditions.

Current inputs:
    - District
    - Crop
    - Soil moisture
    - Temperature
    - Humidity

Current risk categories:
    - Drought Stress
    - Heat Stress
    - Waterlogging / Excess Moisture

Important:
    Thresholds in this module are configurable engineering defaults.
    They must be agriculturally validated before production deployment.

The engine does NOT claim AI-based prediction.
It is an explainable rule-based risk assessment layer.
"""


# ============================================================
# CONFIGURATION
# ============================================================

# These values are configurable.
# Do not treat them as universal agricultural thresholds.

MOISTURE_LOW_THRESHOLD = 35
MOISTURE_HIGH_THRESHOLD = 85

HEAT_TEMPERATURE_THRESHOLD = 35.0
SEVERE_HEAT_TEMPERATURE_THRESHOLD = 40.0

HIGH_HUMIDITY_THRESHOLD = 85.0


# ============================================================
# INPUT VALIDATION
# ============================================================

def _validate_numeric(value, name, minimum=None, maximum=None):
    """
    Validate numeric input.

    Raises:
        ValueError: If input is missing, non-numeric, or outside range.
    """

    if value is None:
        raise ValueError(f"{name} is required")

    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be numeric")

    if minimum is not None and value < minimum:
        raise ValueError(f"{name} cannot be below {minimum}")

    if maximum is not None and value > maximum:
        raise ValueError(f"{name} cannot be above {maximum}")

    return value


# ============================================================
# DROUGHT RISK
# ============================================================

def detect_drought_risk(moisture):
    """
    Detect possible drought/soil-water stress based on soil moisture.

    Returns:
        Risk dictionary or None.
    """

    moisture = _validate_numeric(
        moisture,
        "soil_moisture",
        0,
        100
    )

    if moisture <= MOISTURE_LOW_THRESHOLD:

        if moisture <= 20:
            severity = "CRITICAL"
        else:
            severity = "WARNING"

        return {
            "risk_type": "DROUGHT_STRESS",
            "severity": severity,
            "status": "WARNING",
            "reason": (
                f"Soil moisture is very low ({moisture:.0f}%). "
                "The crop may experience water stress."
            ),
            "recommended_action": (
                "Inspect the field and assess irrigation requirement. "
                "Prioritize irrigation if crop and soil conditions require it."
            )
        }

    return None


# ============================================================
# HEAT STRESS
# ============================================================

def detect_heat_risk(temperature):
    """
    Detect possible heat stress from air temperature.

    Returns:
        Risk dictionary or None.
    """

    temperature = _validate_numeric(
        temperature,
        "temperature",
        -20,
        70
    )

    if temperature >= SEVERE_HEAT_TEMPERATURE_THRESHOLD:

        return {
            "risk_type": "HEAT_STRESS",
            "severity": "CRITICAL",
            "status": "CRITICAL",
            "reason": (
                f"Temperature is very high ({temperature:.1f} °C). "
                "The crop may be exposed to heat stress."
            ),
            "recommended_action": (
                "Monitor the crop immediately and assess irrigation, "
                "shade, and other crop-specific heat management measures."
            )
        }

    if temperature >= HEAT_TEMPERATURE_THRESHOLD:

        return {
            "risk_type": "HEAT_STRESS",
            "severity": "WARNING",
            "status": "WARNING",
            "reason": (
                f"Temperature is high ({temperature:.1f} °C). "
                "Heat stress risk should be monitored."
            ),
            "recommended_action": (
                "Monitor crop condition and soil moisture. "
                "Apply crop-specific heat management practices when required."
            )
        }

    return None


# ============================================================
# WATERLOGGING / EXCESS MOISTURE
# ============================================================

def detect_waterlogging_risk(moisture, humidity):
    """
    Detect possible excessive-moisture / waterlogging conditions.

    Soil moisture is the primary signal.
    Humidity provides additional environmental context.

    Returns:
        Risk dictionary or None.
    """

    moisture = _validate_numeric(
        moisture,
        "soil_moisture",
        0,
        100
    )

    humidity = _validate_numeric(
        humidity,
        "humidity",
        0,
        100
    )

    # Very high soil moisture is the primary indicator.
    if moisture >= MOISTURE_HIGH_THRESHOLD:

        if humidity >= HIGH_HUMIDITY_THRESHOLD:

            severity = "CRITICAL"

            reason = (
                f"Soil moisture is very high ({moisture:.0f}%) and "
                f"humidity is high ({humidity:.0f}%). "
                "Possible waterlogging or excessive moisture conditions."
            )

        else:

            severity = "WARNING"

            reason = (
                f"Soil moisture is very high ({moisture:.0f}%). "
                "Possible excessive moisture or waterlogging condition."
            )

        return {
            "risk_type": "WATERLOGGING",
            "severity": severity,
            "status": severity,
            "reason": reason,
            "recommended_action": (
                "Inspect field drainage and standing water. "
                "Avoid unnecessary irrigation and take crop-specific "
                "water-management action."
            )
        }

    return None


# ============================================================
# MAIN RISK ENGINE
# ============================================================

def evaluate_risks(
    district,
    crop,
    moisture,
    temperature,
    humidity
):
    """
    Evaluate agricultural risks using currently available
    AGRORA environmental inputs.

    Parameters:
        district      : Tamil Nadu district
        crop          : Selected/recommended crop
        moisture      : Soil moisture percentage (0-100)
        temperature   : Temperature in Celsius
        humidity      : Relative humidity percentage (0-100)

    Returns:
        Dictionary containing risk assessment.
    """

    if not district:
        raise ValueError("district is required")

    if not crop:
        raise ValueError("crop is required")

    moisture = _validate_numeric(
        moisture,
        "soil_moisture",
        0,
        100
    )

    temperature = _validate_numeric(
        temperature,
        "temperature",
        -20,
        70
    )

    humidity = _validate_numeric(
        humidity,
        "humidity",
        0,
        100
    )

    risks = []

    # --------------------------------------------------------
    # Individual risk detection
    # --------------------------------------------------------

    drought = detect_drought_risk(moisture)

    if drought:
        risks.append(drought)

    heat = detect_heat_risk(temperature)

    if heat:
        risks.append(heat)

    waterlogging = detect_waterlogging_risk(
        moisture,
        humidity
    )

    if waterlogging:
        risks.append(waterlogging)

    # --------------------------------------------------------
    # Overall field status
    # --------------------------------------------------------

    if not risks:

        overall_status = "NORMAL"
        overall_severity = "NORMAL"

        overall_action = (
            "No immediate environmental risk detected. "
            "Continue monitoring field conditions."
        )

    else:

        severity_priority = {
            "CRITICAL": 3,
            "WARNING": 2,
            "MONITOR": 1,
            "NORMAL": 0
        }

        highest_risk = max(
            risks,
            key=lambda risk: severity_priority.get(
                risk["severity"],
                0
            )
        )

        overall_severity = highest_risk["severity"]
        overall_status = highest_risk["status"]

        if overall_severity == "CRITICAL":

            overall_action = (
                "Immediate field inspection is recommended. "
                "Follow the recommended action for the critical risk."
            )

        elif overall_severity == "WARNING":

            overall_action = (
                "Monitor the field closely and take appropriate "
                "crop-specific corrective action."
            )

        else:

            overall_action = (
                "Continue monitoring the field."
            )

    return {
        "district": district,
        "crop": crop,

        "input_conditions": {
            "soil_moisture": round(moisture, 1),
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1)
        },

        "overall_status": overall_status,
        "overall_severity": overall_severity,

        "risk_count": len(risks),

        "risks": risks,

        "overall_recommendation": overall_action
    }