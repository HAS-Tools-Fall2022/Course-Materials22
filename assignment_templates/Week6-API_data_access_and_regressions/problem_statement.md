# Forecasting assignment: API Data access and Regression analysis

In this forecasting assignment you'll be using APIs to download
streamflow data from the USGS database as well as analyzing it
with a basic regression model using the `scipy` package.

## Checklist:
To successfully score points for this assignment you must:

 1. Submit a python script titled `<yourname>_forecast_10-04-2022.py` to your homework respoitory under the `Forecast_Submissions` folder.
 2. This script must read the past 30 years of data for the Verde river stream gauge.
 3. You must fit a regression model that takes the historical streamflow data and week of year and estimates the streamflow in 2 weeks.
 4. Submit your streamflow forecasts for weeks beginning 10/3/2022 10/10/2022.
 
## Hints:
 - You can access the week of year as an integer with `df.index.weekofyear`
 - You can select out a particular week of year with:
    ```
    woy = 33
    df_woy = df[df.index.weekofyear == woy]
    ```
