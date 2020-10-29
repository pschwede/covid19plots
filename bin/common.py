DE_STATE_NAMES = {
    "BB": "Brandenburg",
    "BE": "Berlin",
    "BW": "Baden-Württemberg",
    "BY": "Bayern",
    "HB": "Bremen",
    "HE": "Hessen",
    "HH": "Hamburg",
    "MV": "Mecklenburg-Vorpommern",
    "NI": "Niedersachsen",
    "NW": "Nordrhein-Westfalen",
    "RP": "Rheinland-Pfalz",
    "SH": "Schleswig-Holstein",
    "SL": "Saarland",
    "SN": "Sachsen",
    "ST": "Sachsen-Anhalt",
    "TH": "Thüringen",
}
DE_STATE_ISO_CODE = {v: k for k,v in DE_STATE_NAMES.items()}

DE_STATE_POPULATION = {
    'Baden-Württemberg': 11069533,
    'Bayern': 13076721,
    'Berlin': 3644826,
    'Brandenburg': 2511917,
    'Bremen': 682986,
    'Hamburg': 1841179,
    'Hessen': 6265809,
    'Mecklenburg-Vorpommern': 1609675,
    'Niedersachsen': 7982448,
    'Nordrhein-Westfalen': 17932651,
    'Rheinland-Pfalz': 4084844,
    'Saarland': 990509,
    'Sachsen': 4077937,
    'Sachsen-Anhalt': 2208321,
    'Schleswig-Holstein': 2896712,
    'Thüringen': 2143145,
}

DAYS_INFECTION_TILL_SYMPTOM = 4
DAYS_SYMPTOMS_TILL_DEATH = 14

DE_POPULATION = 83e6
