# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 09:21:06 2022

@author: amin
==============================================================================
#                      3.1 Options Valuation                                 #
#                      and Pricing   Models                                  #
==============================================================================
"""
##############################################################################
#   3.1.3. Black-Scholes-Merton                                              #
##############################################################################

from math import log, sqrt, exp
from scipy import stats


class bsm_call_option(object):
    ''' Class for European call options in BSM model.

    Attributes
    ==========
    S0: float
        initial stock/index level
    K: float
        strike price
    T: float
        maturity (in year fractions)
    r: float
        constant risk-free short rate
    sigma: float
        volatility factor in diffusion term

    Methods
    =======
    value: float
        returns the present value of call option
    vega: float
        returns the Vega of call option
    imp_vol: float
        returns the implied volatility given option quote
    '''

    def __init__(self, S0, K, T, r, sigma):
        self.S0 = float(S0)
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def value(self):
        ''' Returns option value.
        '''
        d1 = ((log(self.S0 / self.K) +
               (self.r + 0.5 * self.sigma ** 2) * self.T) /
              (self.sigma * sqrt(self.T)))
        d2 = ((log(self.S0 / self.K) +
               (self.r - 0.5 * self.sigma ** 2) * self.T) /
              (self.sigma * sqrt(self.T)))
        value = (self.S0 * stats.norm.cdf(d1, 0.0, 1.0) -
                 self.K * exp(-self.r * self.T) * stats.norm.cdf(d2, 0.0, 1.0))
        return value

    def vega(self):
        ''' Returns Vega of option.
        '''
        d1 = ((log(self.S0 / self.K) +
               (self.r + 0.5 * self.sigma ** 2) * self.T) /
              (self.sigma * sqrt(self.T)))
        vega = self.S0 * stats.norm.pdf(d1, 0.0, 1.0) * sqrt(self.T)
        return vega

    def imp_vol(self, C0, sigma_est=0.2, it=100):
        ''' Returns implied volatility given option price.
        '''
        option = bsm_call_option(self.S0, self.K, self.T, self.r, sigma_est)
        for i in range(it):
            option.sigma -= (option.value() - C0) / option.vega()
        return option.sigma

from bsm_option_class import *
o = bsm_call_option(100., 105., 1.0, 0.05, 0.2)
type(o)
value = o.value()
value
o.vega()
o.imp_vol(C0=value)

import numpy as np
maturities = np.linspace(0.05, 2.0, 20)
strikes = np.linspace(80, 120, 20)
T, K = np.meshgrid(strikes, maturities)
C = np.zeros_like(K)
V = np.zeros_like(C)
for t in enumerate(maturities):
    for k in enumerate(strikes):
        o.T = t[1]
        o.K = k[1]
        C[t[0], k[0]] = o.value()
        V[t[0], k[0]] = o.vega()

from pylab import cm, mpl, plt
from mpl_toolkits.mplot3d import Axes3D
mpl.rcParams['font.family'] = 'serif'
#%config InlineBackend.figure_format = 'svg'

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(12, 7))
surf = ax.plot_surface(T, K, C, rstride=1, cstride=1,
            cmap=cm.coolwarm, linewidth=0.5, antialiased=True)
ax.set_xlabel('strike')
ax.set_ylabel('maturity')
ax.set_zlabel('European call option value')
fig.colorbar(surf, shrink=0.5, aspect=5);

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(12, 7))
surf = ax.plot_surface(T, K, V, rstride=1, cstride=1,
            cmap=cm.coolwarm, linewidth=0.5, antialiased=True)
ax.set_xlabel('strike')
ax.set_ylabel('maturity')
ax.set_zlabel('Vega of European call option')
fig.colorbar(surf, shrink=0.5, aspect=5);
