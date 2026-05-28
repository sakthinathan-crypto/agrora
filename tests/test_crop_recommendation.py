from src.logic.crop_recommendation_engine import (
    recommend_crops
)

result = recommend_crops(

    district="Thanjavur",

    ph=6.5,

    nitrogen=20,

    phosphorus=40,

    potassium=30,

    moisture="HIGH",

    humidity="HIGH",

    temperature=30
)

print(result)