#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from glob import glob
from datetime import datetime
import matplotlib.dates as mdates

from scrape import scrape, divi, entorb

federal_state_translation = {
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

def load_tsv():
    """Load local tsv file"""
    df = pd \
            .read_csv("data/divi.tsv", sep="\t") \
            .replace({
                'NaN': 0.0,
                'VERFUEGBAR': 1.0,
                'BEGRENZT': 0.5,
                'NICHT_VERFUEGBAR': 0.0
                })
    df['Stand'] = pd.to_datetime(df['Stand'], format="%Y-%m-%d %H:%M:%S")
    return df


def plot_german_hbars(dataframe, fname):
    """Plot a horizontal bar for each federal state."""
    df = dataframe[(dataframe['Stand'] > '2019-12-31') & (dataframe['Stand'] <= datetime.now())].set_index('Stand') \
            .drop(columns='COVID-19 cases')

    fig, ax = plt.subplots()
    df \
            .groupby(['Bundesland']).mean().reset_index() \
            .plot(kind='barh', ax=ax, x='Bundesland', y=['ECMO', 'ICU high care', 'ICU low care'], stacked=True, figsize=(8,8))
    ax.set_title("German mean hospital occupancy")
    ax.set_xticks([0.0, 1.5, 3.0])
    ax.set_xticklabels(["available", "limited", "exhausted"])
    ax.set_ylabel("federal state")
    fig.savefig(fname)
    
def plot_history(dataframe, fname):
    """Plot each federal state's total exhaustion from @entorb but also keep each curve in
    dict bundesland_curves for later correlations"""
    availability = dict()
    deaths = dict()

    df = dataframe.set_index('Stand').bfill()

    for federal_state in federal_state_translation:
        availability[federal_state] = df[df['Bundesland'] == federal_state].resample('D').mean()
        deaths[federal_state] = entorb.to_dataframe(federal_state)['Deaths_New']
        deaths[federal_state].name = 'Deaths'

    for federal_state in sorted(list(federal_state_translation.keys())):
        fig, ax = plt.subplots()

        ax = deaths[federal_state].plot(kind='line', ax=ax, color='grey', linestyle=':', marker='+', legend=True, figsize=(16,9))
        ax.set_xlabel('Deaths')

        ax = availability[federal_state].plot(kind='line', ax=ax, secondary_y=True, marker='') # drawstyle=steps-post
        ax.set_yticks([
            0.0, # * num_clinics[federal_state],
            0.5, # * num_clinics[federal_state],
            1.0, # * num_clinics[federal_state],
            ])
        ax.set_yticklabels(["available", "limited", "unavailable"])
        ax.set_title("%s" % federal_state_translation[federal_state])

        fig.savefig(fname % {'state': federal_state})


if __name__ == "__main__":
    import sys
    df = load_tsv()
    plot_german_hbars(dataframe=df, fname=sys.argv[1])
    plot_history(dataframe=load_tsv(), fname=sys.argv[2]) 
