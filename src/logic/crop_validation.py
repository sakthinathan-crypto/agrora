def validate_crop(

    crop_row,

    terrain_type,

    rainfall,

    region,

    irrigation

):

    penalty = 0

    reasons = []

    # -------------------------
    # Terrain Validation
    # -------------------------

    crop_terrain = str(
        crop_row["terrain_type"]
    ).upper()

    if terrain_type.upper() != crop_terrain:

        penalty += 20

        reasons.append(
            f"Best suited for {crop_terrain} terrain"
        )

    # -------------------------
    # Rainfall Validation
    # -------------------------

    crop_rainfall = str(
        crop_row["rainfall_requirement"]
    ).upper()

    if rainfall.upper() != crop_rainfall:

        penalty += 15

        reasons.append(
            f"Requires {crop_rainfall} rainfall"
        )

    # -------------------------
    # Region Validation
    # -------------------------

    supported_regions = str(
        crop_row["region_support"]
    ).upper()

    if region.upper() not in supported_regions:

        penalty += 25

        reasons.append(
            "Region mismatch detected"
        )

    # -------------------------
    # Irrigation Validation
    # -------------------------

    crop_irrigation = str(
        crop_row["irrigation_type"]
    ).upper()

    if irrigation.upper() != crop_irrigation:

        penalty += 10

        reasons.append(
            f"Best with {crop_irrigation} irrigation"
        )

    return penalty, reasons