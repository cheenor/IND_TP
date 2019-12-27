#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 09:59:18 2019

@author: chenjh
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
from pylab import *
import string
import numpy as np
import datetime
import scipy.stats as scista
from netCDF4 import Dataset
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['contour.negative_linestyle'] = 'dashed'
mpl.rcParams['ytick.labelsize'] = 18
mpl.rcParams['xtick.labelsize'] = 18
plt.rc('lines', linewidth=4)
def readAscii(fpath,iskp,*nl):
    #iskp  the total line skipped of the file
    # fpath   the full path of the file
    # usage: onedim=readAscii(fpaht,iskp)
    onedim=[]
    linesplit=[]
    f=open(fpath)
    if nl:
        nrl=nl[0]
        ff=f.readlines()[iskp:nrl]  ## first line in obs file is legend 
    else:
        ff=f.readlines()[iskp:]
    datestr=[]
    for line in ff:
        line=string.lstrip(line)
        linesplit.append(line[:-1].split(' '))
    for lnstrs in linesplit:
        for strs in lnstrs:
#            if strs!='':
#                onedim.append(string.atof(strs))
            try:
                aa=string.atof(strs)
                if aa==-99 or aa==-9:
                    aa=None
                onedim.append(aa)
            except:
                if strs!='':
                    datestr.append(strs)
#            else:
#                onedim.append(string.atof(strs))
    del linesplit,ff
    f.close()
    print len(onedim)
    return onedim
####################################
dirin='/Volumes/MacHD/Work/Papers/INDMosoon_TP/Data/'
dirout='/Volumes/MacHD/Work/Papers/INDMosoon_TP/Pics/'
yearstr=[]
monindx=[]
fpath=dirin+'ismidx-jja.txt'
onedim=readAscii(fpath,2)
nyy=len(onedim)/2
ny=0
for i in range(0,nyy):
    strs='%d'%onedim[i*2]
    iy=onedim[i*2]
    if iy>=1990 and iy<2010:
        ny=ny+1
        yearstr.append(strs)
        monindx.append(onedim[i*2+1])
#######################################
xdat=range(0,ny)
indm=np.zeros(shape=(ny),dtype=float)
for i in range(0,ny):
    indm[i]=monindx[i]
mm=np.zeros(shape=(ny),dtype=float)
std=np.zeros(shape=(ny),dtype=float)
for i in range(0,ny):
    mm[i]=indm.mean()
    std[i]=0.5*indm.std()    
clrs=[]
for i in range(0,ny):
    if monindx[i]<mm[0]-std[0]:
        clrs.append('red')
    elif monindx[i]>mm[0]+std[0]:
        clrs.append('green')
    else:
        clrs.append('gray')
fig, ax = plt.subplots(nrows=1,ncols= 1,figsize=(14,6))
ax.bar(xdat,monindx,0.9,color=clrs, hatch="///",alpha=0.2)
ax.set_xlim(0,ny-1)
ax.set_xticks(range(0,ny,1))  
xticklabels = [yearstr[nn] for nn in range(0,ny,1)] 
ax.set_xticklabels(xticklabels, size=16,rotation=45)
ax.plot(xdat,mm,c='gray',ls='-',lw=1.5)
ax.plot(xdat,mm-std,c='r',ls=":",lw=1.5,alpha=0.7)
ax.plot(xdat,mm+std,c='g',ls=':',lw=1.5,alpha=0.7)
ax.set_title('India Summer Monsoon Index',fontsize=18)
plt.savefig(dirout+'Index_IndMosoon_1990-2009.png',dpi=300)
plt.close()











