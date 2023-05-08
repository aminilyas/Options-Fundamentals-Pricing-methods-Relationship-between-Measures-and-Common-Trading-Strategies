# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 08:10:26 2022

@author: amin
==============================================================================
#                      3.1 Options Valuation                                 #
#                      and Pricing   Models                                  #
==============================================================================
"""
import math
import numpy as np
import numpy.random as npr 
from pylab import plt, mpl
import scipy.stats as scs

#pip install bsm==0.3.0

##############################################################################
#   3.1.2. Part I Monte Carlo Simulation - European Options                  #
##############################################################################
''' Function to generate random numbers for simulation.
Parameters
==========
M: int
number of time intervals for discretization
I: int
number of paths to be simulated
anti_paths: boolean
use of antithetic variates
mo_math: boolean
use of moment matching
'''
def gen_sn(M, I, anti_paths=True, mo_match=True):
    if anti_paths is True:
        sn = npr.standard_normal((M + 1, int(I / 2)))
        sn = np.concatenate((sn, -sn), axis=1)
    else:
        sn = npr.standard_normal((M + 1, I))
    if mo_match is True:
        sn = (sn - sn.mean()) / sn.std()
    return sn

''' Valuation of European call option in Black-Scholes-Merton
by Monte Carlo simulation (of index level at maturity)
Parameters
==========
K: float
(positive) strike price of the option
Returns
=======
C0: float
estimated present value of European call option
'''
S0 = 100.
r = 0.05
sigma = 0.25
T = 1.0
I = 50000

def gbm_mcs_stat(K):
    sn = gen_sn(1, I)
    # simulate index level at maturity
    ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T
                     + sigma * math.sqrt(T) * sn[1])
    # calculate payoff at maturity
    hT = np.maximum(ST - K, 0)
    # calculate MCS estimator
    C0 = math.exp(-r * T) * np.mean(hT)
    return C0

M = 50
def gbm_mcs_dyna(K, option='call'):
    dt = T / M
    # simulation of index level paths
    S = np.zeros((M + 1, I))
    S[0] = S0
    sn = gen_sn(M, I)
    for t in range(1, M + 1):
        S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt
                                 + sigma * math.sqrt(dt) * sn[t])
    # case-based calculation of payoff
    if option == 'call':
        hT = np.maximum(S[-1] - K, 0)
    else:
        hT = np.maximum(K - S[-1], 0)
    # calculation of MCS estimator
    C0 = math.exp(-r * T) * np.mean(hT)
    return C0

gbm_mcs_dyna(K=110., option='call')
gbm_mcs_dyna(K=110., option='put')

from bsm_functions import bsm_call_value
stat_res = [] 
dyna_res = [] 
anal_res = [] 
k_list = np.arange(80., 120.1, 5.) 
np.random.seed(100)

for K in k_list:
    stat_res.append(gbm_mcs_stat(K)) 
    dyna_res.append(gbm_mcs_dyna(K)) 
    anal_res.append(bsm_call_value(S0, K, T, r, sigma))

stat_res = np.array(stat_res) 
dyna_res = np.array(dyna_res) 
anal_res = np.array(anal_res)

"""
Plot of static simulation:
Analytical option values vs. monte carlo
"""
plt.figure(figsize=(10, 6))
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
ax1.plot(k_list, anal_res, 'b', label='analytical')
ax1.plot(k_list, stat_res, 'ro', label='static')
ax1.set_ylabel('European call option value')
ax1.legend(loc=0)
ax1.set_ylim(bottom=0)
wi = 1.0
ax2.bar(k_list - wi / 2, (anal_res - stat_res) / anal_res * 100, wi)
ax2.set_xlabel('strike')
ax2.set_ylabel('difference in %')
ax2.set_xlim(left=75, right=125);

##############################################################################
#   3.1.2. Part II Monte Carlo Simulation - American Options                 #
##############################################################################

def gbm_mcs_amer(K, option='call'):
    ''' Valuation of American option in Black-Scholes-Merton
    by Monte Carlo simulation by LSM algorithm
    
    Parameters
    ==========
    K : float
        (positive) strike price of the option
    option : string
        type of the option to be valued ('call', 'put')
    
    Returns
    =======
    C0 : float
        estimated present value of European call option
    '''
    dt = T / M
    df = math.exp(-r * dt)
    # simulation of index levels
    S = np.zeros((M + 1, I))
    S[0] = S0
    sn = gen_sn(M, I)
    for t in range(1, M + 1):
        S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt 
                + sigma * math.sqrt(dt) * sn[t])
    # case based calculation of payoff
    if option == 'call':
        h = np.maximum(S - K, 0)
    else:
        h = np.maximum(K - S, 0)
    # LSM algorithm
    V = np.copy(h)
    for t in range(M - 1, 0, -1):
        reg = np.polyfit(S[t], V[t + 1] * df, 7)
        C = np.polyval(reg, S[t])
        V[t] = np.where(C > h[t], V[t + 1] * df, h[t])
    # MCS estimator
    C0 = df * np.mean(V[1])
    return C0

gbm_mcs_amer(110., option='call')

gbm_mcs_amer(110., option='put')

euro_res = []
amer_res = []

k_list = np.arange(80., 120.1, 5.)

for K in k_list:
    euro_res.append(gbm_mcs_dyna(K, 'put'))
    amer_res.append(gbm_mcs_amer(K, 'put'))

euro_res = np.array(euro_res)
amer_res = np.array(amer_res)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
ax1.plot(k_list, euro_res, 'b', label='European put')
ax1.plot(k_list, amer_res, 'ro', label='American put')
ax1.set_ylabel('call option value')
ax1.legend(loc=0)
wi = 1.0
ax2.bar(k_list - wi / 2, (amer_res - euro_res) / euro_res * 100, wi)
ax2.set_xlabel('strike')
ax2.set_ylabel('early exercise premium in %')
ax2.set_xlim(left=75, right=125);
# plt.savefig('../../images/ch12/stoch_17.png');