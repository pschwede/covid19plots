#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt

from scrape import entorb
from scrape import rki
from scrape import risklayer


def plot_source_deltas():
    fig, axes = plt.subplots(nrows=6)

    da = entorb.to_dataframe(nation='DE')
    db = risklayer.to_dataframe(nation='DE')
    for ax,col in zip(axes.flat[:2], ['Cases', 'Cases_New']):
        (da[col]-db[col]).plot(kind='bar', label="%s, delta entorb - risklayer" % col,
                sharex=True, ax=ax)
        ax.legend()

    dc = rki.to_dataframe(nation='DE')
    for ax,col in zip(axes.flat[2:4], ['Cases', 'Cases_New']):
        (da[col]-dc[col]).plot(kind='bar', label="%s, delta entorb - rki" % col,
                sharex=True, ax=ax)
        ax.legend()

    for src in [entorb, rki, risklayer]:
        df = {entorb: da, rki: dc, risklayer: db}[src]
        for ax,col in zip(axes.flat[4:], ['Cases', 'Cases_New']):
            df[col].plot(label="%s, %s" % (col, src.__name__), sharex=True, ax=ax)
            ax.legend()

    fig.set_size_inches(16,9)
    return fig


def main():
    import sys
    if len(sys.argv) < 2:
        print("USAGE: %s OUTFILE" % sys.argv[0])
        sys.exit(2)
    fname = sys.argv[1]
    with plt.style.context('ggplot'):
        fig = plot_source_deltas()
        fig.savefig(fname, bbox_inches='tight')


if __name__ == "__main__":
    main()
