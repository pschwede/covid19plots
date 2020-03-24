#!/usr/bin/env python

"""
General tools for scraping
"""
from typing import Dict, Union
from time import sleep

import requests


def retry_getting(html: str = None,
                  json: str = None,
                  params: Dict = None,
                  retries: int = 10) -> Union[str, object]:
    """
    Download either an HTML document or a JSON object depending on given
    arguments using POST-request.  When failing, retries until with delay.
    Delay doubles with each retry.

    Args:
        html: url of an HTML document
        json: url of an JSON object
        params: dictionary of HTTP request paramters
        retries: max number of retries (default: 10)

    Returns:
        html if argument was given; otherwise a json object.
    """
    params = params if params else {}

    delay = 200 # milliseconds
    while retries:
        resp = requests.post(html if html else json, params=params)
        if resp.status_code == 200:
            return resp.text if html else resp.json
        sleep(delay)
        delay *= 2
        retries -= 1
    raise Exception("No response.")
