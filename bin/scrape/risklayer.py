#!/usr/bin/env python

import requests
import pandas as pd
from datetime import datetime

def AGS_to_BL(ags):
    return "SH,HH,NI,HB,NW,HE,RP,BW,BY,SL,BE,BB,MV,SN,ST,TH".split(",")[int(ags[:2])-1]

def to_dataframe(federal_state=None, nation=None) -> pd.DataFrame:
    if nation and nation != 'DE':
        return None
    df = pd.read_csv("http://www.risklayer-explorer.com/media/data/events/GermanyValues.csv") \
            .iloc[:-3] # removes credits
    if not nation and not federal_state:
        return df
    idx = [datetime.strptime(x[:10], "%d.%m.%Y") for x in
            df.transpose() \
                    .drop(['AGS','ADMIN','Population']) \
                    .index]
    result = pd.DataFrame({'Date': idx})
    if nation and not federal_state:
        result['Cases'] = df \
                .drop(columns=['AGS','ADMIN','Population']) \
                .sum().values
    if not nation and federal_state:
        df['BL'] = [AGS_to_BL(x) for x in df['AGS']]
        result['Cases'] = df.loc[df['BL'] == federal_state] \
                .drop(columns=['AGS','ADMIN','Population', 'BL']) \
                .sum().values
    result['Cases_New'] = result['Cases'] - result['Cases'].shift(1)
    return result.set_index('Date')

if __name__ == "__main__":
    print(to_dataframe())
    print(to_dataframe(nation='DE'))
    print(to_dataframe(federal_state='SN'))
