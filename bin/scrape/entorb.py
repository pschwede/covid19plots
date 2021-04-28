#!/usr/bin/env python

"""
Load data from entorb's corona project
"""

import pandas as pd

def to_dataframe(federal_state=None, nation=None) -> pd.DataFrame:
    """
    Load data from @entorb' dataset

    Args:
        federal_state: One of DE, BW, BY, BE, BB, HB, HH, HE, MV, NI, NW, RP, SL, SN, ST, SH, TH
        int_state: One of AD, AF, AG, .. CN, .. DE, .. FR, .. GB, .. US, .. ZM, ZW

    Returns:
        A fully functional pandas.DataFrame.
    """
    url = ""
    if federal_state:
        url = ("https://raw.githubusercontent.com/entorb/"
               "COVID-19-Coronavirus-German-Regions/master/data/"
               "de-states/de-state-BUNDESLAND.tsv").replace("BUNDESLAND", federal_state)
    elif nation:
        url = ("https://raw.githubusercontent.com/entorb/"
               "COVID-19-Coronavirus-German-Regions/master/data/"
               "int/country-NATION.tsv").replace("NATION", nation)
    else:
        raise Exception("Neither `federal_state` nor `country` given.")
    result = pd.read_csv(url, index_col=0, sep="\t")
    result['Date'] = pd.to_datetime(result['Date'], format="%Y-%m-%d")
    return result.set_index('Date')


if __name__ == "__main__":
    print(to_dataframe("SN"))
