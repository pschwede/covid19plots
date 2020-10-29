#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
from scrape import entorb
from common import DE_STATE_NAMES

def lethality_plot():
    fig, axes = plt.subplots(ncols=4, nrows=4, sharey=True, sharex=True)

    for num, (ax, area) in enumerate(zip(axes.flat, DE_STATE_NAMES)):
        df = entorb.to_dataframe(area)
        df['Lethality Weekly'] = df['Deaths_New'].resample('1W').sum() / df['Cases_New'].shift(14).resample('1W').sum() * 100
        df['Lethality Monthly'] = df['Deaths_New'].resample('1M').sum() / df['Cases_New'].shift(14).resample('1M').sum() * 100
        df['Lethality Weekly'].plot(ax=ax)
        df['Lethality Monthly'].plot(ax=ax)
        ax.set_title(DE_STATE_NAMES[area])
    fig.suptitle("Lethality (%)\n(statistical likelihood of death after 14 days after COVID-19 diagnosis)\n", fontsize=16)
    fig.set_size_inches(16,16)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig

def main():
    import sys
    if len(sys.argv) != 2:
        print("USAGE: %s OUTFILE" % sys.argv[0])
        sys.exit(2)
    outfile = sys.argv[1]
    with plt.style.context('ggplot'):
        lethality_plot().savefig(outfile, bbox_inches='tight')

if __name__ == "__main__":
    main()
