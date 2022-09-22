#%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#%%
df = pd.read_csv(
    'https://raw.githubusercontent.com/arbennett/'
    'summa_snow_layering_analysis/master/obs_data/dana_obs.csv',
    index_col=0, skipinitialspace=True, parse_dates=True
)

# %%
df.head()


# %%
df['Tuolumne Meadows Pillow SWE [mm]'].plot()
df['Dana Meadows Pillow SWE [mm]'].plot()
plt.legend()


# %%
df.plot.scatter(
    x='Tuolumne Meadows Pillow SWE [mm]',
    y='Dana Meadows Pillow SWE [mm]'
)
# %%
