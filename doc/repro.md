### Reproduction rate

Here, the reproduction rate is computed using the [logistic map](https://en.wikipedia.org/wiki/Logistic_map):

`n(t+1) = r*n(t)*(1-n(t))`

[Solving for r](https://www.wolframalpha.com/input/?i=Solve+n%28t%2B1%29+%3D+r*n%28t%29*%281-n%28t%29%29+for+r):

`r = n(t+1) / (n(t)-n²(t))`

This r-value has a way smoother curve (red) than the 4-days incidence (blue), the RKI first suggested:

![RKI & Logistic Rates Chart](../img/rki_and_logistic.svg)

#### German federated states race against the pandemic

![German districts in the race to 0.0](../img/rki_bars.svg)
![German districts in the race to 1.0](../img/logistic_bars.svg)
![German districts ranked over time (Logistic rate)](../img/plot_rank_logistic.svg)
![German districts in the race to 0.0](../img/weekly_bars.svg)
![German districts ranked over time (Inzidenz)](../img/plot_rank_inzidenz.svg)
