from src.logic.fertilizer_engine import (
    recommend_fertilizer
)

result = recommend_fertilizer(

    crop="Paddy",

    nitrogen=20,

    phosphorus=50,

    potassium=10,

    ph=6.5
)

print(result)