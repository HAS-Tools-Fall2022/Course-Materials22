#%%
import urllib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%%
# A quick detour on 'f-strings'
# In python there is a really nice way to insert values 
# from variables into a string variable. This task is 
# referred to in programming as string formatting. In the
# past there were other ways to do this in python, but 
# a few years ago they added this approach which is generally
# seen as the best way to do this. For an overview see this:
# - https://realpython.com/python-f-strings/
#
random_numbers = np.random.random(5)
print('The average of my random numbers is', np.mean(random_numbers))
print(f'The average of my random numbers is {np.mean(random_numbers)}')


#%%
# With that out of the way let's start to work towards being able
# to grab data on the fly from the USGS website. And now we've defined
# the site id for the Verde River, as well as some start and end dates
# to get the data for. With those defined clearly it makes it much
# easier for someone else to understand what you are trying to do.
args = {
    'site_no': '09506000',
    'begin_date': '2021-09-25',
    'end_date': '2022-09-25'
}
query = urllib.parse.urlencode(args)

# Now we can use f-strings to insert these values into the query URL
# which will point to the same website that we saw in the lecture portion
# You can verify this by copying the URL into your web browser.
verde_url = (
    f'https://waterdata.usgs.gov/nwis/dv?'
    f'cb_00060=on&format=rdb&referred_module=sw&{query}'
)
print(verde_url)


#%%
# With that we need to download the data and get it into pandas.
# To download the data we'll use the `urllib` module which is 
# built into the python "standard library" of stuff you get for
# free when you install python. We use the `urllib.request.urlopen`
# function which simply opens a connection to the url, just like 
# going to the url in your web browser. Then, we can put the `response`
# into `pd.read_table`. There are a lot of other parameters going 
# into this function now, and this is very common for when you scrape
# data directly from the internet because formats vary.
# 
# Anyways, let's walk through a few of them:
#  - comment='#': Lines beginning with a '#' are comments that pandas should ignore
#  - skipfooter=1: Skip the last line, not including this leads to no data ¯\_( ツ )_/¯
#  - delim_whitespace=True: The data representing columns are separated by white space
#  - names: The names of the columns. I set these because the USGS ones are trash
#  - index_col=2: Set the 3rd column as the index (that is, "date")
#  - parse_dates=True: Try to make dates the correct data type, didn't work here but a good idea

response = urllib.request.urlopen(verde_url)
df = pd.read_table(
    response,
    comment='#',
    skipfooter=1,
    delim_whitespace=True,
    names=['agency', 'site', 'date', 'streamflow', 'quality_flag'],
    index_col=2,
    parse_dates=True
).iloc[2:]

# Now convert the streamflow data to floats and
# the index to datetimes. When processing raw data
# it's common to have to do some extra postprocessing
df['streamflow'] = df['streamflow'].astype(np.float64)
df.index = pd.DatetimeIndex(df.index)
df.head()


# %%
# And voila - we have a nice dataframe with streamflow data in it
# You can do all of the standard pandas stuff
df['streamflow'].plot()
plt.semilogy()
plt.ylabel('Streamflow [cfs]')
plt.xlabel('')


# %%
# Now, you might be thinking... why only one year of data?!
# And that's a great question. Before getting too far, let's
# just turn our little data processing things into some helper
# functions to save space, and make this easier for you to port
# to your homework
def create_usgs_url(site_no, begin_date, end_date):
    return (
        f'https://waterdata.usgs.gov/nwis/dv?'
        f'cb_00060=on&format=rdb&referred_module=sw&'
        f'site_no={site_no}&'
        f'begin_date={begin_date}&'
        f'end_date={end_date}'
    )

def open_usgs_data(site, begin_date, end_date):
    url = create_usgs_url((site), begin_date, end_date)
    response = urllib.request.urlopen(url)
    df = pd.read_table(
        response,
        comment='#',
        skipfooter=1,
        delim_whitespace=True,
        names=['agency', 'site', 'date', 'streamflow', 'quality_flag'],
        index_col=2,
        parse_dates=True
    ).iloc[2:]

    # Now convert the streamflow data to floats and
    # the index to datetimes. When processing raw data
    # it's common to have to do some extra postprocessing
    df['streamflow'] = df['streamflow'].astype(np.float64)
    df.index = pd.DatetimeIndex(df.index)
    return df


# %%
site = '09506000'
begin_date = '2000-09-25'
end_date = '2022-09-25'

df = open_usgs_data(site, begin_date, end_date)
df['streamflow'].plot()
plt.semilogy()
plt.ylabel('Streamflow [cfs]')
plt.xlabel('')


#%%
# Hmm, 20 years of daily data starts to blend together.
# Just a quick aside on another nice feature of pandas, the resample
# Let's just resample the data down to monthly means like so:
df.resample('M').mean()['streamflow'].plot()
plt.semilogy()
plt.ylabel('Streamflow [cfs]')
plt.xlabel('')


# %%
# Now, let's look at some DayMet data. 
# Before that, let me explain...


# %%
# DayMet actually has a really nice interactive
# API explorer that you can use to prototype:
# - https://daymet.ornl.gov/single-pixel/api

url = "https://daymet.ornl.gov/single-pixel/api/data?lat=34.9455&lon=-113.2549"  \
       "&vars=prcp&start=1984-08-14&end=2014-10-18&format=json"

begin_date = '2000-09-20'
end_date = '2020-09-25'
args = {
    'lat':  34.4483605,
    'lon': -111.7898705,
    'start': begin_date,
    'end': end_date,
    'vars': ['prcp', 'Tmax', 'Tmin'],
    'format': 'csv'
}
query = urllib.parse.urlencode(args)
url = f"https://daymet.ornl.gov/single-pixel/api/data?{query}"
url

# %% 
# 
response = urllib.request.urlopen(url)
daymet_df = pd.read_csv(response, header=6)
daymet_df.head()


#%%
# Daymet is annoying in that it only reports the year
# and day of year, rather than real dates. Also it uses
# a no-leap calendar, meaning all years have 365 days.
# So now our goal is to convert the `year` and `yday`
# columns into proper date times. This one took me a 
# second to figure out, but some quick googling got 
# me there:
# https://stackoverflow.com/questions/34258892/converting-year-and-day-of-year-into-datetime-index-in-pandas
datestring = (daymet_df['year'].astype(str) 
              + daymet_df['yday'].astype(str))
datestring.head()


#%%
# And we can pass that directly into the `pd.to_datetime` 
# function, with a format of `%Y%j` which means YEAR followed
# by the Julian day (AKA day of year)
dates = pd.to_datetime(datestring, format='%Y%j')
daymet_df.index = pd.DatetimeIndex(dates)
daymet_df.head()


#%% 
# With the dates correct, we now can merge things together
# Just one last minor hickup, the lack of leap years in
# daymet means we have to reindex to the dates from the 
# USGS database. Finally, for shorthand I just rename the 
# whole thing `df`.
verde_df = open_usgs_data(site, begin_date, end_date)
daymet_df = daymet_df.reindex(verde_df.index)
daymet_df['streamflow'] = verde_df['streamflow']
df = daymet_df


# %%
# And now we can do some comparisons!
df_monthly = df.resample('M').mean()
df_monthly.plot.scatter(x='tmax (deg c)', y='streamflow')
plt.semilogy()


# %%
