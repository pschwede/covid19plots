#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import datetime

from common import DE_POPULATION, DAYS_INFECTION_TILL_SYMPTOM
from scrape import entorb
from repro import polynomial_r

FUTURE_RANGE = 5 * 365

def plot_projection(col='Cases', future_range=FUTURE_RANGE, LOG=False):
    """
    Plot graphs of four rates.
    """
    de = entorb.to_dataframe('DE-total')
    de = de.drop(columns=[c for c in de.columns if c != col]).rolling('7D').mean()

    now = de[col].index[-1]

    date_range = pd.date_range(start=de[col].index[-1], \
            periods=FUTURE_RANGE/DAYS_INFECTION_TILL_SYMPTOM, \
            freq="%dD" % DAYS_INFECTION_TILL_SYMPTOM)

    done = []

    fig, axes = plt.subplots(nrows=2, sharex=True, figsize=(10,9))
    for factor, interval in [(1, 1), (1, 7), (1, 14), (4, 7)]:
        df = de * factor if factor != 1 else de
        
        rs = polynomial_r(df, population=DE_POPULATION, generation_time=DAYS_INFECTION_TILL_SYMPTOM)
        rlast = rs.last("%dD" % interval).mean().iloc[-1]

        ys = list()
        for i, _ in enumerate(date_range):
            if i == 0:
                ys.append(df[col].last('1D').sum())
                continue
            ys.append(max(ys[-1], rlast * ys[-1] * (1. - ys[-1]/DE_POPULATION)))

        proj_col = "Projected %s%s (last %dD avg rate)" % (col, '' if factor==1 else (' x' + str(factor) + ', '), interval)
        proj = pd.DataFrame({ 'Date': date_range, proj_col: ys }) \
                .set_index('Date') #\

        for d,c in [(df, col), (proj, proj_col)]:
            if (c, factor) not in done:
                d[c].plot(ax=axes[0], logy=LOG, label=("%s x%d" % (c, factor)) if c==col and factor!=1 else c)
                d[c].diff(1).plot(ax=axes[1], logy=LOG, label=("%s x%d" % (c, factor)) if c==col and factor!=1 else c)
            done.append((c, factor))

    axes[0].grid()
    axes[0].set_ylabel("Total")
    axes[1].grid()
    axes[1].set_ylabel("Daily")
    axes[1].legend(handles=axes[1].lines, loc='best')

    fig.suptitle(("COVID-19 spread projection using Logistic map\n"
        "assuming a carrying capacity of K=%dM people and dt=%dD tick time.\n"
        "created: %d-%02d-%02d, "
        "author: @pschwede, "
        "source: JHU CSSE via @entorb & @pomber.") \
                % (DE_POPULATION/1e6, DAYS_INFECTION_TILL_SYMPTOM, now.year, now.month, now.day))

    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.autofmt_xdate()
    return fig


def main():
    import sys
    if len(sys.argv) < 2:
        print("USAGE: %s OUTFILE" % sys.argv[0])
        sys.exit(2)
    with plt.style.context('ggplot'):
        plot_projection().savefig(sys.argv[1], bbox_inches='tight')


if __name__ == "__main__":
    main()

