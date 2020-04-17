# Concerning #COVID-19

## Trends

### Reproduction rate

[repro.ipynb](https://github.com/pschwede/covid19plots/blob/master/repro.ipynb) computes the logistic reproduction rate for each German federal state.

### Total VS Week

They (who?) say that a turn in [a curve like these](https://aatishb.com/covidtrends/) signals a stopping pandemy: The more people get infected, the more people should get infected per week. However, if that trend seises to continue, the vicious circle has been stopped. See [sum_vs_window.ipynb](https://github.com/pschwede/covid19plots/blob/master/sum_vs_window.ipynb) for how German federal states behave.

## Correlations

### General
[scatter_matrix.ipynb](https://github.com/pschwede/covid19plots/blob/master/scatter_matrix.ipynb) also includes an attempt to model the total number of deaths using the total number of cases.

### Fertility rate
[fertility.ipynb](https://github.com/pschwede/covid19plots/blob/master/fertility.ipynb) looks for fertility rates of German federal states correlated with COVID-19 cases. R²=0.311 is low.

### German registry for intensive care (DIVI)

Did German hospitals exceed their capacity recently? I scraped alert data from [German registry for intensive care (DIVI)](https://www.intensivregister.de/#/intensivregister). To scrape it yourself, simply run `scrape/divi.py <outfile>`. However, feel free to use [the already scraped and ~~continuously~~ updated data](https://raw.githubusercontent.com/pschwede/covid19plots/master/data/divi.tsv). Also see [scrape_divi.ipynb](https://github.com/pschwede/covid19plots/blob/master/scrape_divi.ipynb) for plots.

## Other

### German top headlines

How did media react to COVID-19? See [topst_headlines](https://github.com/pschwede/covid19plots/blob/master/topst_headlines.ipynb).
