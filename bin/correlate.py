#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
from qwikidata.sparql \
import return_sparql_query_results
from scrape import entorb


def plot_correlation():
    # https://query.wikidata.org/
    dictlist = return_sparql_query_results("""
    SELECT DISTINCT ?code ?population ?area ?ppp ?ngdp ?growth ?totrsv ?hdi ?medinc ?literacy ?life_expectancy ?fertility_rate
    {
      ?country wdt:P31 wd:Q3624078 ;
               wdt:P297 ?code ;
               wdt:P2046 ?area ;
               wdt:P1082 ?population .
        OPTIONAL {
               ?country wdt:P4010 ?ppp .
               ?country wdt:P2131 ?ngdp .
               ?country wdt:P2219 ?growth .
               ?country wdt:P2134 ?totrsv .
               ?country wdt:P1081 ?hdi .
               ?country wdt:P3529 ?medinc .
               ?country wdt:P6897 ?literacy .
               ?country wdt:P2250 ?life_expectancy .
               ?country wdt:P4841 ?fertility_rate .
        }
    }
    """)['results']['bindings']
    df = pd.DataFrame({
        k: [x[k]['value'] if k is 'code' else float(x[k]['value']) if k in x else None for x in dictlist] \
                for k in ['code', 'population', 'area', 'ppp', 'ngdp', 'growth', 'totrsv', 'hdi', 'medinc', 'literacy', 'life_expectancy', 'fertility_rate']}) \
                            .set_index('code')
    df['density'] = df['population']/df['area']
    df['ngdp/p'] = df['ngdp'] / df['population']
    df['ppp/p'] = df['ppp'] / df['population']
    df['growth/p'] = df['growth'] / df['population']
    df['totrsv/p'] = df['totrsv'] / df['population']
    df['hdi/p'] = df['hdi'] / df['population']

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

    ncols=int((len(df.columns)-1)/4+1)
    fig, axes = plt.subplots(ncols=ncols, nrows=4)
    for ax,col in zip(axes.flat, [c for c in df.columns if c not in cols]):
        df.plot(kind='scatter', y='Deaths_Per_Million', logy=True, x=col, sharey=True, ax=ax)
    fig.set_size_inches(16, 4*ncols)
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
