#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
from scrape import entorb
from common import DE_STATE_NAMES, DAYS_SYMPTOMS_TILL_DEATH

def lethality_plot(federal_state=None, nation='DE', ax=None):
    resolutions = {'Weekly': 7, 'Monthly': 30}
    with pd.option_context('mode.use_inf_as_na', True):
        df = entorb.to_dataframe(federal_state, nation) \
                .filter(items=['Deaths_New', 'Cases_New'])
        for title, days in resolutions.items():
            df[title] = df['Deaths_New'].rolling(days).sum()
            df[title] /= df['Cases_New'].shift(DAYS_SYMPTOMS_TILL_DEATH) \
                .rolling(days).sum()
            df[title] *= 100
            df[title] = df[title].dropna()
        ax = df.filter([x for x in resolutions]) \
                .plot(kind='line', \
                ax=ax, \
                legend=False, \
                sharex=True, sharey=True, \
                title=nation if nation else DE_STATE_NAMES[federal_state])
        ax.set_ylim(0, df['Monthly'].max())
        return ax.get_figure()

def lethality_mass_plot(federal_states=[x for x in DE_STATE_NAMES], nations=None):
    areas = nations if nations else federal_states
    ncols=min(int(len(areas)**0.5), 4)
    nrows=round(len(areas) / ncols)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, \
            sharex='all', sharey='all', \
            squeeze=True)
    for (area, ax) in zip(areas, axes.flat):
        if nations:
            lethality_plot(nation=area, ax=ax)
        else:
            lethality_plot(federal_state=area, nation=None, ax=ax)
        ax.set_xlabel(None)
    fig.suptitle("Lethality (%) (statistical likelihood of death after 14 days after COVID-19 diagnosis)", fontsize=16)
    fig.set_size_inches(4*ncols, 4*nrows)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig

def main():
    import sys
    if len(sys.argv) != 3:
        print("USAGE: %s FUNC OUTFILE" % sys.argv[0])
        sys.exit(2)
    outfile = sys.argv[2]
    with plt.style.context('ggplot'):
        if sys.argv[1] in ["1", lethality_mass_plot.__name__]:
            fig = lethality_mass_plot()
        elif sys.argv[1] in ["2", lethality_plot.__name__]:
            fig = lethality_plot()
        fig.savefig(outfile, bbox_inches='tight')

if __name__ == "__main__":
    main()
