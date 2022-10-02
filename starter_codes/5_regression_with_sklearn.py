#%%
import urllib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# A NEW THING!!!
from sklearn.linear_model import LinearRegression

# %%
def create_usgs_url(site_no, begin_date, end_date):
    return (f'https://waterdata.usgs.gov/nwis/dv?'
        f'cb_00060=on&format=rdb&referred_module=sw&'
        f'site_no={site_no}&'
        f'begin_date={begin_date}&'
        f'end_date={end_date}')

def open_usgs_data(site, begin_date, end_date):
    url = create_usgs_url((site), begin_date, end_date)
    response = urllib.request.urlopen(url)
    df = pd.read_table(
        response, comment='#', skipfooter=1, delim_whitespace=True,
        names=['agency', 'site', 'date', 'streamflow', 'quality_flag'],
        index_col=2, parse_dates=True).iloc[2:]
    df['streamflow'] = df['streamflow'].astype(np.float64)
    df.index = pd.DatetimeIndex(df.index)
    return df

def open_daymet_data(lat, lon, begin_date, end_date):
    args = {'lat':  lat, 'lon': lon, 'format': 'csv',
            'start': begin_date, 'end': end_date}
    query = urllib.parse.urlencode(args)
    url = f"https://daymet.ornl.gov/single-pixel/api/data?{query}"
    response = urllib.request.urlopen(url)
    df = pd.read_csv(response, header=6)
    datestring = (df['year'].astype(str) + df['yday'].astype(str))
    dates = pd.to_datetime(datestring, format='%Y%j')
    df.index = pd.DatetimeIndex(dates)
    return df


#%%
site = '09506000'
begin_date = '2000-09-25'
end_date = '2022-09-25'
lat = 34.4483605
lon = -111.7898705

daymet_df = open_daymet_data(lat, lon, begin_date, end_date)
daymet_df.head()
verde_df = open_usgs_data(site, begin_date, end_date)
daymet_df = daymet_df.reindex(verde_df.index)
daymet_df['streamflow'] = verde_df['streamflow']
df = daymet_df
df.head()


# %%
df_monthly = df.resample('M').mean()
df_monthly = df_monthly.dropna()
df_monthly.plot.scatter(x='tmax (deg c)', y='streamflow')
plt.semilogy()


#%% 
lm = LinearRegression()
x = df_monthly[['tmax (deg c)']]
y = df_monthly[['streamflow']]
lm.fit(x, y)
xfit = np.linspace(np.min(x), np.max(x), 20).reshape(-1, 1)
yfit = lm.predict(xfit)

df_monthly.plot.scatter(x='tmax (deg c)', y='streamflow')
plt.plot(xfit, yfit, color='red')
plt.semilogy()


# %%
log_lm = LinearRegression()
x = df_monthly[['tmax (deg c)']]
ylog = np.log(df_monthly[['streamflow']])
log_lm.fit(x, ylog)

xfit = np.linspace(np.min(x), np.max(x), 20).reshape(-1, 1)
# Remember we fit on log values, so we need to transform
# from log(streamflow) -> streamflow via the `np.exp` call
yfit_log = np.exp(log_lm.predict(xfit))

df_monthly.plot.scatter(x='tmax (deg c)', y='streamflow')
plt.plot(xfit, yfit_log, color='maroon', label='fit on log values')
plt.plot(xfit, yfit, color='darkgoldenrod', linestyle='--', label='fit on raw values')
plt.legend()
plt.semilogy()

#%%

log_score = log_lm.score(x, ylog)
reg_score = log_lm.score(x, y)

print(log_score, reg_score)

# %%

c = log_lm.coef_
i = log_lm.intercept_
print(c, i)

# %%
