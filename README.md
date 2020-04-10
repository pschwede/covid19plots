# Concerning #COVID-19

## German registry for intensive care (DIVI)

Did German hospitals exceed their capacity recently? I scraped alert data from [German registry for intensive care (DIVI)](https://www.intensivregister.de/#/intensivregister). To scrape it yourself, simply run `scrape/divi.py <outfile>`. However, feel free to use [the already scraped and continuously updated data](https://raw.githubusercontent.com/pschwede/covid19plots/master/data/divi.tsv). Also see [scrape_divi.ipynb](https://github.com/pschwede/covid19plots/blob/master/scrape_divi.ipynb) for plots.

## Total VS Week

They (who?) say that a turn in [a curve like these](https://aatishb.com/covidtrends/) signals a stopping pandemy: The more people get infected, the more people should get infected per week. However, if that trend seises to continue, the vicious circle has been stopped. See [sum_vs_window.ipynb](https://github.com/pschwede/covid19plots/blob/master/sum_vs_window.ipynb) for how German federal states behave.

## German top headlines

How did media react to COVID-19? See [topst_headlines](https://github.com/pschwede/covid19plots/blob/master/topst_headlines.ipynb).
