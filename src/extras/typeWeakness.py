type_chart = {
    "bug": {"fighting": 0.5, "grass": 0.5, "ground": 0.5, "fire": 2, "flying": 2, "rock": 2},
    "dark": {"dark": 0.5, "ghost": 0.5, "psychic": 0.5, "bug": 2, "fairy": 2, "fighting": 2},
    "dragon": {"electric": 0.5, "fire": 0.5, "grass": 0.5, "water": 0.5, "dragon": 2, "fairy": 2, "ice": 2},
    "electric": {"electric": 0.5, "flying": 0.5, "steel": 0.5, "ground": 2},
    "fairy": {"bug": 0.5, "dark": 0.5, "dragon": 0.5, "fighting": 0.5, "poison": 2, "steel": 2},
    "fighting": {"bug": 0.5, "dark": 0.5, "rock": 0.5, "fairy": 2, "flying": 2, "psychic": 2},
    "fire": {"bug": 0.5, "fire": 0.5, "fairy": 0.5, "grass": 0.5, "ice": 0.5, "steel": 0.5, "ground": 2, "rock": 2, "water": 2},
    "flying": {"bug": 0.5, "fighting": 0.5, "grass": 0.5, "ground": 0.5, "electric": 2, "ice": 2, "rock": 2},
    "ghost": {"bug": 0.5, "fighting": 0.5, "normal": 0.5, "poison": 0.5, "dark": 2, "ghost": 2},
    "grass": {"electric": 0.5, "grass": 0.5, "ground": 0.5, "water": 0.5, "bug": 2, "fire": 2, "flying": 2, "ice": 2, "poison": 2},
    "ground": {"electric": 0.5, "poison": 0.5, "rock": 0.5, "grass": 2, "ice": 2, "water": 2},
    "ice": {"ice": 0.5, "fighting": 2, "fire": 2, "rock": 2, "steel": 2},
    "normal": {"ghost": 0.5, "fighting": 2},
    "poison": {"fairy": 0.5, "fighting": 0.5, "grass": 0.5, "poison": 0.5, "bug": 0.5, "ground": 2, "psychic": 2},
    "psychic": {"fighting": 0.5, "psychic": 0.5, "bug": 2, "dark": 2, "ghost": 2},
    "rock": {"fire": 0.5, "flying": 0.5, "normal": 0.5, "poison": 0.5, "fighting": 2, "grass": 2, "ground": 2, "steel": 2, "water": 2},
    "steel": {"bug": 0.5, "dragon": 0.5, "fairy": 0.5, "flying": 0.5, "grass": 0.5, "ice": 0.5, "poison": 0.5, "psychic": 0.5, "rock": 0.5, "steel": 0.5, "fighting": 2, "fire": 2, "ground": 2},
    "water": {"fire": 0.5, "ice": 0.5, "steel": 0.5, "water": 0.5, "electric": 2, "grass": 2},
}


def getWeaknessTypes(type1="normal", type2="none"):
    weaknesses = set()
    type1 = type1.lower()
    type2 = type2.lower()
    for t in [type1, type2]:
        if t == "none":
            continue

        type_multipliers = type_chart.get(t, {})
        for other_type, multiplier in type_multipliers.items():
            if multiplier > 1:
                weaknesses.add(other_type.capitalize())

    return list(weaknesses)
