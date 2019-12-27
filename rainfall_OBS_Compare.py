#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 08:12:36 2018

@author: jhchen
"""
from netCDF4 import Dataset #用于读取netcdf文件
from mpl_toolkits.basemap import Basemap# 地图
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
import struct
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
def readAscii(fpath,iskp):
    #iskp  the total line skipped of the file
    # fpath   the full path of the file
    # usage: onedim=readAscii(fpaht,iskp)
    onedim=[]
    linesplit=[]
    f=open(fpath)
    ff=f.readlines()[iskp:]  ## first line in obs file is legend 
    for line in ff:
        line=string.lstrip(line)
        linesplit.append(line[:-1].split(' '))
    for lnstrs in linesplit:
        for strs in lnstrs:
            if strs!='':
                onedim.append(string.atof(strs))
    del linesplit
    f.close()
    return onedim
def readAscii2(fpath,iskp):
    #iskp  the total line skipped of the file
    # fpath   the full path of the file
    # usage: onedim=readAscii(fpaht,iskp)
    onedim=[]
    linesplit=[]
    f=open(fpath)
    ff=f.readlines()[iskp:]  ## first line in obs file is legend 
    for line in ff:
        line=string.lstrip(line)
        linesplit.append(line[:-1].split(' '))
    for lnstrs in linesplit:
        for strs in lnstrs:
            if strs!='':
                onedim.append(string.atof(strs))
    del linesplit
    f.close()
    return onedim
def readBin(fpath):
    # fpath   the full path of the file
    # usage: onedim=readAscii(fpath)
    nxc=283
    nyc=163
    nxy=nxc*nyc
    iskp=0
    for iy in range(1961,2010):
        ndays=isYear(iy)
        iskp=iskp+ndays*nxy
    onedim=[]
    binfile=open(fpath,'rb')
    bins=binfile.read()
    nn= len(bins)/4
    n1=iskp
    ndays=isYear(2010)
    n2=iskp+ndays*nxy
    for n in range(n1,n2):
        k1=n*4
        k2=k1+4
        aa,=struct.unpack('f',bins[k1:k2])
        onedim.append(aa)        
    return onedim
def getjuday(y,m,d):
    nd=0
    for im in range(1,m):
        wk,days=calendar.monthrange(y,im)
        nd=nd+days
    nd=nd+d
    return nd
def getTPrain(y,m,d,ndd):
    dirTP='D:/Work/MyPaper/PhD05/Archive/2010.6-8/'
    lon=[]
    for ix in range(0,160):
        lon.append(65.0+ix*0.25)
    lat=[]
    for iy in range(0,80):
        lat.append(25.0+(79-iy)*0.25)        
    defv=-9999    
    mon=m
    dy=d
    nde=0
    for i in range(0,ndd+1):
        dy=d+i-nde
        wk,days=calendar.monthrange(y,mon)
        #print dy,mon
        if dy>days:
            mon=mon+1
            dy=dy-days
            nde=days+nde
    filename='TP_DBMA'+'%4.4i'%y+'%2.2i'%mon+'%2.2i'%dy+'.asc'
    print filename
    fpath=dirTP+filename
    onedim=readAscii(fpath,6)
    data=np.zeros(shape=(80,160),dtype=float)
    for iy in range(0,80):
        for ix in range(0,160):
            k=iy*160+ix
            data[iy,ix]=onedim[k]
            if  data[iy,ix]==defv:
                data[iy,ix]=None
    return lon,lat,data
#########################
def getCN05rain():
    nxc05=283
    nyc05=163
    isy=1961
    lon=[]
    for ix in range(0,nxc05):
        lon.append(69.75+ix*0.25)
    lat=[]
    for iy in range(0,nyc05):
        lat.append(14.75+iy*0.25)
    cn05rain=np.zeros(shape=(366,nyc05,nxc05),dtype=float)
    dirCN05='K:/DATA/CN05/CN05.1/daily/'
    filename='CN05.1_Pre_1961_2012_daily_025x025.dat'
    fpath=dirCN05+filename
    onedim=readBin(fpath)
    k=0
    #year=iyr+isy
    nday=isYear(2010)
    for iday in range(0,nday):
        for iy in range(0,nyc05):
            for ix in range(0,nxc05):
                cn05rain[iday,iy,ix]=onedim[k]
                k=k+1
    return lon,lat,cn05rain
def getTRMM(y,m,d,nd):
    dirin=''
    return lon,lat,rain 
###############################################################################
###############################################################################
dirin1='Z:/CRM/500m/'
dirin2='Z:/CRM/SHLH/'
dirpic='D:/Work/MyPaper/PhD05/Pics/OBS_COM/'
diro='D:/Work/MyPaper/PhD04/Cases/ERA/FORCING/'
ndataset=['HY','CN05','TRMM']
n=len(ndataset)
astr=[r'$(a)$',r'$(b)$', r'$(c)$',r'$(d)$',r'$(e)$',r'$(f)$']
years=[2010,2010,2010]
mons=[7,6,6]
days=[3,3,2]
charsize=20
font = {'family' : 'serif',
        'color'  : 'k',
        'weight' : 'normal',
        'size'   : 18,
        }   
################################################################
nxc05=283
nyc05=163
iscy=1961
lonc05,latc05,cn05rain=getCN05rain()  #cn05rain=np.zeros(shapes=(52,366,nxc05,nyc05),dtype=float)
nd=getjuday(2010,6,1)
iyc=2010-1961
for idd in range(0,92): # June to Sempt
    fig,ax=plt.subplots(nrows=2,ncols=1,figsize=(12,10))
    jc=0
    jr=0
    ij=1
    for idn in range(0,2):
        if jc==2:
            jc=0
            jr=jr+1
        if idn==1:
            zdat=cn05rain[nd+idd,:,:]
            lon=lonc05
            lat=latc05
        elif idn==0:
            print idd
            lon,lat,zdat=getTPrain(2010,6,1,idd)
        elif idn==2:
            lon,lat,zdat=getTRMM(2010,6,1,idd)
        plt.subplot(2,1,ij)
        m=Basemap(projection='lcc', llcrnrlon=75.,llcrnrlat=25.,urcrnrlon=105.,urcrnrlat=45.,
          lat_1=15.,lat_2=45.,lat_0=32.,lon_0=90.,rsphere=6371200., resolution='l') 
        m.drawcoastlines() # 显示地图海岸线
        m.drawcountries() # 显示国界线
        m.drawstates() # 显示国界线
        parallels = np.arange(-90,90,10.) #地图上的纬度线，间隔是10，范围是-90到90
        m.drawparallels(parallels,labels=[1,0,0,0],fontsize=14) #地图上画出
        # draw meridians
        meridians = np.arange(0.,360.,10.) #地图上的经度线，间隔是10，范围是-90到90
        m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=14) # 地图上画出
        ny=len(lat)
        nx=len(lon)
        lon_grid=np.ndarray(shape=(ny,nx),dtype=float)
        lat_grid=np.ndarray(shape=(ny,nx),dtype=float)
        for i in range(0,ny):
            for j in range(0,nx):
                lon_grid[i,j]=lon[j]
                lat_grid[i,j]=lat[i]
        x, y = m(lon_grid, lat_grid) # compute map proj coordinates. 
        clevs= range(0,15,2)  # 等值线间隔为2，从0开始
        cs = m.contourf(x,y,zdat,clevs,cmap=cm.terrain,extend='both')
                #cbar = m.colorbar(cs,location='bottom')#,pad="5%") # 色标
        #cbar.set_label(r'Rianfall',fontsize=16) # 色标下面标注单位
        ##########################
        plt.title(ndataset[idn],fontsize=16)
        ij=ij+1
        jc=jc+1
    #cax = fig.add_axes([0.01, 0.2, 0.02, 0.6])
    #fig.colorbar(axbar, cax,extend='both',
    #   spacing='uniform', orientation='vertical')
    fig.subplots_adjust(left=0.11,bottom=0.14,right=1-0.08,top=1-0.08,hspace=0.3,wspace=0.3)
    cax = fig.add_axes([0.15, 0.06, 0.7, 0.03])
    fig.colorbar(cs, cax,extend='both',
        spacing='uniform', orientation='horizontal')               
    plt.savefig(dirpic+'Day'+'%2.2i'%idd+'TP_rianfall.png',dpi=300)        
    #plt.show()
    plt.close()


