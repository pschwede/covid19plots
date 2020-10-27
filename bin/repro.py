#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib import dates as mdates

from scrape import entorb
from common import DE_POPULATION, DE_STATE_POPULATION, DE_STATE_NAMES, DAYS_INFECTION_TILL_SYMPTOM, DAYS_SYMPTOMS_TILL_DEATH


def polynomial_r(df, population=DE_POPULATION, generation_time=DAYS_INFECTION_TILL_SYMPTOM):
    """
    Reproduction rate using logistic map

    Args:
        df (DataFrame): data
        population (int): total infectable population
        generation_time: delay between infections in days

    Return:
        DataFrame with reproduction rates for `Deaths` and
        `Cases`
    """
    rs = pd.DataFrame()
    for col in ['Deaths', 'Cases']:
        try:
            normalized = df[col] / population
            earlier = normalized.shift(generation_time)
            rs[col] = normalized / (earlier - earlier**2)
        except KeyError as e:
            """pass"""
    return rs


def rki_r(df, generation_time=DAYS_INFECTION_TILL_SYMPTOM):
    """
    Reproduction rate using RKI method. That is: `r =
    C(one generation time earlier) / C(now)` For each `C`
    sum up Cases over the last generation time.

    Args:
        df (DataFrame): data
        generation_time: delay between infections in days

    Return:
        DataFrame with reproduction rates for `Deaths` and
        `Cases`
    """
    rs = pd.DataFrame()
    for col in ['Deaths', 'Cases']:
        try:
            rolled = df[col+'_New'].rolling("%dD" % generation_time).sum()
            earlier = rolled.shift(generation_time)
            rs[col] = rolled / earlier
        except KeyError as e:
            """pass"""
    return rs


def weekly_r(df, generation_time=7):
    """
    Number of infections per 100k people in a week. Resamples to 7 days.

    Args:
        df (DataFrame): data
        generation_time: delay between infections in days

    Return:
        DataFrame with reproduction rates for `Deaths` and `Cases`
    """
    rs = pd.DataFrame()
    for col in ['Deaths', 'Cases']:
        rs[col] = df[col+'_New_Per_100000'].resample("%dD" % generation_time).sum()
    return rs


def plot_rki_and_logistic_total(state='DE-total'):
    """
    Plot rki and logistic rates for Germany.

    Args:
        state: ISO code of German district, DE-total or Country

    Return:
        Figure
    """
    de = entorb.to_dataframe(state)

    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    l = ax2.plot(de.index, de['Cases_New'].rolling('7D').mean().shift(-3), color='k', label='New Cases rolling week')
    ax2.plot(de.index, de['Cases_New'], linestyle=':', color=l[0].get_color(), label='New Cases')

    poly = polynomial_r(de)['Cases']
    l = ax.plot(de.index, poly.rolling('7D').mean().shift(-3), label='Logistic rate rolling week')
    ax.plot(de.index, poly, linestyle=':', color=l[0].get_color(), label='Logistic rate')

    rki = rki_r(de)['Cases']
    l = ax.plot(de.index, rki.rolling('7D').mean().shift(-3), label='RKI rate rolling week')
    ax.plot(de.index, rki, linestyle=':', color=l[0].get_color(), label='RKI rate')

    plt.legend(handles=ax.lines+ax2.lines)
    ax.axhline(1.0, color='g', alpha=0.5)
    fig.set_size_inches(16,9)
    return fig

def plot_r(population=DE_POPULATION):
    lasts = []
    lasts_rki = []
    areas = sorted([x for x in DE_STATE_NAMES])
    fig, axes = plt.subplots(nrows=4, ncols=4, sharex=True, sharey=True)
    for i, (ax, area) in enumerate(zip(axes.flat, areas)):
        de = entorb.to_dataframe(area).rolling('7D').mean()
        
        rs = polynomial_r(de, population[DE_STATE_NAMES[area]])
        lasts.append(rs[col].tail(1).values[0])
        
        ax.plot(range(-len(rs.index), 0), rs[col])
        ax.set_title("%s (%d Ew.)" % (DE_STATE_NAMES[area], population[DE_STATE_NAMES[area]]))
        ax.set_xlabel('')
        ax.set_xlim(-len(rs.index), 0)
        ax.set_ylim(0, 3)
        
        rs = rki_r(de)
        lasts_rki.append(rs[col].tail(1).values[0])
        
        ax.plot(range(-len(rs.index), 0), rs[col])
        
    fig.set_size_inches(16,16)
    return fig, lasts, lasts_rki

def plot_weekly_r(col='Cases', ncols=4):
    """
    Plot of <col> per week
    
    Args:
        col: What to plot. 'Cases' by default.
        ncols: Columns of charts of resulting figure.

    Return:
        Figure
    """
    lasts = []
    lasts_rki = []
    areas = sorted([x for x in DE_STATE_NAMES])
    fig, axes = plt.subplots(nrows=4, ncols=4, sharex=True, sharey=True)
    for i, (ax, area) in enumerate(zip(axes.flat, areas)):
        de = entorb.to_dataframe(area)

        rs = weekly_r(de)
        lasts.append(rs[col].tail(1).values[0])

        ax.plot(range(-len(rs.index), 0), rs[col])
        ax.set_title("%s" % DE_STATE_NAMES[area])

        rs[col].plot(ax=ax, kind='bar')

    fig.suptitle("Weekly new cases")
    fig.set_size_inches(16,16)
    fig.tight_layout()
    return fig


