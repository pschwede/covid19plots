#!/usr/bin/env python

"""
Scrape German register for intensive care (DIVI)
"""

import sys
import argparse
import logging
from typing import Callable
from os import path
from io import StringIO
import requests
import numpy as np
import pandas as pd


TRANSLATE_AVAILABILITY = {'VERFUEGBAR': 1.0, 'BEGRENZT': 0.5, 'NICHT_VERFUEGBAR': 0.0, 'UNBEKANNT': np.nan}
TRANSLATE_FEDERAL_STATE = {
        'BADEN_WUERTTEMBERG': "BW",
        'BAYERN': "BY",
        'BERLIN': "BE",
        'BRANDENBURG': "BB",
        'BREMEN': "HB",
        'HAMBURG': "HH",
        'HESSEN': "HE",
        'MECKLENBURG_VORPOMMERN': "MV",
        'NIEDERSACHSEN': "NI",
        'NORDRHEIN_WESTFALEN': "NW",
        'RHEINLAND_PFALZ': "RP",
        'SAARLAND': "SL",
        'SACHSEN': "SN",
        'SACHSEN_ANHALT': "ST",
        'SCHLESWIG_HOLSTEIN': "SH",
        'THUERINGEN': "TH",
        }


def to_dataframe(mapping: Callable[[str], float] = TRANSLATE_AVAILABILITY.get) -> pd.DataFrame:
    response = requests.get("https://www.intensivregister.de/api/public/intensivregister?page=0&size=2000")
    response_json = response.json()
    headers = ['Klinikname', 'Bundesland', 'ICU low care', 'ICU high care', 'ECMO', 'Stand', 'COVID-19 cases']
    columns = {h: [] for h in headers}
    for row in response_json['data']:
        columns[headers[0]].append(row['krankenhausStandort']['bezeichnung'])
        columns[headers[1]].append(TRANSLATE_FEDERAL_STATE[row['krankenhausStandort']['bundesland']])
        columns[headers[2]].append(mapping(row['bettenStatus']['statusLowCare']))
        columns[headers[3]].append(mapping(row['bettenStatus']['statusHighCare']))
        columns[headers[4]].append(mapping(row['bettenStatus']['statusECMO']))
        columns[headers[5]].append(row['meldezeitpunkt'])
        columns[headers[6]].append(row['faelleCovidAktuell'])
    result = pd.DataFrame(columns, columns=headers)
    result['Stand'] = pd.to_datetime(result['Stand'])
    result = result.set_index('Stand')
    return result.drop_duplicates().tz_localize(None)


def __main() -> int:
    """
    Scrape most recent table and store it to file with in tab-separated values format.

    Returns:
        0 if new data has been received (update successful)
        1 if data has been received that is not new (no update)
        2 if an error occured (failure)
    """
    desc = "Scrape most recent table and save it in file with tab-separated values."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("outfile",
                        nargs='?',
                        default=None,
                        help="Appendable output file. Will print to stdout if not given.")
    parser.add_argument("-v", "--verbose",
                        default=0,
                        action="count")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)s %(message)s',
                        level=[logging.ERROR, logging.INFO][args.verbose] \
                        if args.verbose < 3 else logging.DEBUG)

    # Download recent data
    data = to_dataframe().reset_index()

    # Append existing data
    logging.debug("shape before: %s", data.shape)
    if args.outfile and path.exists(args.outfile):
        logging.debug("loading file %s" % args.outfile)
        try:
            with open(args.outfile, 'r') as outfile:
                appendix = pd.read_csv(outfile, sep="\t", index_col=0, parse_dates=True) \
                        .drop(columns=['Stand'])
                data = data.append(appendix, ignore_index=True)
        except pd.errors.EmptyDataError as exc:
            logging.debug(exc)
        except IOError as exc:
            logging.fatal(exc)
            return 2
    data = data.drop_duplicates().set_index('Stand')
    logging.debug("shape after: %s", data.shape)

    # Print to stdout unless outfile given.
    if not args.outfile:
        # workaround pandas issue writing to sys.stdout: https://stackoverflow.com/a/51201819
        logging.debug("writing to stdout")
        output = StringIO()
        data.to_csv(output, sep="\t", header=True)
        output.seek(0)
        print(output.read())
        return 0

    logging.debug("writing to %s" % args.outfile)
    try:
        with open(args.outfile, 'w') as outfile:
            data.to_csv(outfile, sep="\t", header=True)
        return 0
    except IOError as exc:
        logging.getLogger().fatal(exc)
        return 2


if __name__ == "__main__":
    sys.exit(__main())
