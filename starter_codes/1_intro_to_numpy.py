# %%
# The numpy library is short for "numerical python"
# In this script I will motivate numpy as well
# as provide an introduction to it's functionality
# Numpy is a huge library with tons of capabilities
# so there will be a lot we don't cover.
# The numpy documentation is excellent though:
# https://numpy.org/doc/stable/
#
# There is also a really good quickstart guide
# that covers many of the things we will see here too:
# https://numpy.org/doc/stable/user/quickstart.html
#
# To start with numpy you can import it. The 
# line `import numpy as np` is the standard way
# to import it. This just renames `numpy` as `np`
# to save you time on typing
# I'm also importing math so that we can compare
# and finally the function from the previous script

import time
import math
import numpy as np

def air_pressure_at_height(h):
    p0 = 101325      # reference pressure in pascals
    M = 0.02896968   # molar mass of air kg/mol
    g = 9.81         # gravity m/s2
    R0 = 8.314462618 # gas constant J/(mol·K) 
    T = 273          # temp in kelvin

    ratio = -(g * h * M) / (R0 * T)
    # NOTE: here I changed math.exp -> np.exp, 
    #       you will see why in a minute
    p_h = p0 * np.exp(ratio)
    return p_h

start = 0
end = 20000
step = 1


# %%
t0 = time.time()
h_list = range(start, end, step)
p_list = []
for height in h_list:
    p_h = air_pressure_at_height(height)
    p_list.append(p_h)

t1 = time.time()
base_python_time = t1-t0
print("With plain python this took:", base_python_time, " seconds")


# %%
t0 = time.time()
h_array = np.arange(start, end, step)
p_array = air_pressure_at_height(h_array)

t1 = time.time()

numpy_time = t1-t0
print("With plain python this took:", numpy_time, " seconds")
print("Numpy version is ", base_python_time/numpy_time, " times faster")


# %%
# Okay, so how did that work?
# Numpy is an "array-based" library, meaning it defines the "array" type
# Here you can see we have `h_array` is an `ndarray`, which means 
# N-dimensional array. In our case N=1. We can also look at the shape
# NOTE: The length of the shape is always equal to the number of dimensions
print(type(h_array))
print(h_array.ndim)
print(h_array.shape)
print(len(h_array.shape) == h_array.ndim)


# %%
# What else can you do with numpy? Basically anything with numbers!
array_shape = (5, 5)

# Create an array of all ones with a specific shape
ones_matrix = np.ones(array_shape)
print(ones_matrix)
print(ones_matrix.shape)
print()
# Numpy also makes math easier to do, now you can just 
# multiply numbers and any ndarray object
print(0.1 * ones_matrix)
print()

# You can also operate on arrays with other numpy functions
print(np.sum(ones_matrix))
print(np.sum(ones_matrix, axis=0))

# %%
# Some really handy functions:

# Create an array from a list
sample_1d = np.array([0,1,2])
sample_2d = np.array(
    [[0,1,2],
     [3,4,5]]
)
print(sample_1d)
print()
print(sample_2d)
print()

# %%
# Create an array of all zeros
zeros = np.zeros(array_shape)
print(zeros)
print()

# %%
# Arange is just like the regular `range` function
# but produces an array rather than a `range` object
sequence_1 = np.arange(start, end, step)
print(sequence_1)
print()

# %%
# Linspace is the counterpart to `arange`. If you know
# how many numbers you need rather than the step size
# Here, 5 evenly spaced values form 0 to pi 
# NOTE: Linspace actually includes the end point
sequence_2 = np.linspace(0, np.pi, 5)
print(sequence_2)
print()

# %%
# You can create random numbers too
random_matrix = np.random.random(array_shape)
print(random_matrix)

# %%
# Numpy is really good for linear algebra
vector_shape = array_shape[0]
random_vector = np.random.random(vector_shape)
random_matrix_2 = np.random.random(array_shape)

# For example the dot product
random_dot = np.dot(random_vector, random_matrix_2)

# Or matrix multiplication
random_matmul = np.matmul(random_matrix, random_matrix_2)


# %%
# And there are a ton of operations, you can usually
# find what you need by searching online for 
# "numpy (whatever function you want)"
np.exp(random_matrix)
np.sin(random_matrix)
np.log(random_vector)
np.max(random_matmul)

# %%
# Finally, let's talk about slicing and indexing
# Like lists you can index arrays directly
sequence_1[0]
sequence_1[-1]

# %%
# You can also "slice" which is basically indexing
# multiple values. The syntax for slicing is like so
start = 0
stop = 5
step = 2
print(sequence_1[start:stop:step])

# Additionally you can create a `slice` object which
# can be convenient because you can use it multiple times
my_slice = slice(start, stop, step)
print(sequence_1[my_slice])
print(sequence_2[my_slice])


# %%
# For multidimensional arrays indexing works a 
# bit differently
increasing_matrix = np.arange(0, 9).reshape((3,3))
print(increasing_matrix)
print()
# Get the first row
print(increasing_matrix[0])
print()
# Get the middle value
print(increasing_matrix[1,2])
print()
# Get the first column, the `:` means "everything"
# It is equivalent to `slice(None, None, None)`
print(increasing_matrix[:, 0])

# %%
# Arrays can be of large dimension 
# (up to, I think, 64)
array_5d = np.arange(0, 3**5).reshape((3,3,3,3,3))
print(array_5d.shape, array_5d.ndim)


# %%
# Numpy also features some rudimentary ways of 
# reading data from files. This is how you'll complete
# your forecasting assignment. I've downloaded the daily
# streamflow in cubic feet per second for the last thirty 
# days (ending Sept 10) and placed it in the `data` directory
# 
filename ='../data/verde_river_daily_flow_cfs.csv'
np.loadtxt(filename, delimiter=',', usecols=[1])
# %%
