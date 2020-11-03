### Sources

[**entorb:**](../bin/scrape/entorb.py) Converts data from the RKI via [swildermann/COVID-19](https://github.com/swildermann/COVID-19) and [ArcGIS Covid19 RKI Sums](https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/) and JHU CSSE from  [pomber/codi19](https://github.com/swildermann/COVID-19) to csv. `Date`, `Days_Past`, `Cases`, `Deaths`, `Cases_New`, `Deaths_New`, `Cases_Last_Week` , `Deaths_Last_Week` , `Cases_Per_Million` ,`Deaths_Per_Million`, `Cases_New_Per_Million`, `Deaths_New_Per_Million`, `Cases_Last_Week_Per_Million` , `Deaths_Last_Week_Per_Million`, `Cases_Doubling_Time`, `Deaths_Doubling_Time`

[**rki**:](../bin/scrape/rki.py) Uses ArcGIS [(PYPI)](https://pypi.org/project/arcgis/) to load the official  or loads a copy of it.

[**risklayer**:](../bin/scrape/risklayer.py) Loads the CSV from [Risklayer](https://risklayer-explorer.com) in Karlsruhe, Germany. With the help of volunteers, they gather data directly from German health offices.

Comparison

![Charts showing differences between the three sources above.](../img/sources_deltas.png)
