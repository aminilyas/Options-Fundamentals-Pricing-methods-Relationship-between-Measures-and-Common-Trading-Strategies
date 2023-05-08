# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 09:50:49 2022

@EDITOR: Amin Ilyas
"""

#%%

######NASDAQ NDX########

# -*- coding: utf-8 -*-
"""
Codes generate lecture 4

@author: wenbin.cao

"""
# import and define functions
from datetime import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

# this one is for 3D plots
from mpl_toolkits.mplot3d import Axes3D
# add a color bar (optional)
from matplotlib import cm

# define a function to make the z variable for the 3-D plot of z on x and y
def makeZ(df, colName):
    '''
    Take one column of df, either call1 or put1, by colName
    Return a matrix, zM, with the same shape as mGc or tG
    mGc and expValues are defined later
    I loop over the values of expValues
    each row of zM corresponds to the values of df[colName] for each expValue
    '''
    zM = np.zeros(mGc.shape)
    for i in range(len(expValues)):        
        zM[i,:] = df[df['maturity']==expValues[i]][colName]
    return zM

#%%
# change to the path of your working directory
inputPath='C:/Users/amin/OneDrive/IEMBA MSC NEOMA BS/8 Financial Data Visualization/Final Project - Group 12/Story 4'
# inputPath = 'D:/OneDrive - NEOMA Business School/MSc_Financial_Markets_&_Technologies/Courses S1/Course Data Visulization/codes'
""
s0 = 11549.6855      # the level of the SP500 index at the time of downloading the data on Dec 6 2022

# read the first files
fileName = inputPath+'/ndx_202212.xlsx'
call = pd.read_excel(fileName, 'call')
put = pd.read_excel(fileName, 'put')
# loop to read other files and append to these two files
for i in range(1,6):
    fileName = inputPath+'/ndx_20230'+str(i)+'.xlsx'
    tempC = pd.read_excel(fileName, 'call')
    call = call.append(tempC, ignore_index=True)
    tempP = pd.read_excel(fileName, 'put')
    put = put.append(tempP, ignore_index=True)

# convert dates
call['Expiration Date'] = pd.to_datetime(call['Expiration Date'])
put['Expiration Date'] = pd.to_datetime(put['Expiration Date'])
# create a column for date
call['date'] = pd.to_datetime('20221206', format = '%Y%m%d', errors = 'ignore') #Amin change to day download and work on the data
put['date'] = pd.to_datetime('20221206', format = '%Y%m%d', errors = 'ignore') #Amin change to day download and work on the data
# create a colum for days till expiration
#Amin for comparison run this: call['maturity1'] = (call['Expiration Date']-call['date'])
call['maturity'] = (call['Expiration Date']-call['date']).apply(lambda x: x.days) #Amin remove pd.datetime delta object-->make only days
put['maturity'] = (put['Expiration Date']-put['date']).apply(lambda x: x.days)
# we want to identify the strike prices common to all expiration date values
# call 
expValues = call.maturity.unique()      # unique maturity values
kValues = call[call['maturity']==expValues[0]]['Strike']      # the strike for the first maturity
for i in range(1, len(expValues)):
    temp = call[call['maturity']==expValues[i]]['Strike']      # the strike for the i-th maturity
    kValues = np.intersect1d(kValues, temp)          # use set intersect function to identify common strikes and update the original one
# the subset that has common strikes for each maturity   
call1 = call[call['Strike'].isin(kValues)]
# put
expValues = put.maturity.unique()      # unique maturity values
kValues = put[put['maturity']==expValues[0]]['Strike']      # the strike for the first maturity
for i in range(1, len(expValues)):
    temp = put[put['maturity']==expValues[i]]['Strike']      # the strike for the i-th maturity
    kValues = np.intersect1d(kValues, temp)          # use set intersect function to identify common strikes and update the original one
# the subset that has common strikes for each maturity
put1 = put[put['Strike'].isin(kValues)]
# use centered moneyness instead of strike: K/S-1
call1['moneyness'] = call1['Strike']/s0
put1['moneyness'] = put1['Strike']/s0


print(call1[['Strike','moneyness']].describe())

#%%
'''
3-D plot based on moneyness and maturity
To make it general, we do calls and puts separately even though they have the same strikes
You need to run %matplotlib qt to stop inline plotting, such that you can twist your 3-D plots
'''
# %matplotlib qt
dpi = 150       # resolution of the graph
fts = 12

mVc = call1['moneyness'].unique()
# we need to create a meshgird for 3D plots
mGc, tG = np.meshgrid(mVc, expValues)    # create the x-y coordinates

'''
Implied volatility surface
i do not add title and colarbar to make the 3-D plot itself bigger
'''
# call
# we need to convert the variable to have the same shape as our x-y coordinates
zM = makeZ(call1, 'IV')

fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
surf = ax.plot_surface(tG, mGc, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts) #k = strike S=underlying level (indicator for moneyness) - Amin
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'IV', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)

# put
mVp = put1['moneyness'].unique()
# we need to create a meshgird for 3D plots
mGp, tG = np.meshgrid(mVp, expValues)    # create the x-y coordinates   
# we need to convert the variable to have the same shape as our x-y coordinates
zM = makeZ(put1, 'IV')

fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
surf = ax.plot_surface(tG, mGp, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'IV', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)

'''
Delta
'''
# call
zM = makeZ(call1, 'Delta')
fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
surf = ax.plot_surface(tG, mGc, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'Delta', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)
# put
zM = makeZ(put1, 'Delta')
fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
surf = ax.plot_surface(tG, mGp, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'Delta', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)

'''
Gamma
'''
# call
zM = makeZ(call1, 'Gamma')
fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
surf = ax.plot_surface(tG, mGc, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'Gamma', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)
# put
zM = makeZ(put1, 'Gamma')
fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
surf = ax.plot_surface(tG, mGp, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'Gamma', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)

'''
Volume
'''
# call
zM = makeZ(call1, 'Volume')
fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
# we use scatter than surface due to many zeros in volume
ax.scatter(tG, mGc, zM)
# surf = ax.plot_surface(tG, mGc, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'Volume', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)
# put
zM = makeZ(put1, 'Volume')
fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
# we use scatter than surface due to many zeros in volume
ax.scatter(tG, mGp, zM)
# surf = ax.plot_surface(tG, mGp, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'Volume', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)

'''
Open Interest
'''
# call
zM = makeZ(call1, 'Open Interest')
fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
# we use scatter than surface due to many zeros
ax.scatter(tG, mGc, zM)
# surf = ax.plot_surface(tG, mGc, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'Open Interest', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)
# put
zM = makeZ(put1, 'Open Interest')
fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
# we use scatter than surface due to many zeros 
ax.scatter(tG, mGp, zM)
# surf = ax.plot_surface(tG, mGp, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'Open Interest', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)

'''
bid-ask spread
'''
call1['ABAS'] = call1['Ask']-call1['Bid']
call1['RBAS'] = (call1['Ask']-call1['Bid'])/(call1['Ask']+call1['Bid'])
put1['ABAS'] = put1['Ask']-put1['Bid']
put1['RBAS'] = (put1['Ask']-put1['Bid'])/(put1['Ask']+put1['Bid'])

'''
ABAS
'''
# call
zM = makeZ(call1, 'ABAS')
fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
ax.scatter(tG, mGc, zM)
# surf = ax.plot_surface(tG, mGc, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'ABAS', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)
# put
zM = makeZ(put1, 'ABAS')
fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
ax.scatter(tG, mGc, zM)
# surf = ax.plot_surface(tG, mGp, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'ABAS', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)

'''
RBAS
'''
# call
zM = makeZ(call1, 'RBAS')
fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
ax.scatter(tG, mGc, zM)
# surf = ax.plot_surface(tG, mGc, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'RBAS', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)
# put
zM = makeZ(put1, 'RBAS')
fig = plt.figure(dpi=dpi)
ax = fig.gca(projection='3d')
ax.scatter(tG, mGc, zM)
# surf = ax.plot_surface(tG, mGp, zM, cmap=cm.coolwarm, linewidth=0, antialiased=False)    # x=tG, y = mG, z = implied volatility
# ax.set_title(r'Implied Volatility Surface', fontsize =fts)
ax.set_ylabel(r'$K/S$', fontsize =fts)
ax.set_xlabel(r'Maturity', fontsize =fts)
ax.set_zlabel(r'RBAS', fontsize =fts)
# fig.colorbar(surf, shrink=0.5, aspect=5)