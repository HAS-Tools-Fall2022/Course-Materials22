# %%
# This script simply provides the implementation for 
# calculating the air pressure at a given elevation
# that we worked through in class.

import math

# %% 

def air_pressure_at_height(h):
    p0 = 101325      # reference pressure in pascals
    M = 0.02896968   # molar mass of air kg/mol
    g = 9.81         # gravity m/s2
    R0 = 8.314462618 # gas constant J/(mol·K) 
    T = 273          # temp in kelvin

    ratio = -(g * h * M) / (R0 * T)
    p_h = p0 * math.exp(ratio)
    return p_h
# %%

# List of elevations to run
h_list = range(0, 1000, 100)
p_list = []
for height in h_list:
    p_h = air_pressure_at_height(height)
    p_list.append(p_h)
# %%
