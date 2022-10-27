#%%
import numpy as np
import matplotlib.pyplot as plt

#%%
# Want points (x, y) where x in [-1, +1]
# and y in [-1, +1]
x = np.random.uniform(-1, 1)
y = np.random.uniform(-1, 1)

#%% 
# Want to know radius of a line from the
# origin (0,0) to the point (x,y)

xs = x ** 2
ys = y ** 2
r = np.sqrt(xs + ys)

print(x, y, r)

# %%
def random_point_and_radius():
    x = np.random.uniform(-1, 1)
    y = np.random.uniform(-1, 1)
    xs = x ** 2
    ys = y ** 2
    r = np.sqrt(xs + ys)
    return x, y, r


# %%
# Want to run this 1000 times
all_x = []
all_y = []
all_r = []
ntimes = 1000
for i in range(ntimes):
    # What you want to do many times
    # how do we assign values from this function
    x, y, r = random_point_and_radius()
    all_x.append(x)
    all_y.append(y)
    all_r.append(r)

all_x = np.array(all_x)
all_y = np.array(all_y)
all_r = np.array(all_r)


# %%
# boolean array all trues/falses
in_circle = all_r <= 1
out_circle = all_r > 1

#%%
plt.scatter(
    all_x[in_circle], all_y[in_circle]
)
plt.scatter(
    all_x[out_circle], all_y[out_circle]
)
# %%
