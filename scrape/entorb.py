#!/usr/bin/env python

"""
Load data from entorb's corona project
"""

import pandas as pd

def to_dataframe(federal_state) -> pd.DataFrame:
    """
    Load data by @entorb

    Args:
        federal_state: One of DE, BW, BY, BE, BB, HB, HH, HE, MV, NI, NW, RP, SL, SN, ST, SH, TH

    Returns:
        A fully functional pandas.DataFrame.
    """
    result = pd.read_csv(("https://raw.githubusercontent.com/entorb/"
                          "COVID-19-Coronavirus-German-Regions/master/data/"
                          "de-states/de-state-BUNDESLAND.tsv").replace("BUNDESLAND", federal_state),
                         index_col=0,
                         sep="\t")
    result['Date'] = pd.to_datetime(result['Date'], format="%Y-%m-%d")
    return result.set_index('Date')


if __name__ == "__main__":
    print(to_dataframe("SN"))
