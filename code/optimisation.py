# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 12:19:13 2019

@author: Reinis
"""

import numpy as np
import scipy.stats as stat
from scipy.optimize import Bounds, LinearConstraint, NonlinearConstraint, BFGS, minimize
import matplotlib.pyplot as plt

# Notation:
# _n  - Subscript for normal tissue parameters.
# _t  - Subscript for tumour parameters.
# N   - Number of read.
# L   - Length of a read.
# G   - Length of relevant part of genome (incl. whole genome).
# rho - Sequencing redundancy, rho = N*L/G.
# phi - 
# h   -
# C   -
# f   -
# p   -
# k   -
# eta -


# Computes the expected coverage 
def f(rho, phi, h):
    return np.power(1-stat.poisson.cdf(phi, np.clip(rho,0.1, None)/h), h)

# On input input
#   v_rho_t - vector of tumour tissue sequencing redundancies
#   v_rho_n - vector of normal tissue sequencing redundancies
#   other parameters described in notation
# Outputs the false negative probability of the test when testing at
#  an alpha_0 level
def beta(v_rho_t, v_rho_n, 
         ni, G,
         mu_t, mu_n, mu_0, 
         phi_t = 14, phi_n = 8, h = 2,
         alpha_0 = 0.01):
    f_t = f(v_rho_t, phi_t, h)
    f_n = 1-f(v_rho_n, phi_n, h)
    f_n_t = (f_n*f_t).sum()
    f_n_sq = (f_n*f_n*f_t).sum()
    f_t_sq = (f_t*f_t).sum()
    f_t = f_t.sum()
    f_n = f_n.sum()
    return stat.norm.cdf(
            mu_0 - stat.norm.ppf(alpha_0)*np.sqrt(mu_0*(1-mu_0)/(f_t*G)),
            ((mu_t*ni+mu_0*(1-ni))*f_t + mu_n*f_n_t)/f_t,
            np.sqrt((ni*mu_t*(1-mu_t)+(1-ni)*mu_0*(1-mu_0))*G*f_t+
                    ni*(1-ni)*(mu_t-mu_0)*(mu_t-mu_0)*G*G*f_t_sq+
                    mu_n*(1-mu_n)*G*f_n_sq)/(G*f_t))

# Similar to my_beta, but outputs the power of the test instead
def power(v_rho_t, v_rho_n, 
         ni, G,
         mu_t, mu_n, mu_0, 
         phi_t = 14, phi_n = 8, h = 2,
         alpha_0 = 0.01):
    return 1-beta(v_rho_t, v_rho_n, 
                 ni, G,
                 mu_t, mu_n, mu_0, 
                 phi_t, phi_n, h,
                 alpha_0)
    
# Similar to my_beta, but outputs the type I error probability 
#  of the test instead
def alpha(v_rho_t, v_rho_n,
          ni, G,
          mu_0, mu_n, 
          phi_t = 14, phi_n = 8, h = 2,
          alpha_0 = 0.01):
    return power(v_rho_t, v_rho_n,
                ni, G,
                mu_0, mu_n, mu_0, 
                phi_t, phi_n, h,
                alpha_0)

# Initialize the parameters of the optimization
    
G = 30000

s = 100
ni = 0.5

mu_0 = 1e-6
mu_t = 15e-6
mu_n = 3e-6

phi_t = 14
phi_n = 8
h = 2

alpha_0 = 0.05

# We generate somewhat plausible parameters for tumour content and 
#  relative tumour genome size
p = stat.beta.rvs(60, 40, size = s)
k = 1+stat.expon.rvs(scale = 0.5, size = s)
eta = k+1/p-1
# Plot the resulting cost distribution
plt.hist(eta)
plt.show()

# Allocate sequencing budget
rho_t_T = s*50
rho_n_T = s*40

# Redefinition of the alpha and beta functions for the optimisation
def alpha_opt(x):
    v_rho_t = x[:s]
    v_rho_n = x[s:]
    return alpha(v_rho_t, v_rho_n, ni, G, mu_0, mu_n, phi_t, phi_n, h, alpha_0)

def beta_opt(x):
    v_rho_t = x[:s]
    v_rho_n = x[s:]
    return beta(v_rho_t, v_rho_n, ni, G, mu_t, mu_n, mu_0, phi_t, phi_n, h, alpha_0)

# Calculate the initial sequencing distribution
# In this case we use the base method of allocating to each sample the same
#  amount of sequencing relative to the total redundancy budget allocated
#  for that category.
v_rho_t = np.repeat(rho_t_T/s, s)/eta
v_rho_n = np.repeat(rho_n_T/s, s)
x0 = np.append(v_rho_t, v_rho_n)
# Results of the initial distribution
print(beta_opt(x0), alpha_opt(x0))

# Define the total cost constraint
linear_constraint = LinearConstraint(np.append(eta, np.repeat(1,s)), 
                                     0, rho_t_T+rho_n_T)
# Define the type I error constraint
nonlinear_constraint = NonlinearConstraint(alpha_opt, 0, 0.051, jac='2-point', hess=BFGS())
# Define bounds on the sequencing redundancy (i.e. make sure it is not negative)
bounds = Bounds(np.repeat(0, 2*s), np.repeat(np.inf, 2*s))

# This runs the optimization
res = minimize(beta_opt, x0, method='trust-constr', 
               jac='2-point', hess=BFGS(),
               constraints=[linear_constraint, 
                            nonlinear_constraint],
               options={'verbose': 2}, bounds=bounds)


# Optimisation restults
print(beta_opt(res.x), alpha_opt(res.x))

# Outputs the number of samples that were included in the sequencing experiment
# Defined to be samples sequenced to at least t coverage
t = 0.5
print(sum(f(res.x[:s], phi_t, h)>t))
