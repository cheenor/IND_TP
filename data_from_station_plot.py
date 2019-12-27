 #!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 08:12:36 2018

@author: jhchen
"""
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np  # 数组，数值计算
import matplotlib.pyplot as plt  # 画图 模块
import math  #数学公式模块
import string  #字符串处理
import os    # 系统模块，可以建立文件夹，删除文件，改文件名等等
import calendar
import datetime
from pylab import *
import locale
from locale import atof
import glob
#import Station_loop
mpl.rcParams['ytick.labelsize'] = 20
mpl.rcParams['xtick.labelsize'] = 20
mpl.rcParams['contour.negative_linestyle'] = 'dashed'
###############################################################
def isYear(year):  
    if (year%4 == 0) & (year%100 != 0):  
        print("%d年是闰年" %year)
        return 366  
    elif year%400 == 0:  
        print("'%d'年是闰年" %year) 
        return 366
    else:  
        print("'%d'不年是闰年" %year)
        return 365
def getFileName(path):
    f_list = os.listdir(path)
    # print f_list
    filename=[]
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.nc':
            #print i
            filename.append(i)
    return filename
def readAscii(fpath,iskp):
    #iskp  the total line skipped of the file
    # fpath   the full path of the file
    # usage: onedim=readAscii(fpaht,iskp)
    onedim=[]
    linesplit=[]
    f=open(fpath)
    ff=f.readlines()[iskp:]  ## first line in obs file is legend 
    for line0 in ff:
        #print 'line 1',line0
        line=line0.lstrip() ##string.lstrip(line0)
        #print 'line 2',string.lstrip(line0)
        linesplit.append(line[:-1].split(' '))
        #print linesplit
    for lnstrs in linesplit:
        #print 'A',lnstrs
        for strs in lnstrs:
            #print 'B',strs
            if strs!='':
                onedim.append(atof(strs))
    del linesplit
    f.close()
    return onedim
#########################################################
dirin='/Volumes/MacHD/Work/Papers/INDMosoon_TP/Data/'
dirpic='/Volumes/MacHD/Work/Papers/INDMosoon_TP/Pics/'
allvars=['PRE','RHU','SSD','TEM','WIN','PRS']
allcol_num=[13,11,9,13,17,13]
nv=len(allvars)
regions=[89.9,100,34.9,37.5]
ndays=[31,28,31,30,31,30,31,31,30,31,30,31]
nm=len(ndays)
monperiod=[4,5,6,7,8,9]
nmp=len(monperiod)
ndd=0
for i in range(0,nmp):
    k=monperiod[i]-1
    ndd=ndd+ndays[k]
nv=15
nyy=2010-1990
allmondat=np.zeros(shape=(nyy,12,nv),dtype=float)
alldaydat=np.zeros(shape=(nyy,ndd,nv),dtype=float)
allyearstr=[]
for iy in range(1990,2010):
    print iy
    iyy=iy-1990
    ndd=isYear(iy)
    ndays[1]=28
    if ndd==366:
        ndays[1]=29
    yearstr='%2.2d'%iy
    allyearstr.append(yearstr)
    fpath=dirin+yearstr+'_StationData_daily.txt'
    onedim=readAscii(fpath,1)
    nl=len(onedim)/nv
    rawdat=np.zeros(shape=(nl,nv),dtype=float)
    for i in range(0,nl):
        for iv in range(0,nv):
            k=i*nv+iv
            rawdat[i,iv]=onedim[k]
    ###########
    ikk=0
    idd=0
    for im in range(0,nm):
        nd=ndays[im]
        mscl=1.0/float(nd)
        for idd in range(0,nd):
            for iv in range(1,nv):
                allmondat[iyy,im,iv]=allmondat[iyy,im,iv]+rawdat[ikk,iv]*mscl                
                if im+1 in monperiod:
                    alldaydat[iyy,idd,iv]=rawdat[ikk,iv]
            if im+1 in monperiod:        
                idd=idd+1
            ikk=ikk+1
# precipitation  #3
yearmean=np.zeros(shape=(nyy),dtype=float)
moonmean=np.zeros(shape=(nyy),dtype=float)
moonmon=np.zeros(shape=(nyy,nmp),dtype=float)
for iy in range(0,nyy):
    tmp=allmondat[iy,:,3]
    yearmean[iy]=tmp.mean()
    a=0
    for im in range(0,nm):
        if im+1 in monperiod:
            a=a+tmp[im]/(nmp*1.0)
    moonmean[iy]=a
# plot yearly mean
a=yearmean.mean()
b=moonmean.mean()
xdat=range(0,nyy)
fig,ax=plt.subplots(nrows=2,ncols= 1,figsize=(14,10))
ax[0].bar(xdat,yearmean-a,0.9,color='r')
ax[0].set_xlim(0,nyy-1)
ax[0].set_xticks(range(0,nyy,1))  
xticklabels = [allyearstr[nn] for nn in range(0,nyy,1)]
ax[0].set_xticklabels(xticklabels, size=16,rotation=45)
ax[1].bar(xdat,moonmean-b,0.9,color='g')
ax[1].set_xlim(0,nyy-1)
ax[1].set_xticks(range(0,nyy,1))  
xticklabels = [allyearstr[nn] for nn in range(0,nyy,1)]
ax[1].set_xticklabels(xticklabels, size=16,rotation=45)
plt.savefig(dirpic+"station_yearly+moonperiod.png",dpi=300)          
#plt.show()
plt.close()
#####
mon12=np.zeros(shape=(12),dtype=float)
monwk=np.zeros(shape=(12),dtype=float)
monst=np.zeros(shape=(12),dtype=float)
aa=moonmean.mean()
###
allmondat_norm=np.zeros(shape=(nyy,nm),dtype=float)
for iy in range(0,nyy):
    tmp=allmondat[iy,:,3]
    a=tmp.min()
    b=tmp.max()
    for im in range(0,nm):
        allmondat_norm[iy,im]=(allmondat[iy,im,3]-a)/(b-a)
###
for im in range(0,nm):
    tmp=allmondat[:,im,3]
    mon12[im]=tmp.mean()-aa
    for iy in range(0,nyy):
        if iy+1990 in (1991,1992,1994,1996,2000,2001):
            monst[im]=monst[im]+(allmondat[iy,im,3]-moonmean[iy])/6.0
        if iy+1990 in (1995,1997,1999,2002,2008,2009):
            monwk[im]=monwk[im]+(allmondat[iy,im,3]-moonmean[iy])/6.0
# plot yearly mean
a=yearmean.mean()
b=moonmean.mean()
nx=12 #range(0,12)
xdat=range(0,nx)
fig,ax=plt.subplots(nrows=1,ncols= 1,figsize=(14,8))
ax.plot(xdat,mon12,color='b')
ax.plot(xdat,monst,color='g')
ax.plot(xdat,monwk,color='r')
ax.set_xlim(0,nx)
ax.set_xticks(range(0,nx,1))  
#xticklabels = [allyearstr[nn] for nn in range(0,nyy,1)]
plt.savefig(dirpic+"station_monthly.png",dpi=300)          
#plt.show()
plt.close()
####
mon12=np.zeros(shape=(12),dtype=float)
monwk=np.zeros(shape=(12),dtype=float)
monst=np.zeros(shape=(12),dtype=float)
aa=moonmean.mean()
for im in range(0,nm):
    tmp=allmondat[:,im,3]
    mon12[im]=tmp.mean()
    for iy in range(0,nyy):
        if iy+1990 in (1991,1992,1994,1996,2000,2001):
            monst[im]=monst[im]+allmondat[iy,im,3]/6.0
        if iy+1990 in (1995,1997,1999,2002,2008,2009):
            monwk[im]=monwk[im]+allmondat[iy,im,3]/6.0
# plot yearly mean
a=yearmean.mean()
b=moonmean.mean()
nx=12 #range(0,12)
xdat=range(0,nx)
fig,ax=plt.subplots(nrows=1,ncols= 1,figsize=(14,8))
ax.plot(xdat,mon12,color='b')
ax.plot(xdat,monst,color='g')
ax.plot(xdat,monwk,color='r')
ax.set_xlim(0,nx)
ax.set_xticks(range(0,nx,1))  
#xticklabels = [allyearstr[nn] for nn in range(0,nyy,1)]
plt.savefig(dirpic+"station_monthly-2.png",dpi=300)          
#plt.show()
plt.close()
######
mon12=np.zeros(shape=(12),dtype=float)
monwk=np.zeros(shape=(12),dtype=float)
monst=np.zeros(shape=(12),dtype=float)
aa=moonmean.mean()
for im in range(0,nm):
    tmp=allmondat_norm[:,im]
    mon12[im]=tmp.mean()
    for iy in range(0,nyy):
        if iy+1990 in (1991,1992,1994,1996,2000,2001):
            monst[im]=monst[im]+allmondat_norm[iy,im]/6.0
        if iy+1990 in (1995,1997,1999,2002,2008,2009):
            monwk[im]=monwk[im]+allmondat_norm[iy,im]/6.0
# plot yearly mean
a=yearmean.mean()
b=moonmean.mean()
nx=12 #range(0,12)
xdat=range(0,nx)
fig,ax=plt.subplots(nrows=1,ncols= 1,figsize=(14,8))
ax.plot(xdat,mon12,color='b')
ax.plot(xdat,monst,color='g')
ax.plot(xdat,monwk,color='r')
ax.set_xlim(0,nx)
ax.set_xticks(range(0,nx,1))  
#xticklabels = [allyearstr[nn] for nn in range(0,nyy,1)]
plt.savefig(dirpic+"station_monthly-3.png",dpi=300)          
#plt.show()
plt.close()
######
mon12=np.zeros(shape=(12),dtype=float)
monwk=np.zeros(shape=(12),dtype=float)
monst=np.zeros(shape=(12),dtype=float)
aa=moonmean.mean()
for im in range(0,nm):
    tmp=allmondat[:,im,6]
    mon12[im]=tmp.mean()
    for iy in range(0,nyy):
        if iy+1990 in (1991,1992,1994,1996,2000,2001):
            monst[im]=monst[im]+allmondat[iy,im,6]/6.0
        if iy+1990 in (1995,1997,1999,2002,2008,2009):
            monwk[im]=monwk[im]+allmondat[iy,im,6]/6.0
# plot yearly mean
a=yearmean.mean()
b=moonmean.mean()
nx=12 #range(0,12)
xdat=range(0,nx)
fig,ax=plt.subplots(nrows=1,ncols= 1,figsize=(14,8))
ax.plot(xdat,mon12*0.1,color='b')
ax.plot(xdat,monst*0.1,color='g')
ax.plot(xdat,monwk*0.1,color='r')
ax.set_xlim(0,nx)
ax.set_xticks(range(0,nx,1))  
#xticklabels = [allyearstr[nn] for nn in range(0,nyy,1)]
plt.savefig(dirpic+"station_temp_monthly.png",dpi=300)          
#plt.show()
plt.close()
######
mon12=np.zeros(shape=(12),dtype=float)
monwk=np.zeros(shape=(12),dtype=float)
monst=np.zeros(shape=(12),dtype=float)
aa=moonmean.mean()
for im in range(0,nm):
    tmp=allmondat[:,im,7]
    mon12[im]=tmp.mean()
    for iy in range(0,nyy):
        if iy+1990 in (1991,1992,1994,1996,2000,2001):
            monst[im]=monst[im]+allmondat[iy,im,7]/6.0
        if iy+1990 in (1995,1997,1999,2002,2008,2009):
            monwk[im]=monwk[im]+allmondat[iy,im,7]/6.0
# plot yearly mean
a=yearmean.mean()
b=moonmean.mean()
nx=12 #range(0,12)
xdat=range(0,nx)
fig,ax=plt.subplots(nrows=1,ncols= 1,figsize=(14,8))
ax.plot(xdat,mon12*0.1,color='b')
ax.plot(xdat,monst*0.1,color='g')
ax.plot(xdat,monwk*0.1,color='r')
ax.set_xlim(0,nx)
ax.set_xticks(range(0,nx,1))  
#xticklabels = [allyearstr[nn] for nn in range(0,nyy,1)]
plt.savefig(dirpic+"station_Maxtemp_monthly.png",dpi=300)          
#plt.show()
plt.close()








