#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
from qwikidata.sparql \
import return_sparql_query_results
from scrape import entorb


def plot_correlation():
    # https://query.wikidata.org/
    dictlist = return_sparql_query_results("""
    SELECT DISTINCT ?code ?population ?area ?ppp ?life_expectancy ?fertility_rate
    {
      ?country wdt:P31 wd:Q3624078 ;
               wdt:P297 ?code ;
               wdt:P2046 ?area ;
               wdt:P1082 ?population .
        OPTIONAL {
               ?country wdt:P4010 ?ppp .
               ?country wdt:P2250 ?life_expectancy .
               ?country wdt:P4841 ?fertility_rate .
        }
    }
    """)['results']['bindings']
    df = pd.DataFrame({
        k: [x[k]['value'] if k is 'code' else float(x[k]['value']) if k in x else None for x in dictlist] \
                for k in ['code', 'population', 'area', 'ppp', 'life_expectancy', 'fertility_rate']}) \
                            .set_index('code')
    df['density'] = df['population']/df['area']

    cols = ['Deaths_Per_Million']
    dict_entorb = {c: [] for c in cols}
    for area in df.index:
        try:
            for col in cols:
                dict_entorb[col].append(entorb.to_dataframe(nation=area)[col].values[-1])
        except:
            for col in cols:
                dict_entorb[col].append(None)
    for col in dict_entorb:
        df[col] = dict_entorb[col]

    fig, axes = plt.subplots(ncols=2, nrows=int((len(df.columns) - 1)/2))
    for ax,col in zip(axes.flat, [c for c in df.columns if c not in cols]):
        df.plot(kind='scatter', x='Deaths_Per_Million', y=col, sharex=True, ax=ax)
    fig.set_size_inches(9, 9*(len(df.columns)-1)/4)
    return fig


def main():
    import sys
    if len(sys.argv) != 2:
        print("USAGE: %s OUTFILE" % sys.argv[0])
        sys.exit(2)
    fname = sys.argv[1]
    with plt.style.context('ggplot'):
        fig = plot_correlation()
        fig.savefig(fname, bbox_inches='tight')


if __name__ == "__main__":
    main()
