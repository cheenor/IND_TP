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
dirin='/Volumes/DATA02/DATA/data/'
dirout='/Volumes/MacHD/Work/Papers/INDMosoon_TP/Data/'
allvars=['PRE','RHU','SSD','TEM','WIN','PRS']
allcol_num=[13,11,9,13,17,13]
nv=len(allvars)
regions=[89.9,100,34.9,37.5]
ndays=[31,28,31,30,31,30,31,31,30,31,30,31]
for iy in range(1990,2010):
    print iy
    ndd=isYear(iy)
    ndays[1]=28
    if ndd==366:
        ndays[1]=29
    yearstr='%2.2d'%iy
    fpath=dirout+'Station_'+yearstr+'.txt'
    fout=open(fpath,'w')
    fout.write('Date ')
    varstrings=''
    #for iv in range(0,nv):
    #    fout.write(allvars[iv])    
    alldata=[]
    yy0=iy
    mm0=1
    dd0=1
    allnc=[]
    for iv in range(0,nv):
        alldd=[]
        alldate=[]
        if 'PRE' in allvars[iv]:
            idx=[8,9,10]
            varstrings=varstrings+'20-8Pre '+'8-20Pre '+'20-20Pre '
        if 'RHU' in allvars[iv]:
            idx=[8]
            varstrings=varstrings+'RH '
        if 'SSD' in allvars[iv]:
            idx=[8]
            varstrings=varstrings+'SSD '
        if 'TEM' in allvars[iv]:
            idx=[8,9,10]
            varstrings=varstrings+'Temp '+'MaxTemp '+'MinTemp '
        if 'PRS' in allvars[iv]:
            idx=[8,9,10]
            varstrings=varstrings+'Pres '+'MaxPres '+'MinPres '
        if 'WIN' in allvars[iv]:
            idx=[8,9,10]
            varstrings=varstrings+'WSPD '+'MaxWSPD '+'MaxDir '
        tmpstring='SURF_CLI_CHN_MUL_DAY-'+allvars[iv]
        fpath=dirin+yearstr+'/'+tmpstring+'*'
        allpath=glob.glob(fpath)
        nf=len(allpath)
        ncol=allcol_num[iv]
        nc=len(idx)
        allnc.append(nc)        
        num=0.0
        ########################################
        for im in range(0,12):
            for idd in range(0,ndays[im]):
                datestring='%4d'%yy0+'%2.2d'%im+'%2.2d'%idd
                #print datestring
                alldate.append(datestring)
                atmp=np.zeros(shape=(nc),dtype=float)
                anum=0
                for j in range(0,nf):
                    fpath=allpath[j]
                    #print fpath
                    onedim=readAscii(fpath,0)
                    nn=len(onedim)
                    nl=int(nn/ncol)
                    tempr=np.zeros(shape=(nl,ncol),dtype=float)           
                    for i in range(0,nl):
                        for ii in range(0,ncol):
                            k=i*ncol+ii                    
                            tempr[i,ii]=onedim[k]
                        lat=tempr[i,1]/100.
                        lon=tempr[i,2]/100.
                        yy=tempr[i,4]
                        mm=tempr[i,5]
                        dd=tempr[i,6]
                        if yy==yy0 and mm==im and dd==idd:
                            if lon> regions[0] and lon<=regions[1]:
                                if lat> regions[2] and lat<=regions[3]:
                                    for ii in range(0,nc):
                                        kk=idx[ii]-1
                                        atmp[ii]=atmp[ii]+tempr[i,kk]
                                    anum=anum+1.0
                    ##################################################
                    '''
                    num,tmp=Station_loop.eachfile(onedim,region,idx,yy0,im,idd,nl,ncol)
                    for i in range(0,nc):
                        atmp[i]=atmp[i]+tmp[i]
                    anum=anum+num
                    '''
                if anum>0:
                    for ii in range(0,nc):
                        atmp[ii]=atmp[ii]/anum
                alldd.append(atmp)
        alldata.append(alldd)
        #
    ###################################3
    fout.write(varstrings)
    fout.write('\n')
    nt=len(alldate)
    for it in range(0,nt):
        for iv in range(0,nv):
            nc=allnc[iv]
            alldd=alldata[iv]
            tmp=alldd[it]
            datastring=''
            for ii in range(0,nc):
                strs='%f'%tmp[ii]
                datastring=datastring+strs+' '
            fout.write(datastring)
        fout.write('\n')
    fout.close()













