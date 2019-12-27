#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 08 18:36:31 2018

@author: jhchen
"""
from netCDF4 import Dataset #用于读取netcdf文件
from mpl_toolkits.basemap import Basemap# 地图
import matplotlib.cm as cm
import numpy as np  # 数组，数值计算
import matplotlib.pyplot as plt  # 画图 模块
import math  #数学公式模块
import string  #字符串处理
import os    # 系统模块，可以建立文件夹，删除文件，改文件名等等
import calendar
###############################################################
def isYear(year):  
    if (year%4 == 0) & (year%100 != 0):  
        print("%d年是闰年" %year)
        return 29  
    elif year%400 == 0:  
        print("'%d'年是闰年" %year) 
        return 29
    else:  
        print("'%d'不年是闰年" %year)
        return 28
def getid(year,mon,jd):
    nd=0
    for i in range(1,mon):
         wk,days=calendar.monthrange(year,i)
         nd=nd+days
    nd=nd+jd-1
    return nd
dirin='L:/DATA/ERA_Interim/X2.5/'
dirout='D:/Work/MyPaper/PhD05/DATA/RW1/'
regions=['ETP']#,'MLYR']
filevars=['uwnd','vwnd','sh']
varsinfiles=['u','v','q']
years=[1994,2009]
mons=[4,4,4]
days=[1,1,1]
ndays=30+31+60+31+31+30 # month 4 5 6 7 8 9
ng=len(regions)
nf=len(filevars)
g=9.8
plv=[1000.,975.,950.,925.,900.,875.,850.,825.,800.,775.
    ,750.,700.,650.,600.,550.,500.,450.,400.,350.,300.
    ,250.,225.,200.,175.,150.,125.,100.,70.,50.,30.,20.
    ,10.,7.,5.,3.,2.,1.]
nz=len(plv)
ngrds=np.zeros(shape=(4,ng),dtype=int)
for i in range(0,2):
    ystrs="%4.4i"%years[i]
    if isYear(years[i])==28:
        nyd=365
    else:
        nyd=366
    nd=getid(years[i],1,1)
    alldata=np.zeros(shape=(4,3,4,nyd,nz,20),dtype=float) #sides,vars,time,nt,z, grids
    fpath=dirout+regions[0]+ystrs+'4side'+'vaporflux_IND_MS.txt'
    fout=open(fpath,'w')
    for j in range(0,4):
        strs="%2.2i"%(j*6)
        for k in range(0,nf):
            varname=filevars[k]
            var=varsinfiles[k]
            filename=ystrs+'_'+varname+'_'+strs+'.nc'
            fpath=dirin+filename            
            f=Dataset(fpath,'a')  # 打开netcdf文件
            lon=f.variables['longitude'][:]
            lat=f.variables['latitude'][:]
            raw=f.variables[var][:]####[time,level,lat,lon]
            nt=len(raw[:,0,0,0])
            nz=len(raw[0,:,0,0])
            ny=len(raw[0,0,:,0])
            nx=len(raw[0,0,0,:])
            print nt,nz,ny,nx
            for it in range(nd,nd+nyd):
                for iz in range(0,nz):
                    for ix in range(0,nx):
                        if lon[ix]==100:
                            iyy=0
                            for iy in range(0,ny):
                                if lat[iy]>=30 and lat[iy]<=37.5:
                                    alldata[0,k,j,it-nd,iz,iyy]=raw[it,iz,iy,ix]
                                    iyy=iyy+1
                            ngrds[0,i]=iyy
            for it in range(nd,nd+nyd):
                for iz in range(0,nz):
                    for ix in range(0,nx):
                        if lon[ix]==85:
                            iyy=0
                            for iy in range(0,ny):
                                if lat[iy]>=30 and lat[iy]<=37.5:
                                    alldata[1,k,j,it-nd,iz,iyy]=raw[it,iz,iy,ix]
                                    iyy=iyy+1
                            ngrds[1,i]=iyy
            for it in range(nd,nd+nyd):
                for iz in range(0,nz):                    
                    for iy in range(0,ny):
                        if lat[iy]==30.:
                            ixx=0
                            for ix in range(0,nx):
                                if lon[ix]>=85 and lon[ix]<=100:
                                    alldata[2,k,j,it-nd,iz,ixx]=raw[it,iz,iy,ix]
                                    ixx=ixx+1
                            ngrds[2,i]=ixx                                    
            for it in range(nd,nd+nyd):
                for iz in range(0,nz):
                    for iy in range(0,ny):
                        if lat[iy]==37.5:
                            ixx=0
                            for ix in range(0,nx):
                                if lon[ix]>=85 and lon[ix]<=100:
                                    alldata[3,k,j,it-nd,iz,ixx]=raw[it,iz,iy,ix]
                                    ixx=ixx+1
                            ngrds[3,i]=ixx                                       
    fpath=dirout+regions[i]+'4side'+'vaporflux_mean_IND_MS.txt'
    foutmean=open(fpath,'w')
    for isd in range(0,4):
        itme="%i "%ngrds[isd,i]
        fout.write(itme)
    fout.write('\n')
    for it in range(0,nyd):
        for j in range(0,4):
            for isd in range(0,4):
                ngd=ngrds[isd,i]
                meanflux=0.0
                imf=0.0
                for iz in range(0,nz):
                    for ix in range(0,ngd):
                        if isd<2: # west -east 
                             vflux=alldata[isd,0,j,it,iz,ix]*alldata[isd,2,j,it,iz,ix]/g
                        else:
                             vflux=alldata[isd,1,j,it,iz,ix]*alldata[isd,2,j,it,iz,ix]/g
                        print alldata[isd,2,j,it,iz,ix]
                        itme="%f "%vflux
                        fout.write(itme)
                        if iz>=13 and iz<=26 :  # 600-100
                            meanflux=meanflux+vflux
                            imf=imf+1.0
                    fout.write('\n')
                meanflux=meanflux/imf
                itme="%f "%meanflux
                foutmean.write(itme)
            foutmean.write('\n')            
    fout.close()
    foutmean.close()





















