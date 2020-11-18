#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import datetime

from common import DE_POPULATION, DAYS_INFECTION_TILL_SYMPTOM
from scrape import entorb
from repro import polynomial_r

FUTURE_RANGE = 5 * 365

def plot_projection(de, population, col='Cases', future_range=FUTURE_RANGE, LOG=False):
    """
    Plot graphs of four rates.
    """
    de = de.drop(columns=[c for c in de.columns if c != col]).rolling('7D').mean()

    now = de.reset_index()['Date'].tail(1).values[0]

    date_range = pd.date_range(start=now, \
            periods=FUTURE_RANGE/1, \
            freq="%dD" % 1)

    done = set()

    fig, axes = plt.subplots(nrows=2, sharex=True, figsize=(10,9))
    for factor, interval in [(1, 1), (1, 7), (1, 14), (4, 7)]:
        df = de * factor
        rs = polynomial_r(df, population=population, generation_time=1)
        
        r = rs[col].values[-1]

        n = list()
        for i, _ in enumerate(date_range):
            if i == 0:
                n.append(df[col].tail(1).values[0])
                continue
            n.append(r * n[-1] * (1. - n[-1]/population))

        proj_col = "Projected %s%s (last %dD avg rate)" % (col, '' if factor==1 else (' x' + str(factor) + ', '), interval)
        proj = pd.DataFrame({ 'Date': date_range, proj_col: n }) \
                .set_index('Date')

        for d,c in [(df, col), (proj, proj_col)]:
            if (c, factor) in done:
                continue
            d[c].plot(ax=axes[0], logy=LOG, label=(("%s x%d" % (c, factor)) if (c==col and factor!=1) else c))
            d[c].diff(1).plot(ax=axes[1], logy=LOG, label=("%s x%d" % (c, factor)) if (c==col and factor!=1) else c)
            done.add((c, factor))

    axes[0].grid()
    axes[0].set_ylabel("Total")
    axes[1].grid()
    axes[1].set_ylabel("Daily")
    axes[1].legend(handles=axes[1].lines, loc='best')

    fig.suptitle(("COVID-19 spread projection using Logistic map\n"
        "assuming a carrying capacity of K=%dM people and dt=%dD tick time.\n"
        "created: %s"
        "author: @pschwede, "
        "source: JHU CSSE via @entorb & @pomber.") \
                % (population/1e6, DAYS_INFECTION_TILL_SYMPTOM, str(now)[:10]))

    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.autofmt_xdate()
    return fig


def main():
    import sys
    if len(sys.argv) < 2:
        print("USAGE: %s OUTFILE" % sys.argv[0])
        sys.exit(2)
    de = entorb.to_dataframe('DE-total')
    with plt.style.context('ggplot'):
        plot_projection(de, DE_POPULATION).savefig(sys.argv[1], bbox_inches='tight')


if __name__ == "__main__":
    main()

