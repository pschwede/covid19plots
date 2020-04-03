#!/usr/bin/env python
"""
Scrape RKI Dashboard
"""

from datetime import datetime
import requests
import pandas as pd

CASES_URL = ("https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/"
             "RKI_COVID19/FeatureServer/0/query?f=json"
             "&where=(Meldedatum%3Etimestamp%20%272020-03-01%2022%3A59%3A59%27%20"
             "AND%20NeuerFall%20IN(0%2C%201))%20"
             "AND%20(Bundesland%3D%27BUNDESLAND%27)"
             "&returnGeometry=false&spatialRel=esriSpatialRelIntersects"
             "&outFields=ObjectId%2CAnzahlFall%2CMeldedatum%2CNeuerFall"
             "&orderByFields=Meldedatum%20asc&resultOffset=0&resultRecordCount=2000"
             "&cacheHint=true")

CUMSUM_CASES_URL = ("https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/"
                    "services/Covid19_RKI_Sums/FeatureServer/0/query?f=json"
                    "&where=(Meldedatum%3Etimestamp%20%272020-03-01%2022%3A59%3A59%27%20)%20"
                    "AND%20(Bundesland%3D%27BUNDESLAND%27)"
                    "&returnGeometry=false&spatialRel=esriSpatialRelIntersects"
                    "&outFields=ObjectId%2CSummeFall%2CMeldedatum"
                    "&orderByFields=Meldedatum%20asc&resultOffset=0"
                    "&resultRecordCount=2000&cacheHint=true")

FULL_FEDERAL_STATE_NAME = {
    "BB": "Brandenburg",
    "BE": "Berlin",
    "BW": "Baden-Württemberg",
    "BY": "Bayern",
    "HB": "Bremen",
    "HE": "Hessen",
    "HH": "Hamburg",
    "MV": "Mecklenburg-Vorpommern",
    "NI": "Niedersachsen",
    "NRW": "Nordrhein-Westfalen",
    "RP": "Rheinland-Pfalz",
    "SH": "Schleswig-Holstein",
    "SL": "Saarland",
    "SN": "Sachsen",
    "ST": "Sachsen-Anhalt",
    "TH": "Thüringen",
}

def to_dataframe(federal_state: str, cumulated: bool = False) -> pd.DataFrame:
    """
    Load German data from RKI dashboard

    Args:
        federal_state: state name or one of DE, BW, BY, BE, BB, HB, HH, HE, MV,
                       NI, NW, RP, SL, SN, ST, SH, TH

    Returns:
        A fully functional pandas.DataFrame
    """
    if len(federal_state) == 2:
        federal_state = FULL_FEDERAL_STATE_NAME[federal_state]

    url = CASES_URL
    if cumulated:
        url = CUMSUM_CASES_URL

    response_json = requests.get(url.replace("BUNDESLAND", federal_state)).json()

    return pd.DataFrame(
        [([int(feature['attributes']['SummeFall'])] if cumulated else \
                [int(feature['attributes']['AnzahlFall']),
                 int(feature['attributes']['NeuerFall'])]) \
                for feature in response_json['features']],
        index=[datetime.utcfromtimestamp(int(feature['attributes']['Meldedatum'])/1000) \
                for feature in response_json['features']],
        columns=['SummeFall'] if cumulated else ['AnzahlFall', 'NeuerFall'])

if __name__ == "__main__":
    print(to_dataframe("SN"))
