#!/usr/bin/env python

"""
Scrape German register for intensive care (DIVI)
"""

import sys
import argparse
import logging
from datetime import datetime
from os import path
from io import StringIO
import lxml.html.soupparser as soupparser
import numpy as np
import pandas as pd

import scrape


def to_dataframe(html: str) -> pd.DataFrame:
    """
    Turn html table into into a pandas DataFrame.
    * respects <small/>-tags in first column
    * respects classes of <span/>-tags in columns where there's no content
    * empty cells will be contained as empty strings `""`
    * converts dates in last column to datetime objects

    Args:
        html: string that contains HTML with a table.

    Returns:
        A fully functional pandas.DataFrame.
    """
    stress = {'green': 1.0, 'yellow': 0.5, 'red': 0.0, 'unavailable': np.nan}

    result = list()
    table = soupparser.fromstring(html) \
            .xpath("/html/body/div/div/div/div/div/div/form/div/div/table")[0]

    headers = [x.text_content().strip() for x in table.xpath("thead//th")]
    result = {head: [] for head in headers}

    for table_row in table.xpath("tbody/tr"):
        for i, cell in enumerate(table_row.xpath("td")):
            cell_content = cell.text_content().replace("\n", " ")

            # first column contains <small/> tags
            if i == 0:
                smalls = cell.xpath("small")
                texts = [cell.text]
                texts += [s.text for s in smalls if len(s) and s.text]
                cell_content = ", ".join(texts)

            cell_content = cell_content.strip()

            # there are three columns that contain just <span/> tags with specific classes
            spans = cell.xpath("span")
            if spans:
                cell_content = stress[spans[0].get('class').replace("hr-icon-", '')]

            if i == 6:
                cell_content = datetime.strptime(cell_content, '%d.%m.%Y %H:%M')

            result[headers[i]].append(cell_content)

    return pd.DataFrame(result)


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
    html = scrape.retry_getting(
        html="https://divi.de/register/intensivregister?view=items",
        params={"filter[search]": "",
                "list[fullordering]": "a.title+ASC",
                "list[limit]": 0,
                "filter[federalstate]": 0,
                "filter[chronosort]": 0,
                "filter[icu_highcare_state]": "",
                "filter[ecmo_state]": "",
                "filter[ards_network]": "",
                "limitstart": 0,
                "task": "",
                "boxchecked": 0,
                "07b860ef6bacf3cbfc30dc905ef94486": 1})
    data = to_dataframe(html)

    # Append existing data
    shape = data.shape
    logging.debug("shape before: %s", shape)
    if args.outfile and path.exists(args.outfile):
        try:
            with open(args.outfile, 'r') as outfile:
                try:
                    appendix = pd.read_csv(outfile, sep="\t", index_col=0, parse_dates=True)
                    data = data.append(appendix, ignore_index=True)
                except pd.errors.EmptyDataError:
                    shape = (0, 0)
        except IOError as exc:
            logging.fatal(exc)
            return 2
    data = data.drop_duplicates()
    logging.debug("shape after: %s", data.shape)

    # Print to stdout unless outfile given.
    if args.outfile:
        if shape == data.shape:
            return 1
        try:
            with open(args.outfile, 'w') as outfile:
                data.to_csv(outfile, sep="\t", header=True)
            return 0
        except IOError as exc:
            logging.getLogger().fatal(exc)
            return 2

    # workaround pandas issue writing to sys.stdout: https://stackoverflow.com/a/51201819
    output = StringIO()
    data.to_csv(output, sep="\t", header=True)
    output.seek(0)
    print(output.read())
    return 0


if __name__ == "__main__":
    sys.exit(__main())