def plot_rki_and_logistic(col='Cases', ncols=4, population=DE_STATE_POPULATION):
    """
    Plot of reproduction of <col>
    
    Args:
        col: What to plot. 'Cases' by default.
        ncols: Columns of charts of resulting figure.

    Return:
        Tuple of a Figure, a list of last logistical rates and a list of last rki values
    """
    lasts = []
    lasts_rki = []
    areas = sorted([x for x in DE_STATE_NAMES])
    fig, axes = plt.subplots(nrows=4, ncols=4, sharex=True, sharey=True)
    for i, (ax, area) in enumerate(zip(axes.flat, areas)):
        de = entorb.to_dataframe(area).rolling('7D').mean()

        rs = polynomial_r(de, population[DE_STATE_NAMES[area]])
        lasts.append(rs[col].tail(1).values[0])

        ax.plot(range(-len(rs.index), 0), rs[col])
        ax.set_title("%s (%d Ew.)" % (DE_STATE_NAMES[area], population[DE_STATE_NAMES[area]]))
        ax.set_xlabel('')
        ax.set_xlim(-len(rs.index), 0)
        ax.set_ylim(0, 3)

        rs = rki_r(de)
        lasts_rki.append(rs[col].tail(1).values[0])

        ax.plot(range(-len(rs.index), 0), rs[col])

    fig.set_size_inches(16,16)
    return fig, lasts, lasts_rki

def logistic_bars(lasts, title='Infektionen'):
    current_r = pd.DataFrame({'Logistic': lasts}, index=[DE_STATE_NAMES[x] for x in sorted([y for y in DE_STATE_NAMES])]).sort_values('Logistic')
    ax = current_r.plot(kind='barh',
            xlim=(min(1.0, min(lasts)), max(lasts)),
            legend=False, grid=False,
            title="Die Bundesländer im Rennen auf R=1.0\nLogistisch, %s, Stand: %s" % (title, datetime.now().strftime('%Y-%m-%d')))
    fig = ax.get_figure()
    return fig

def rki_bars(lasts_rki, title='Infektionen'):
    current_r = pd.DataFrame({'RKI': lasts_rki}, index=[DE_STATE_NAMES[x] for x in sorted([y for y in DE_STATE_NAMES])]).sort_values('RKI')
    ax = current_r.plot(kind='barh',
            xlim=(min(0.0, min(lasts_rki)), max(lasts_rki)),
            legend=False, grid=False,
            style='dark_background',
            title="Die Bundesländer im Rennen auf R=0.0\nRKI, %s, Stand: %s" % (title, datetime.now().strftime('%Y-%m-%d')))
    fig = ax.get_figure()
    return fig

def plot_press_chronic():
    de = entorb.to_dataframe('DE-total')
    
    rs1 = polynomial_r(de)
    rs2 = rki_r(de)
    news = pd.read_csv('data/chronic_de.tsv', sep="\\t", usecols=['Datum', 'Ereignis'], engine='python')
    news['Datum'] = pd.to_datetime(news['Datum'], format='%Y-%m-%d')
    news = news.set_index('Datum')

    shifted1 = rs1['Cases'].shift(-DAYS_INFECTION_TILL_SYMPTOM)
    shifted2 = rs2['Cases'].shift(-DAYS_INFECTION_TILL_SYMPTOM)
    fig, ax = plt.subplots()
    ax.plot(shifted1, shifted1.index, label='Logistisch')
    ax.plot(shifted2, shifted2.index, label='RKI')
    ax.set_title("Fall-Rate (%d Tage vorversetzt). Links: COVID-19-Chronik der FAZ" % DAYS_INFECTION_TILL_SYMPTOM)
    ax.set_yticks(news.index)
    ax.set_ylim(news.index.max() + timedelta(days=4), shifted1.index.min())
    ax.set_yticklabels(news['Ereignis'])
    ax.grid()
    ax.set_ylabel('')
                 
    plt.legend(loc='lower right')
                 
    fig.set_size_inches(9,16)
    
    return fig

def main():
    import sys
    if len(sys.argv) < 3:
        print("USAGE: %s F OUTFILE [F OUTFILE [...]]" % sys.argv[0])
        print("Values for F:")
        for i,x in enumerate([ \
                plot_rki_and_logistic_total, \
                plot_rki_and_logistic, \
                logistic_bars, \
                rki_bars, \
                plot_press_chronic]):
            print("%d: %s%s ", i, x.__name__, x.__doc__)
        sys.exit(2)

    with plt.style.context('ggplot'):
        for i in range(1, len(sys.argv), 2):
            if sys.argv[i] in ["0", plot_rki_and_logistic_total.__name__]:
                fig = plot_rki_and_logistic_total()
            elif sys.argv[i] in ["4", plot_press_chronic.__name__]:
                fig = plot_press_chronic()
            elif sys.argv[i] in ["4", plot_weekly_r.__name__]:
                fig = plot_weekly_r()
            else:
                fig, lasts, lasts_rki = plot_rki_and_logistic()
                if sys.argv[i] in ["1", plot_rki_and_logistic.__name__]:
                    """pass"""
                elif sys.argv[i] in ["2", logistic_bars.__name__]:
                    fig = logistic_bars(lasts)
                elif sys.argv[i] in ["3", rki_bars.__name__]:
                    fig = rki_bars(lasts_rki)
            print("saving", sys.argv[i+1])
            fig.savefig(sys.argv[i+1], bbox_inches='tight')
    sys.exit(0)

if __name__ == "__main__":
    main()
