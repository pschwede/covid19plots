#!/usr/bin/env python

import pandas as pd

def to_dataframe(federal_state) -> pd.DataFrame:
    """
    Load data by @entorb
    
    Args:
        federal_state: One of DE , BW , BY , BE , BB , HB , HH , HE , MV , NI , NW , RP , SL , SN , ST , SH , TH
    
    Returns:
        A fully functional pandas.DataFrame.
    """
    return pd.read_csv(
        "https://raw.githubusercontent.com/entorb/COVID-19-Coronavirus-German-Regions/master/data/de-state-%s.tsv" % federal_state,
        index_col=0,
        sep="\t",
        parse_dates=True
    )