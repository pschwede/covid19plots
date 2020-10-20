# Trends

#### Countries in comparison

Did you know that apparently 3x more people per million died due to COVID-19 in Sweden than in Germany? [countries_in_comparison.ipynb](https://github.com/pschwede/covid19plots/blob/master/countries_in_comparison.ipynb)

#### Reproduction rate

What's the logistic reproduction rate for each German federal state? [repro.ipynb](https://github.com/pschwede/covid19plots/blob/master/repro.ipynb)

#### Mortality rate

Most deaths happen after days after being diagnosed positively for COVID-19. [letality.ipynb](https://github.com/pschwede/covid19plots/blob/master/letality.ipynb) assumes that time span being 14 days across all patients. (Also see [scatter_matrix.ipynb](https://github.com/pschwede/covid19plots/blob/master/scatter_matrix.ipynb))

#### Projection

What will the COVID-19 future look like? [projection.ipynb](https://github.com/pschwede/covid19plots/blob/master/projection.ipynb)

A similar approaches:

* https://www.sciencedirect.com/science/article/pii/S1201971220303039
* https://medium.com/analytics-vidhya/predicting-the-spread-of-covid-19-coronavirus-in-us-daily-updates-4de238ad8c26
#### Total VS Week

They (who?) say that a turn in [a curve like these](https://aatishb.com/covidtrends/) signals a stopping pandemy: The more people get infected, the more people should get infected per week. However, if that trend seises to continue, the vicious circle has been stopped. See [sum_vs_window.ipynb](https://github.com/pschwede/covid19plots/blob/master/sum_vs_window.ipynb) for how German federal states behave.

# Correlations

#### General
[scatter_matrix.ipynb](https://github.com/pschwede/covid19plots/blob/master/scatter_matrix.ipynb) also includes an attempt to model the total number of deaths using the total number of cases.

Do corona virus spreaders like youngsters immunitize the oldr population against COVID19? [correlate.ipynb](https://github.com/pschwede/covid19plots/blob/master/correlate.ipynb) looks for fertility rates of German federal states VS COVID-19 cases.

#### German registry for intensive care (DIVI)

Did German hospitals exceed their capacity recently? I scraped alert data from [German registry for intensive care (DIVI)](https://www.intensivregister.de/#/intensivregister). To scrape it yourself, simply run `scrape/divi.py <outfile>`. However, feel free to use [the already scraped and ~~continuously~~ updated data](https://raw.githubusercontent.com/pschwede/covid19plots/master/data/divi.tsv). Also see [scrape_divi.ipynb](https://github.com/pschwede/covid19plots/blob/master/scrape_divi.ipynb) for plots.

# Other

#### German top headlines

How did media react to COVID-19? See [topst_headlines](https://github.com/pschwede/covid19plots/blob/master/topst_headlines.ipynb).
