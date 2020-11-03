### Sources

[**entorb:**](../bin/scrape/entorb.py) Converts data from RKI via [swildermann/COVID-19](https://github.com/swildermann/COVID-19) and [ArcGIS Covid19 RKI Sums](https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/) and from JHU CSSE from [pomber/codi19](https://github.com/swildermann/COVID-19) to csv and json. It serves a lot of different pre-computed data: `Date`, `Days_Past`, `Cases`, `Deaths`, `Cases_New`, `Deaths_New`, `Cases_Last_Week` , `Deaths_Last_Week` , `Cases_Per_Million` ,`Deaths_Per_Million`, `Cases_New_Per_Million`, `Deaths_New_Per_Million`, `Cases_Last_Week_Per_Million` , `Deaths_Last_Week_Per_Million`, `Cases_Doubling_Time`, `Deaths_Doubling_Time`

[**risklayer:**](../bin/scrape/risklayer.py) Loads the CSV from [Risklayer](https://risklayer-explorer.com) in Karlsruhe, Germany. With the help of volunteers, they gather data directly from German health offices.

[**rki:**](../bin/scrape/rki.py) Uses ArcGIS [(PYPI)](https://pypi.org/project/arcgis/) to load the data from [corona.rki.de](https://corona.rki.de) or loads a copy of it. Sadly, I couldn't figure out yet how to use the data as it has very different columns than the other two. Also, it takes way too much time to load.

#### Comparison

![Charts showing differences between the three sources above.](../img/sources_deltas.png)
