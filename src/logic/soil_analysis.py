def get_nitrogen_status(value):

    if value < 30:
        return "LOW_NITROGEN"

    elif value <= 70:
        return "NORMAL_NITROGEN"

    return "HIGH_NITROGEN"


def get_phosphorus_status(value):

    if value < 30:
        return "LOW_PHOSPHORUS"

    elif value <= 70:
        return "NORMAL_PHOSPHORUS"

    return "HIGH_PHOSPHORUS"


def get_potassium_status(value):

    if value < 30:
        return "LOW_POTASSIUM"

    elif value <= 70:
        return "NORMAL_POTASSIUM"

    return "HIGH_POTASSIUM"