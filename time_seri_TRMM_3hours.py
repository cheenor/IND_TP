#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:43:13 2015

@author: jhchen
"""
from pytrmm import TRMM3B40RTFile as TRM3B40
import os
import datetime
import calendar
from netCDF4 import Dataset
#==============================
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
def getdatestr(yy,mm,dd,nd):
    datestart=datetime.datetime(yy,mm,dd,0,0,0)
    det=datetime.timedelta(hours=3)            
    dateiso=[]
    nt=nd*8          
    for dt in range(0,nt):
        dateiso.append(datestart+dt*det)
    xdate=[]               
    for tm in dateiso:
        xdate.append(datetime.datetime.strftime(tm,"%b/%d %H:%M"))
    return xdate  
os.system("cls")
dirin='/Volumes/DATA02/DATA/TRMM/'
dirout='/Volumes/MacHD/Work/Papers/INDMosoon_TP/Data/'
regions=['ETP','WTP','PRD','MLYR','NPC','NEC']
slon =[90.  , 80. , 107.5 , 110. , 110. , 120. ]
elon =[100. , 90. , 117.5 , 120. , 120. , 130. ]
slat =[27.5 , 27.5, 17.5  , 25.  , 32.5 , 40.  ]
elat =[37.5 , 37.5, 27.5  , 35.  , 42.5 , 50.  ]
# the start date of ever region and how many days for every region.
nag=len(regions)
#get the basic information of the data TRMM 3B40
allvars=['precipitation',
    'relativeError',
    'satPrecipitationSource',
    'HQprecipitation',
    'IRprecipitation',
    'satObservationTime',
    'nlon',
    'nlat']
ilon=0 
for ig in range(0,nag):
    for iy in range(2006,2011):
        dm2=isYear(iy)
        if  dm2==28:
            ndd=265
        if dm2==29:
            ndd=366
        yearstr="%d"%iy
        fpath=dirout+regions[ig]+"-Year"+yearstr+"_TRMM3B42_3hrs_025deg.txt"
        fout=open(fpath,"w")
        fout.write("Date ")
        fout.write("Precipitation")
        fout.write("\n")
        fout.write('%d'%ndd)
        fout.write("\n")
        for im in range(0,12):
            imm=im+1
            monrng=calendar.monthrange(iy,imm)
            mds=monrng[1]
            monstr='%2.2d'%imm
            for idd in range(0,mds):
                daystr='%2.2d'%(idd+1)
                for ih in range(0,24,3):
                    hourstr='%2.2d'%ih
                    datestr=yearstr+monstr+daystr+'.'+hourstr
                    filename='3B42.'+datestr+'.7.HDF.nc4'
                    fpath=dirin+filename
                    #print fpath
                    if os.path.isfile(fpath):
                        print fpath
                        f=Dataset(fpath,'a')  # 打开netcdf文件
                        if ilon==0:
                            lon=f.variables['nlon'][:]
                            lat=f.variables['nlat'][:]
                            nx=len(lon)
                            ny=len(lat)
                            ilon=1
                        precip=f.variables['precipitation'][:]
                        cont=0.
                        tmp=0.
                        for ix in range(0,nx):
                            if lon[ix]>(slon[ig]) and lon[ix]<(elon[ig]):
                                for iy in range(0,ny):
                                    if lat[iy]>slat[ig] and lat[iy]<elat[ig]:
                                        if precip[ix,iy]>=0.0 :
                                            tmp=tmp+precip[ix,iy]
                                            cont=cont+1.
                        if cont>0:
                            item="%f "%(tmp/cont)
                        else:
                            item='-9'
                        fout.write(item)
                        del precip
                    else:
                        filename='3B42.'+datestr+'.7A.HDF.nc4'
                        fpath=dirin+filename
                        print fpath
                        if os.path.isfile(fpath):
                            f=Dataset(fpath,'a')  # 打开netcdf文件
                            if ilon==0:
                                lon=f.variables['nlon'][:]
                                lat=f.variables['nlat'][:]
                                nx=len(lon)
                                ny=len(lat)
                                ilon=1
                            precip=f.variables['precipitation'][:]
                            cont=0.
                            tmp=0.
                            for ix in range(0,nx):
                                if lon[ix]>(slon[ig]) and lon[ix]<(elon[ig]):
                                    for iy in range(0,ny):
                                        if lat[iy]>slat[ig] and lat[iy]<elat[ig]:
                                            if precip[ix,iy]>=0.0 :
                                                tmp=tmp+precip[ix,iy]
                                                cont=cont+1.
                            if cont>0:
                                item="%f "%(tmp/cont)
                            else:
                                item='-9'
                            fout.write(item)
                            del precip
                        else:
                            fout.write("-9")  # there is no data file
                    fout.write("\n")
        fout.close()
            
