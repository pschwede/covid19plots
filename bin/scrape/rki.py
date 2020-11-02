#!/usr/bin/env python
"""
Scrape RKI Dashboard
"""

import requests
from datetime import datetime
import pandas as pd

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
REV_FULL_FEDERAL_STATE_NAME = {v: k for k,v in FULL_FEDERAL_STATE_NAME.items()}

ISO_TO_BUNDESLANDID = {
        v: i+1 for i,v in enumerate("SH,HH,NS,HB,NW,HE,RP,BW,BY,SL,BE,BB,MV,SN,SA,TH".split(","))
        }

def __fetch() -> pd.DataFrame:
    now = datetime.strftime(datetime.now(), '%Y-%m-%d')
    fname = "%s.csv" % now
    try:
        print("trying local file", fname)
        df = pd.read_csv(fname)
        print("source: local file", fname)
        return df
    except:
        pass
    try:
        url = "https://github.com/ihucos/rki-covid19-data/releases/download/%s/data.csv" % now
        print("trying", url)
        df = pd.read_csv(requests.get(url, timeout=(5, 300)))
        df.to_csv(fname)
        print("source:", url)
        return df
    except:
        pass
    try:
        url = 'https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.csv'
        print("trying", url)
        df = pd.read_csv(requests.get(url, timeout=(10, 300)))
        df.to_csv(fname)
        print("source:", url)
        return df
    except:
        pass
    from arcgis.gis import GIS
    key = 'dd4580c810204019a7b8eb3e0b329dd6'
    df = GIS().content \
            .get(key) \
            .tables[0] \
            .query() \
            .sdf \
            .drop(columns=['Altersgruppe2', 'Bundesland', 'ObjectId'])
    df.to_csv(fname)
    print("source: arcgis api, key=%s" % key)
    return df

def to_dataframe(federal_state: str = None, nation: str = None, landkreis: str = None, when_sick: bool = False) -> pd.DataFrame:
    df = __fetch()
    df = df[df['IstErkrankungsbeginn'] == (1 if when_sick else 0)]

    if landkreis and not federal_state and not nation:
        return df[df['Landkreis'] == landkreis]
    if nation and not landkreis and not federal_state:
        df = df.groupby('Refdatum').sum() \
                .reset_index()
    if federal_state and not landkreis and not nation:
        bid = ISO_TO_BUNDESLANDID[federal_state]
        df = df[df['IdBundesland'] == bid] \
            .groupby(['IdBundesland', 'Refdatum']).sum() \
            .reset_index() \
            .drop(columns='IdBundesland')

    df = pd.DataFrame({
        'Date': pd.to_datetime(df['Refdatum']),
        'Cases_New': df['AnzahlFall'] - df['NeuerFall'],
        'Deaths_New':df['AnzahlTodesfall'] - df['NeuerTodesfall'],
        'Cured_New': df['AnzahlGenesen'] - df['NeuGenesen'],
        }).set_index('Date')
    df['Cured'] = df['Cured_New'].cumsum()
    df['Deaths'] = df['Deaths_New'].cumsum()
    df['Cases'] = df['Cases_New'].cumsum() + df['Cured']
    df['Cases_New'] = df['Cases'].diff()
    return df
    

if __name__ == "__main__":
    #print(to_dataframe())
    print(to_dataframe(nation='DE'))
    print(to_dataframe(federal_state="SN"))
