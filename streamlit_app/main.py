import numpy as np
import streamlit as st
import scipy.stats as stat
import matplotlib.pyplot as plt

"""
# L90 - Lab 1

## 1. Bernoulli Trial

### Setup

"""

bias = st.number_input("Specify the true bias", min_value=0.0, max_value=1.0, value=0.3)

size = int(st.number_input("Number of points to draw from each distribution", min_value=0, value=10, step=1))

true_dist = stat.bernoulli(bias)
x = true_dist.rvs(size=size)

fig, ax = plt.subplots()
ax.hist(x)
st.pyplot(fig)

"""
### Prior Specification

We'll be using a beta prior - specify parameters alpha and beta.
"""
a = st.number_input("Alpha", min_value=0, value=30, step=1)
b = st.number_input("Beta", min_value=0, value=30, step=1)

prior_dist = stat.beta(a, b)
prior = prior_dist.rvs(size=size)

fig, ax = plt.subplots()
ax.hist(prior)
st.pyplot(fig)

"""
### Posterior Distribution

"""

param_range = np.linspace(0,1,100)
index = np.arange(0,size,100)
fig, ax = plt.subplots()

error = []
for i in index:
    post_dist = stat.beta(np.sum(x[:i])+a,i-np.sum(x[:i])+b)
    post_pdf = post_dist.pdf(param_range)
    ax.plot(param_range, post_pdf)
    error.append((i,np.abs(post_dist.mean()-bias)))
    
post_dist = stat.beta(np.sum(x)+a,size-np.sum(x)+b)
post_pdf = post_dist.pdf(param_range)


ax.plot(param_range, post_pdf)
st.pyplot(fig)

post_dist.mean()


"""
Impact of iterations
"""

iterations = int(st.number_input("Number of iterations to perform", min_value=100, max_value=10000, value=100, step=100))
map_preds = []

for i in np.arange(iterations):
    x = true_dist.rvs(size=size)
    map_preds.append((stat.beta(np.sum(x)+a,size-np.sum(x)+b).mean()))

fig, ax = plt.subplots()
ax.plot(map_preds)
ax.set_ylim(0,1)

st.pyplot(fig)
