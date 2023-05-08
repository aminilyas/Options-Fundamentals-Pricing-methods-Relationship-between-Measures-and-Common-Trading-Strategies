# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 13:19:13 2022

@author: amin
==============================================================================
#                             3.3 Trading Options                            #
#                                Strategy                                    #
==============================================================================
"""
##############################################################################
#   3.3.1. Covered callable                                                  #
##############################################################################
import numpy as np
import matplotlib.pyplot as plt
#%pylab inline
price = np.arange(110,230,1) # the stock price at expiration date
strike = 160 # the strike price
premium = 7.5 # the option premium
# the payoff of short call position
payoff_short_call = [min(premium, -(i - strike-premium)) for i in price]
# the payoff of long stock postion
payoff_long_stock = [i-strike for i in price]
# the payoff of covered call
payoff_covered_call = np.sum([payoff_short_call, payoff_long_stock], axis=0)
plt.figure(figsize=(20,11))
plt.plot(price, payoff_short_call, label = 'short call')
plt.plot(price, payoff_long_stock, label = 'underlying stock')
plt.plot(price, payoff_covered_call, label = 'covered call')
plt.legend(fontsize = 20)
plt.xlabel('Stock Price at Expiry',fontsize = 15)
plt.ylabel('payoff',fontsize = 15)
plt.title('Covered Call Strategy Payoff at Expiration',fontsize = 20)
plt.grid(True)

##############################################################################
#   3.3.2. Bull call spread                                                  #
##############################################################################
price = np.arange(800,1100,1)
k_low = 900 # lower strike price for call
k_high = 1000 # higher strike price for call
premium_low = 20 # premium of call option with lower strike
premium_high = 2 # premium of call option with higher strike
# long call with lower strike
payoff_long_call = [max(-premium, i-k_low-premium_low ) for i in price]
# short call with higher strike
payoff_short_call = [min(premium, -(i-k_high-premium_high)) for i in price]
payoff = np.sum([payoff_long_call, payoff_short_call], axis=0)
plt.figure(figsize=(20,11))
plt.plot(price, payoff_long_call, label = 'long call')
plt.plot(price, payoff_short_call, label = 'short call')
plt.plot(price, payoff, label = 'Bull Call Spread')
plt.legend(fontsize = 20)
plt.xlabel('Stock Price at Expiry',fontsize = 15)
plt.ylabel('payoff',fontsize = 15)
plt.title('Bull Call Spread Payoff at Expiration',fontsize = 20)
plt.grid(True)

##############################################################################
#   3.3.3. Long straddle                                                     #
##############################################################################
price = np.arange(750,1000,1)
strike = 900 # strike price for both call and put
premium_call = 20 # premium of call option
premium_put = 10 # premium of put option
# payoff for the long call
payoff_long_call = [max(-premium_call, i-strike-premium_call) for i in price]
# payoff for the long put
payoff_long_put = [max(-premium_put, strike-i-premium_put) for i in price]
payoff = np.sum([payoff_long_call, payoff_long_put], axis=0)
plt.figure(figsize=(20,15))
plt.plot(price, payoff_long_call, label = 'Long Call')
plt.plot(price, payoff_long_put, label = 'long put')
plt.plot(price, payoff, label = 'Long Straddle')
plt.legend(fontsize = 20)
plt.xlabel('Stock Price at Expiry',fontsize = 15)
plt.ylabel('payoff',fontsize = 15)
plt.title('Long Straddle Payoff',fontsize = 20)
plt.grid(True)

##############################################################################
#   3.3.4. Long strangle                                                     #
##############################################################################
price = np.arange(700,1000,1)
# Suppose the undelying price at time 0 is 830
k_call = 870 # The strike price of OTM call
k_put = 795 # The strike price of OTM put
premium_call = 8 # premium of call option
premium_put = 10 # premium of put option
# payoff for the long call
payoff_long_call = [max(-premium_call, i-k_call-premium_call) for i in price]
# payoff for the long put
payoff_long_put = [max(-premium_put, k_put-i-premium_put) for i in price]
payoff = np.sum([payoff_long_call, payoff_long_put], axis=0)
plt.figure(figsize=(20,15))
plt.plot(price, payoff_long_call, label = 'Long Call')
plt.plot(price, payoff_long_put, label = 'long put')
plt.plot(price, payoff, label = 'Long Strangle')
plt.legend(fontsize = 20)
plt.xlabel('Stock Price at Expiry',fontsize = 15)
plt.ylabel('payoff',fontsize = 15)
plt.title('Long Strangle Payoff',fontsize = 20)
plt.grid(True)

##############################################################################
#   3.3.5. Butterfly Spread                                                  #
##############################################################################
price = np.arange(800,1100,1)
# Suppose the undelying price at time 0 is 935
k_itm = 915 # the strike price of ITM call
k_otm = 955 # the strike price of OTM call
k_atm = 935 # the strike price of ATM call
premium_itm = 45 # the premium of ITM call
premium_otm = 15 # the premium of OTM call
premium_atm = 25 # the premium of ATM call
# payoff for the long ITM call position
payoff_itm_long = [max(-premium_itm, i-k_itm-premium_itm) for i in price]
# payoff for the long OTM call position
payoff_otm_long = [max(-premium_otm, i-k_otm-premium_otm) for i in price]
# payoff for the 2 short ATM call position
payoff_atm_short = [min(2*premium_atm, -2*(i-k_atm-premium_atm)) for i in price]
# payoff for Butterfly Spread Strategy
payoff = np.sum([payoff_itm_long,payoff_otm_long,payoff_atm_short], axis=0)
plt.figure(figsize=(20,15))
plt.plot(price, payoff_itm_long, label = 'Long ITM Call')
plt.plot(price, payoff_otm_long, label = 'Long OTM Call')
plt.plot(price, payoff_atm_short, label = 'Short 2 ATM Call')
plt.plot(price, payoff, label = 'Long Call Butterfly Spread')
plt.legend(fontsize = 20)
plt.xlabel('Stock Price at Expiry',fontsize = 15)
plt.ylabel('payoff',fontsize = 15)
plt.title('Long Call Butterfly Spread Payoff',fontsize = 20)
plt.grid(True)

##############################################################################
#   3.3.6. Iron condor                                                       #
##############################################################################
price = np.arange(700,920,1)
k_call_higher = 850 # the strike price of OTM call(Higher k)
k_call_lower = 820 # the strike price of OTM call(Lower k)
k_put_higher = 780 # the strike price of OTM put(Higher k)
k_put_lower = 750 # the strike price of OTM put(Lower k)
premium_call_higher = 2 # the premium of OTM call(Higher k)
premium_call_lower = 10 # the premium of OTM call(Lower k)
premium_put_higher = 10 # the premium of oTM put(Higher k)
premium_put_lower = 2   # the premium of OTM put(Lower k)
# payoff for the long put position
payoff_long_put = [max(-premium_put_lower, k_put_lower-i-premium_put_lower) for i in price]
# payoff for the short put position
payoff_short_put = [min(premium_put_higher, -(k_put_higher-i-premium_put_higher)) for i in price]
# payoff for the short call position
payoff_short_call = [min(premium_call_lower, -(i-k_call_lower-premium_call_lower)) for i in price]
# payoff for the long call position
payoff_long_call = [max(-premium_call_higher, i-k_call_higher-premium_call_higher) for i in price]
# payoff for Long Iron Condor Strategy
payoff = np.sum([payoff_long_put,payoff_short_put,payoff_short_call,payoff_long_call], axis=0)
plt.figure(figsize=(20,15))
plt.plot(price, payoff_long_put, label = 'Long Put',linestyle='--')
plt.plot(price, payoff_short_put, label = 'Short Put',linestyle='--')
plt.plot(price, payoff_short_call, label = 'Short Call',linestyle='--')
plt.plot(price, payoff_long_call, label = 'Long Call',linestyle='--')
plt.plot(price, payoff, label = 'Long Iron Condor',c='black')
plt.legend(fontsize = 20)
plt.xlabel('Stock Price at Expiry',fontsize = 15)
plt.ylabel('payoff',fontsize = 15)
plt.title('Long Iron Condor Strategy Payoff',fontsize = 20)
plt.grid(True)

##############################################################################
#   3.3.7. Iron butterfly                                                    #
##############################################################################
price = np.arange(700,950,1)
k_atm = 830 # the strike price of ATM call & put
k_otm_put = 800 # the strike price of OTM put
k_otm_call = 860 # the strike price of OTM call
premium_otm_put = 2 # the premium of OTM put
premium_atm_put = 7 # the premium of ATM put
premium_atm_call = 8 # the premium of ATM call
premium_otm_call = 1 # the premium of OTM call
# payoff for the long put position
payoff_long_put = [max(-premium_otm_put, k_otm_put-i-premium_otm_put) for i in price]
# payoff for the short put position
payoff_short_put = [min(premium_atm_put, -(k_atm-i-premium_atm_put)) for i in price]
# payoff for the short call position
payoff_short_call = [min(premium_atm_call, -(i-k_atm-premium_atm_call)) for i in price]
# payoff for the long call position
payoff_long_call = [max(-premium_otm_call, i-k_otm_call-premium_otm_call) for i in price]
# payoff for Iron Butterfly Strategy
payoff = np.sum([payoff_long_put,payoff_short_put,payoff_short_call,payoff_long_call], axis=0)
plt.figure(figsize=(20,15))
plt.plot(price, payoff_long_put, label = 'Long Put',linestyle='--')
plt.plot(price, payoff_short_put, label = 'Short Put',linestyle='--')
plt.plot(price, payoff_short_call, label = 'Short Call',linestyle='--')
plt.plot(price, payoff_long_call, label = 'Long Call',linestyle='--')
plt.plot(price, payoff, label = 'Iron Butterfly',c='black')
plt.legend(fontsize = 20)
plt.xlabel('Stock Price at Expiry',fontsize = 15)
plt.ylabel('payoff',fontsize = 15)
plt.title('Iron Butterfly Strategy Payoff',fontsize = 20)
plt.grid(True)

##############################################################################
#   3.3.8. Protective Collar                                                 #
##############################################################################
price = np.arange(700,950,1)
# assume at time 0, the price of the undelying stock is 830
k_otm_put = 800 # the strike price of OTM put
k_otm_call = 860 # the strike price of OTM call
premium_otm_put = 6 # the premium of OTM put
premium_otm_call = 2 # the premium of OTM call
# payoff for the long put position
payoff_long_put = [max(-premium_otm_put, k_otm_put-i-premium_otm_put) for i in price]
# payoff for the short call position
payoff_short_call = [min(premium_otm_call, -(i-k_otm_call-premium_otm_call)) for i in price]
# payoff for the underlying stock
payoff_stock = price - 830
# payoff for the Protective Collar Strategy
payoff = np.sum([payoff_long_put,payoff_short_call,payoff_stock], axis=0)
plt.figure(figsize=(20,15))
plt.plot(price, payoff_long_put, label = 'Long Put',linestyle='--')
plt.plot(price, payoff_short_call, label = 'Short Call',linestyle='--')
plt.plot(price, payoff_stock, label = 'Underlying Stock',linestyle='--')
plt.plot(price, payoff, label = 'Protective Collar',c='black')
plt.legend(fontsize = 20)
plt.xlabel('Stock Price at Expiry',fontsize = 15)
plt.ylabel('payoff',fontsize = 15)
plt.title('Protective Collar Strategy - Payoff',fontsize = 20)
plt.grid(True)