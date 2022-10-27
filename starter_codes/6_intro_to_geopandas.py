#%% 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import geopandas as gpd

#%%
# This contains the geometric data for the state of Arizona
# The format is an ESRI shapefile, but there are other ways
# to define geospatial data, with the most popular alternative
# probably being a "geojson" file. Anyways, we can just open
# this up with the `gpd.read_file` method, and it will automatically
# figure out that it's a shapefile.
az = gpd.read_file(
    '../data/arizona_shapefile/tl_2016_04_cousub.shp'
)
print(type(az))

# %%
# Just like a regular pandas dataframe the geodataframe
# has a bunch of helper methods for you to be able to 
# see what's in the data. As usual, doing `df.head()`
# will give a quick preview of what's inside it.
#
# NOTE: One important thing, if you scroll over the the
#       far right column in the printout you'll see that 
#       there is a column for the geometry, which defines
#       the shapes of the vector data.
az.head()


#%%
# You can even see the individual polygons in this case by 
# indexing the geometry directly.
az['geometry'].iloc[0]

# %%
# But, more importantly, it's easy to plot things! See
# here we can just call the `.plot()` function and that
# will automatically show you all of the geometries.
az.plot()

#%%
# Further, you can plot the data in the columns
# in an easy way by adding `column='COLUMN_NAME'`
# to the plot call. Also, adding `legend=True`
# will get you a colorbar. Here I'm just plotting
# the area of the land in each of the polygons.
az.plot(column='ALAND', legend=True)

# %%
# A minor aside, but you could also get this
# information from the geometry directly - see here.
# I'll also change the colormap with `cmap='turbo'`
# just to spice things up.
az['area'] = az.geometry.area
az.plot(column='area', legend=True, cmap='turbo')

#%%
# Next up, we can also pull in the GAGES-II dataset,
# which is a USGS product with the acronym "Geospatial 
# Attributes of Gages for Evaluating Streamflow" and 
# contains data from over 9000 located across the US.
# This shapefile only contains some of the attributes,
# but does not actually contain the streamflow timeseries.
# We'll get to that in your homework.
gages = gpd.read_file(
    '../data/gagesii_shapefile/gagesII_9322_sept30_2011.shp'
)
gages.head()

# %%
# As before, we can plot this right up. Now here note that
# we have points rather than polygons, so a different kind
# of vector data. I modified some of the plot attributes
# just to make things prettier. Here you can see the full 
# US, including Alaska, Hawaii, and Puerto Rico.
gages.plot(markersize=1, color='goldenrod')

# %%
# Let's see if we can plot the GAGES data along with the
# Arizona shapefile. Just to start off here, it might be
# worth looking at the axis labels on the previous plots.
# This is where the CRS stuff comes into play. 
# Now, when you run this, you might ask: where's Arizona?
# Great question - but let's jump down to the next cell to
# figure out what happened.
ax = gages.plot(markersize=1, color='goldenrod')
az.plot(ax=ax, color='crimson')

#%%
# Here I've added some bells and whistles to debug the
# behavior from above. Basically I added an `edgecolor`
# and increased the `linewidth` so we can see where
# the Arizona shapefile pops up - and it's somewhere
# south of Texas... clearly wrong. So what's up?
# It's the CRS. The Arizona shapefile has a lat/lon
# projection, and the GAGES shapefile is based on 
# meters, so they don't line up right. How do we fix this?
# See the answer below!
ax = gages.plot(markersize=1, color='goldenrod')
az.plot(
    ax=ax, 
    color='crimson', 
    edgecolor='crimson', 
    linewidth=10
)


# %%
# To get things lined up we can simply do a coordinate
# transformation. This is where geopandas comes in and
# helps out a lot. We can simply take the CRS of one of 
# the shapefiles and project the other one to the same 
# CRS. I'm putting the GAGES data onto the AZ CRS here
# just because I find lat/lon to be more intuitive. 
# Then, it's easy enough to just plot it all together!
gages = gages.to_crs(az.crs)
ax = az.plot(color='crimson')
gages.plot(markersize=1, color='goldenrod', ax=ax, alpha=0.2)

# %%
# Okay, next step you might want to do is just pull out
# the GAGES data that is inside of Arizona. This is really
# easy again thanks to geopandas with the `clip` function.
# Then, we'll just plot the thing up!
az_gages = gages.clip(az)
ax = az.plot(color='lightgrey', edgecolor='white')
az_gages.plot(ax=ax, color='crimson', markersize=5)
plt.title('Gages II data in Arizona')

# %%
# Great, that's all I have for you here! There will be
# more exercises combining this with stuff that you've
# seen for pulling in the streamflow data from USGS.