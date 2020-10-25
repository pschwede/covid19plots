#!/usr/bin/env python

from typing import List
import pandas as pd
from mastodon import Mastodon

def to_dataframe(user:str = 'secrets/topstbot.user.secret',
                 url:str = 'https://botsin.space',
                 since: str = '2020-03-01T00:00:00.000Z',
                 tagged:List[str] = ['de', 'day']) -> pd.DataFrame:
    """
    Fetch all posts that are tagged with [tagged].
    """
    
    mastodon = Mastodon(access_token=user, api_base_url=url)
    my_id = mastodon.me()['id']
    since_date = pd.to_datetime(since)
    statuses = mastodon.account_statuses(my_id)
    while pd.to_datetime(statuses[-1]['created_at']) > since_date:
        statuses += mastodon.account_statuses(my_id, max_id=statuses[-1]['id'])
    
    headers = ['created_at', 'content', 'url']
    columns = {h: [] for h in headers}
    
    for status in statuses:
        if len(set([s.name for s in status['tags']]).intersection(set(tagged)))!=len(tagged):
            continue
            
        columns[headers[0]].append(status[headers[0]])
        columns[headers[1]].append(status[headers[1]])
        columns[headers[2]].append(status[headers[2]])
        
    result = pd.DataFrame(columns, columns=headers)
    result[headers[0]] = pd.to_datetime(result[headers[0]])
    return result.set_index(headers[0])