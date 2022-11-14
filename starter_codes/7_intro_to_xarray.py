#%%
# This overview will cover the basics of 
# the data structures, concepts, and capabilities 
# of xarray. Before getting started make sure you 
# install all of the necessary pieces with:
# 
# NOTE: Added "pooch" to installed packages"
# `conda install -c conda-forge xarray dask zarr fsspec aiohttp requests pooch`
#
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

#%%
# For this walkthrough we will just use one of the 
# included tutorial data. We will use the one simply
# named "air_temperature", but you can see a list
# of other available tutorial datasets here:
# https://docs.xarray.dev/en/stable/generated/xarray.tutorial.open_dataset.html
# 
# The first thing we will do is just output the result
# as `ds` so that we can see what it looks like.
# `xarray` gives a really nice overview representation
# when you do this in something like VSCode or Jupyter.
# It shows all of the dimensions, coordinates, variables,
# and attributes in the dataset in a way that makes it
# very easy to browse around. Try playing with the output
# a little bit to see what's in the data.
ds = xr.tutorial.open_dataset('air_temperature')
ds


#%%
# Okay, now let's dive in a bit further into the core data
# structures and how they're laid out. We'll tackle this in 
# the order they're presented in the output from the last
# code cell, starting with dimensions. A "dimension" in 
# xarray world is a label for the axis of an array. You
# can see we have 3 dimensions in the dataset, `lat`, `lon`,
# and `time`. These are displayed with the shape of the
# underlying array in the printout. You can also inspect
# them for a given dataset, `ds`, like so:
ds.dims

#%%
# Under the hood, the `ds.dims` object is just a dictionary
# that maps a name (with a string datatype) to a size (with
# an integer datatype). That is, it maps a string to an integer
# You can see this by pulling one of the dims out directly:
ds.dims['lat']

#%% 
# Similar to dimensions, in xarray the `coordinates` are
# some helper/extra data pieces which make operating on the
# main data more intuitive/simpler. If dimensions map between
# the axis of an array and it's "name", then coordinates map 
# between the index in the array to a real "place" in some
# space that is intuitive for humans to understand. 
# You can access them in a similar way to how the dimensions
# are accessed:
ds.coords

#%%
# If you want to look at an individual coordinate you can just
# access it like you would a column in a pandas dataframe:
ds['time']

#%%
# Similarly, you can be very specific and specify explicitly
# that what you want is a coordinate:
ds.coords['time']

#%%
# Next up is "data variables". These are specified with names
# just like the coordinates and dimensions. Note here you still
# see the dimensions and coordinates, and get a very similar 
# interface as we did when we showed the full `ds`. This is not
# an accident, and one of the major insights in the xarray data 
# model is data should almost awlays come with the attached metadata
# so that you can easily understand what you're looking at.
ds['air']

# %%
# Speaking of metadata, you can see the the `ds['air']` variable
# has some "Attributes" if you want you can just explore them via
# the widget from the previous cell. You can also see them directly
# in the code via:
ds['air'].attrs

# %%
# Dataset objects can contain multiple variables. The dataset
# from the tutorial here only has a single one, the air temperature
# but we can easily add a new variable, "pressure", using our
# trusty function from the beginning of the course:
def air_pressure_at_height_and_temp(h, T0):
    p0 = 101325      # reference pressure in pascals
    M = 0.02896968   # molar mass of air kg/mol
    g = 9.81         # gravity m/s^2
    R0 = 8.314462618 # gas constant J/(mol·K) 
    T = T0           # temp in kelvin

    ratio = -(g * h * M) / (R0 * T)
    p_h = p0 * np.exp(ratio)
    return p_h

ds['pressure'] = air_pressure_at_height_and_temp(2.0, ds['air'])

# Adding some metadata, this part is optional, but good practice!!
ds['pressure'].attrs['units'] = 'Pa'
ds['pressure'].attrs['long_name'] = 'Standard air pressure at 2m'
ds

# %%
# But what can we do with all of this? First, just to prove 
# something let's grab out the underlying data from the 'air'
# variable. This can be done with `ds['air].values` and will
# return the numpy array with all of the nice stuff stripped
# away. We'll look at the shape and see it's exactly what the
# dimensions said. 
# 
# NOTE: Generally you don't want to drop down into accessing
# the raw numpy array unless you *really* have to. I'm just
# showing you this to make it clear that the data really does
# exist!
print(type(ds['air'].values), ds['air'].values.shape)

# %%
# Okay, back to doing stuff with xarray. There are two 
# main ways to select data out of xarray objects,:
# - ds.isel: using indices to select data (like numpy)
# - ds.sel: using coordinates to select data
# Getting the first time:
first_time_isel = ds.isel(time=0)
first_time_isel

# %%
# Similarly we could to this
first_time_sel = ds.sel(time='2013-01-01 00:00')
print(first_time_sel == first_time_isel)

# %%
# We can also select out multiple coordinates
# at a time. Note here I'm using, `method='nearest'`
# so that we pull out the closest latitude and longitude
# to the points specified. Try running without that
# and see if you can figure out why the error occurs!
tucson_lat = 32.2540
tucson_lon = 110.9742

tucson_ds = ds.sel(
    lat=tucson_lat, 
    lon=tucson_lon, 
    method='nearest'
)
tucson_ds

# %%
# xarray has much more capabilities than just indexing 
# and adding labels to axes. It has a lot of capability
# around plotting. For instance we can just pull out
# the air temperature variable for the Tucson subset
# and call ".plot()" on it. xarray generally tries to
# make an intuitive type of plto for the dimensions that
# you give it to plot with, so here we get a timeseries.
tucson_ds['air'].plot()

# %%
# Similarly, we can plot the pressure that we calculated
# from the temperature. The plots look pretty much identical
# since they're derived from eachother. But note how we 
# get the axis labels including human readable timestamps,
# understandable names, and units all in the plot automatically!
tucson_ds['pressure'].plot()

# %%
# As mentioned, xarray will try to do the right thing when
# you call ".plot()" on something. For instance, if we select
# out a particular time and plot it we get a map:
ds['air'].isel(time=30).plot()

# %%
# Like pandas xarray has some really nice ways to aggregate
# and transform the data. For example, if we want to smooth
# out the temperature data for Tucson by taking the 30 day
# moving average we can do that with a "rolling" operation:
tucson_ds['air'].plot(label='Original')
tucson_ds['air'].rolling(time=30).mean().plot(label='Smoothed')
plt.legend()

# %%
# Similarly, we can do groupby's. Here we'll take the seasonal
# average across time, which creates a new dimension and coordinate
season = tucson_ds['time'].dt.season
seasonal_avg_airtemp = ds['air'].groupby(season).mean()
seasonal_avg_airtemp

#%%
# Further, xarray gives very convenient ways to quickly visualize
# data in common ways. For instance, if we want to see the maps
# of all four seasons from before we can just give the `plot`
# function the keyword `col`, which means plot a new column for
# each "instance" of that dimension. The `col_wrap` tells it to
# wrap to a new row after 2 columns. I'm also changing the colormap
# to make it easier to see the differences between seasons
seasonal_avg_airtemp.plot(col='season', col_wrap=2, cmap='turbo')

# %%
# Okay, that's it for this super fast overview!