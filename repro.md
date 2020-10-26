#### Reproduction rate

Here, the reproducation rate is computed using the [logistic map](https://en.wikipedia.org/wiki/Logistic_map):

`n(t+1) = r*n(t)*(1-n(t))`

Solving for r, I [got](https://www.wolframalpha.com/input/?i=Solve+n%28t%2B1%29+%3D+r*n%28t%29*%281-n%28t%29%29+for+r):

`r = n(t+1) / (n(t)-n²(t))`

