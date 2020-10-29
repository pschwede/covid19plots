#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
from scrape import entorb
from common import DE_STATE_NAMES

def lethality_plot():
    fig, axes = plt.subplots(ncols=4, nrows=4, sharey=True, sharex=True)

    for num, (ax, area) in enumerate(zip(axes.flat, DE_STATE_NAMES)):
        df = entorb.to_dataframe(area).rolling('7D').mean()
        df['Lethality_Weekly'] = df['Cases_New'].shift(-14) / df['Deaths_New'] * 100
        df['Lethality_Monthly'] = df['Cases_New'].rolling('30D').mean().shift(-14) / df['Deaths_New'].rolling('30D').mean() * 100
        p = ax.plot('Date',
                    'Lethality_Weekly',
                    data=df.reset_index(),
                    marker='',
                    linestyle=':',
                    label=DE_STATE_NAMES[area])
        ax.plot('Date',
                'Lethality_Monthly',
                data=df.reset_index(),
                marker='',
                linestyle='-',
                color=p[0].get_color(),
                label=DE_STATE_NAMES[area])
        ax.set_xlabel('Date')
        #ax.set_xscale('symlog')
        ax.set_title(DE_STATE_NAMES[area])
        ax.set_ylabel('Lethality (%)')
        ax.set_ylim(min(0,max(df['Lethality_Monthly'])))
        #ax.set_yscale('symlog')
        #ax.legend()
        #ax.grid()
    fig.suptitle("Lethality (statistical likelihood of death after 14 days after COVID-19 diagnosis)\n", fontsize=16)
    fig.set_size_inches(16,16)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.set_facecolor('w')
    return fig

def main():
    import sys
    if len(sys.argv) != 3:
        print("USAGE: %s OUTFILE" % sys.argv[0])
        sys.exit(2)
    outfile = sys.argv[1]
    with plt.style.context('ggplot'):
        lethality_plot().savefig(outfile, bbox_inches='tight')

if __name__ == "__main__":
    main()
