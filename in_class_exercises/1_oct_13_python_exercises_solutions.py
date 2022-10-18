# %%
# This set of exercises works through
# some basic python functionality
# I'll still be using some functions from 
# numpy but nothing you write should need it
# although you can use it if you'd like
import numpy as np

# %%  1.)
# Write code to translate a boolean value
# to a string. Specifically, if the `testval` 
# is `True` then print "Yes" and if it is
# `False` then print "No"
# What I want: 
#   True -> "yes"
#   False -> "no"
# Solution 1:
testval = bool(np.random.choice([0, 1]))
if testval is True:
    message = "Yes"
else:
    message = "No"
print(testval, message)

#%%
# Solution 2:
# Another approach with conditional
message = "No"
testval = bool(np.random.choice([0, 1]))

if testval is True:
   message = "Yes" 

print(testval, message)


#%%
# Solution 3:
# Another approach with dictionary
testval = bool(np.random.choice([0, 1]))
lookup = {
    # key: value,
    True: "Yes",
    False: "No"
}
print(testval, lookup[testval])


# %% 2.)
# You will be given a random integer, and 
# your goal is to return the same value, but
# as a negative number. Notice, the number you
# are given may already be negative
# Examples:
#  39 -> -39
#  -7 ->  -7
# Solution 1:
testval = np.random.randint(-100, 100)
if testval < 0:
    negval = testval
else:
    negval = -testval

print(testval, negval)

#%%
# Solution 2:
# Another solution using absolute values
testval = np.random.randint(-100, 100)
negval = -abs(testval)
print(testval, negval)

# %% 3.)
# Given a list of random integers, return them
# sorted from low to high. 
# NOTE: I do not want you to write your own
#       sorting algorithm, but want you to 
#       look up how to do this using the 
#       python standard library
# Solution:
random_vals = np.random.random_integers(-100, 100, 10)
sorted_vals = sorted(random_vals)
print(random_vals)
print(sorted_vals)

# %% 4.)
# Given a list of US locations with the format:
# "CityName, StateAbbrev" filter out any that
# are not in Arizona (AZ).
# Solution 1:
city_list = [
    "New York, NY",
    "Chattanooga, TN",
    "Hobart, MN",
    "Kingman, AZ",     # ...
    "Yachats, OR",     # <- no
    "Bisbee, AZ",      # <- yes
    "Muskogee, OK",     # <- no
    "Tucson, AZ",
]
#TODO: Your code here
az_list = []   # <-- add stuff in here
for city in city_list:  # by looking at these
    state = city[-2:]
    if state == 'AZ':
        # add city to az_list
        az_list.append(city)

print(az_list)


#%%
# Solution 2:
# An alternative solution
az_list = []   # <-- add stuff in here
for city in city_list:  # by looking at these
    if city.endswith("AZ"):
        # add city to az_list
        az_list.append(city)
print(az_list)

# %% 5.)
# This code doesn't work - can you fix it?
# Solution:
def multiply(a, b):
    return a * b

print("Line below this should be True:")
print(multiply(5, 10) == 50)

# %% 6.)
# Time for a coding interview classic, FizzBuzz
# The rulse of the game:
#  - print numbers from 1 to 100
#  - if the number is divisible by 3 print "Fizz"
#  - if the number is divisible by 5 print "Buzz"
#  - if the number is divisible by both 3 and 5 print "FizzBuzz"
#  - otherwise, print the number
# NOTE: % is the modulo operator (https://realpython.com/python-modulo-operator/)
# Solution:
testvals = np.arange(1, 101)
for v in testvals:
    if v % 3 == 0 and v % 5 == 0:
        print("v")
    elif v % 3 == 0:
        print("fizz")
    elif v % 5 == 0:
        print("buzz")
    else:
        print(v)

# %%
