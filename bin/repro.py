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

    `n(t+1) = r * n(t) * (1 - n(t)/K)`
    `r = n(t+1) / (n(t) - n(t)**2)`

    Args:
        df (DataFrame): data
        population (int): total infectable population
        generation_time: delay between infections in days

    Return:
        DataFrame with reproduction rates for `Deaths` and
        `Cases`
    """
    rs = pd.DataFrame()
    for col in ['Cases']:
        try:
            earlier = df[col].shift(generation_time)
            rs[col] = (df[col] * population) / (earlier * (-df[col] + population))
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


def weekly_r(df, population):
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
        rs[col] = df[col].diff().rolling("7D").sum() / population * 1e5
    return rs


def plot_rki_and_logistic_total(state='DE-total'):
    """
    Plot rki and logistic rates for Germany.

    Args:
        state: ISO code of German district, DE-total or Country

    Return:
        Figure
    """
    global cached_dfs
    de = None
    if state not in cached_dfs:
        de = entorb.to_dataframe(state)
        cached_dfs[state] = de
    else:
        de = cached_dfs[state]

    fig, ax = plt.subplots()
    ax2 = ax.twinx()

    l = ax2.plot(de.index, de['Cases_New'].rolling('7D').mean(), color='k', label='New Cases rolling week')
    ax2.plot(de.index, de['Cases_New'], linestyle=':', color=l[0].get_color(), label='New Cases')

    poly = polynomial_r(de)['Cases']
    l = ax.plot(de.index, poly.rolling('7D').mean(), label='Logistic rate rolling week')
    ax.plot(de.index, poly, linestyle=':', color=l[0].get_color(), label='Logistic rate')

    rki = rki_r(de)['Cases']
    l = ax.plot(de.index, rki.rolling('7D').mean(), label='RKI rate rolling week')
    ax.plot(de.index, rki, linestyle=':', color=l[0].get_color(), label='RKI rate')

    plt.legend(handles=ax.lines+ax2.lines)
    ax.axhline(1.0, color='g', alpha=0.5)
    fig.set_size_inches(16,9)
    fig.tight_layout()
    return fig


def plot_r(col='Cases', population=DE_POPULATION):
    global cached_dfs
    lasts = []
    lasts_rki = []
    areas = sorted([x for x in DE_STATE_NAMES])
    fig, axes = plt.subplots(nrows=4, ncols=4, sharex=True, sharey=True)
    for i, (ax, area) in enumerate(zip(axes.flat, areas)):
        de = None
        if area in cached_dfs:
            de = cached_dfs[area]
        else:
            de = entorb.to_dataframe(area).rolling('7D').mean()
            cached_dfs[area] = de

        rs = polynomial_r(de, population[DE_STATE_NAMES[area]])
        lasts.append(rs[col].tail(1).values[0])

        ax = rs[col].plot(ax=ax, title="%s (%d Ew.)" % (DE_STATE_NAMES[area], population[DE_STATE_NAMES[area]]))
        
        rs = rki_r(de)
        lasts_rki.append(rs[col].tail(1).values[0])
        rs[col].plot(ax=ax)
        
    fig.set_size_inches(16,16)
    fig.tight_layout()
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
    global cached_dfs
    areas = sorted([x for x in DE_STATE_NAMES])
    fig, axes = plt.subplots(nrows=4, ncols=4, sharex=True, sharey=True)
    for i, (ax, area) in enumerate(zip(axes.flat, areas)):
        de = None
        if area in cached_dfs:
            de = cached_dfs[area]
        else:
            de = entorb.to_dataframe(area)
            cached_dfs[area] = de
        rs = weekly_r(de, DE_STATE_POPULATION[DE_STATE_NAMES[area]])
        rs[col].plot(ax=ax, title=DE_STATE_NAMES[area])
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
    global cached_dfs
    areas = sorted([x for x in DE_STATE_NAMES])
    lasts = {'area': areas, 'logistic': [], 'rki': [], 'weekly': []}
    fig, axes = plt.subplots(nrows=4, ncols=4, sharex=True, sharey=True)
    for i, (ax, area) in enumerate(zip(axes.flat, areas)):
        de = None
        if area in cached_dfs:
            de = cached_dfs[area].rolling('7D').mean()
        else:
            cached_dfs[area] = entorb.to_dataframe(area)
        de = cached_dfs[area].rolling('7D').mean()

        rs = polynomial_r(de, population[DE_STATE_NAMES[area]])
        lasts['logistic'].append(rs[col].values[-1])

        rs[col].plot(ax=ax, label="logistic", title="%s (%d Ew." % (DE_STATE_NAMES[area], population[DE_STATE_NAMES[area]]))

        rs = rki_r(de)
        lasts['rki'].append(rs[col].values[-1])
        rs[col].plot(ax=ax, ylim=(1,2), label="rki", sharex=True, sharey=True)

        rs = weekly_r(de, population[DE_STATE_NAMES[area]])
        lasts['weekly'].append(rs[col].values[-1])
        #ax2 = rs[col].plot(ax=ax, label="weekly", sharex=True, sharey=True, logy=True)

    fig.set_size_inches(16,16)
    return fig, pd.DataFrame(lasts).set_index('area')


def logistic_bars(lasts, title='Infektionen'):
    ax = lasts \
            .drop(columns=[x for x in lasts.columns if x != 'logistic']) \
            .sort_values('logistic') \
            .plot(kind='barh', xlim=(min(1.0, lasts['logistic'].min()),
                    lasts['logistic'].max()), legend=False, grid=False, 
                    title="Die Bundesländer im Rennen auf R=1.0\nLogistisch, %s, Stand: %s" % (title, datetime.now().strftime('%Y-%m-%d')))
    fig = ax.get_figure()
    fig.set_size_inches(9,9)
    return fig


def plot_rank(title='Inzidenz', func=weekly_r,
              states=DE_STATE_NAMES, population=DE_STATE_POPULATION):
    global cached_dfs

    fig, axes = plt.subplots(nrows=4, ncols=4, sharex=True, sharey=True)

    de = None
    for iso, state in states.items():
        if iso not in cached_dfs:
            cached_dfs[iso] = entorb.to_dataframe(iso)
        if de is None:
            de = func(cached_dfs[iso], population=population[state])
            de.drop(columns=[c for c in de.columns if c != 'Cases'])
            de.rename(columns={'Cases': state}, inplace=True)
        else:
            de[state] = func(cached_dfs[iso],
                             population=population[state])['Cases']
    rnk = de.rank(axis=1).rolling('30D').mean()

    ax_idx = 0
    for iso, state in states.items():
        rnk[state].plot(kind='line',
                        ax=axes.flat[ax_idx],
                        title=state,
                        legend=None)
        ax_idx += 1

    fig.suptitle(title)
    fig.set_size_inches(16, 16)
    fig.tight_layout()
    return fig


def rki_bars(lasts, title='Infektionen'):
    ax = lasts \
            .drop(columns=[x for x in lasts.columns if x != 'rki']) \
            .sort_values('rki') \
            .plot(kind='barh', xlim=(min(1.0, lasts['rki'].min()), 
                    lasts['rki'].max()), legend=False, grid=False, 
                    title="Die Bundesländer im Rennen auf R=0.0\nFälle nach 4 Tagen pro Infizierten, %s, Stand: %s" % (title, datetime.now().strftime('%Y-%m-%d')))
    fig = ax.get_figure()
    fig.set_size_inches(9,9)
    return fig


def weekly_bars(lasts, title="Infektionen"):
    ax = lasts \
            .drop(columns=[x for x in lasts.columns if x != 'weekly']) \
            .sort_values('weekly') \
            .plot(kind='barh', xlim=(min(1.0, lasts['weekly'].min()),
                lasts['weekly'].max()),  legend=False, grid=False,
                title="Die Bundesländer im Rennen auf R=0.0\nFälle pro Woche und 100 000 Ew., %s, Stand: %s" % (title, datetime.now().strftime('%Y-%m-%d')))
    fig = ax.get_figure()
    fig.set_size_inches(9,9)
    return fig


def plot_press_chronic():
    global cached_dfs
    de = None
    if 'DE-total' in cached_dfs:
        de = cached_dfs['DE-total']
    else:
        de = entorb.to_dataframe('DE-total')

    rs1 = polynomial_r(de)
    rs2 = weekly_r(de)
    news = pd.read_csv('data/chronic_de.tsv', sep="\\t", usecols=['Datum', 'Ereignis'], engine='python')
    news['Datum'] = pd.to_datetime(news['Datum'], format='%Y-%m-%d')
    news = news.set_index('Datum')

    fig, ax = plt.subplots()
    rs1['Cases'].transpose().plot(ax=ax, label='Logistisch')
    rs2['Cases'].transpose().plot(ax=ax, secondary_x=True, label='Wochenfälle je 100 000 Ew.')
    ax.set_title("Fall-Rate. COVID-19-Chronik der FAZ")
    ax.set_yticks(news.index)
    ax.set_ylim(news.index.max() + timedelta(days=4), rs1['Cases'].index.min())
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
        for x in [ \
                plot_rki_and_logistic_total, \
                plot_rki_and_logistic, \
                logistic_bars, \
                rki_bars, \
                weekly_bars, \
                plot_press_chronic]:
            print("%d: %s%s ", i, x.__name__, x.__doc__)
        sys.exit(2)

    with plt.style.context('ggplot'):
        done = []
        fig, lasts = plot_rki_and_logistic()
        try:
            i = sys.argv.index(plot_rki_and_logistic.__name__)
            print("saving", sys.argv[i+1])
            fig.savefig(sys.argv[i+1], bbox_inches='tight')
            done.append(plot_rki_and_logistic)
            for func in [logistic_bars, rki_bars, weekly_bars]:
                if func in done:
                    continue
                try:
                    i = sys.argv.index(func.__name__)
                    fig = func(lasts)
                    print("saving", sys.argv[i+1])
                    fig.savefig(sys.argv[i+1], bbox_inches='tight')
                    done.append(func)
                except ValueError:
                    pass
        except ValueError:
            pass
        for func in [plot_rki_and_logistic_total, plot_r, plot_weekly_r]:
            if func in done:
                continue
            try:
                i = sys.argv.index(func.__name__)
                fig = func()
                print("saving", sys.argv[i+1])
                fig.savefig(sys.argv[i+1], bbox_inches='tight')
                done.append(func)
            except ValueError:
                pass
        i = sys.argv.index("plot_rank_inzidenz")
        plot_rank(title='Gleitendes 30-Tage-Mittel des Rankings der Bundesländer über die Zeit\nInzidenz (niedriger ist besser), Daten via @entorb', func=weekly_r).savefig(sys.argv[i+1])
        i = sys.argv.index("plot_rank_logistic")
        plot_rank(title='Gleitendes 30-Tage-Mittel des Rankings der Bundesländer über die Zeit\nLogistische Reproduktionsrate (niederiger ist besser), Daten via @entorb', func=polynomial_r).savefig(sys.argv[i+1])
    sys.exit(0)

if __name__ == "__main__":
    cached_dfs = dict()
    main()
