#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 

@author: chenjh
"""
import matplotlib as mpl 
#matplotlib.use('Agg')
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import datetime
import numpy as np
from matplotlib import pyplot as plt
import math
import string
from pylab import *
import imageio
from matplotlib.font_manager import FontProperties
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['contour.negative_linestyle'] = 'dashed'
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['xtick.labelsize'] = 12
plt.rc('lines', linewidth=4)
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
                #if string.atof(strs)>0 :
                #  print strs
    del linesplit
    f.close()
    return onedim
#
def getmonmean(datin,ndays):
    nx=len(datin[:,0])
    ny=len(datin[0,:])
    datout=np.zeros(shape=(6,nx),dtype=float)
    for ix in range(0,nx):
        ij=0
        a=0
        im=3
        for iy in range(0,ny): 
            a=a+datin[ix,iy]
            ij=ij+1
            if ij==ndays[im]:
                datout[im-3,ix]=a/(ij*1.0)
                ij=0
                a=0.0
                im=im+1
    return datout
#############################################
def utc2ltc(nday,ndt,dat,tdt,dt):   # dat[nz,ndt]
    newdat=np.zeros(shape=(ndt,nday),dtype=float)
    dt=15
    ddt=int(tdt*60/dt)
    for k in range(0,nday):
        kk=k
        for it in range(0,ndt):
            a=dat[k,it]
            #itt=it
            itt=it+ddt
            if itt>(ndt-1):
                itt=itt-(ndt-1)
            newdat[itt,kk]=a
    return newdat
def utc2ltc2(nday,ndt,dat,tdt,dt):
    newdat=np.zeros(shape=(nday,ndt),dtype=float)
    dt=15
    ddt=int(tdt*60/dt)
    for k in range(0,nday):
        kk=k
        for it in range(0,ndt):
            a=dat[k,it]
            #itt=it
            itt=it+ddt
            if itt>(ndt-1):
                itt=itt-(ndt-1)
            newdat[kk,itt]=a
    return newdat
def plot1(raindu,mclddu,nt,nday,xdat,zdat,dirpic,addstr,xtime,xdate):
    #
    fig,ax=plt.subplots(nrows=2,ncols= 2,figsize=(16,8)) # x z
    plt.subplot(2,2,1)
    tdt=6
    dt=15
    ndt=nt
    dat=utc2ltc(nday,ndt,raindu,tdt,dt)
    ax[0,0]=plt.contourf(xdat,zdat,dat,extend='both')
    print nday
    #print dat[180,:]
    marknm='(a) Rainfall'
    plt.title(marknm,fontsize=16)
    plt.colorbar()
    #
    axx=fig.add_subplot(2,2,1)
    plt.axis([0,nday,0,96])
    axx.set_xticks(range(0,nday,15))  
    xticklabels = [xdate[nn] for nn in range(0,nday,15)] 
    axx.set_xticklabels(xticklabels, size=16,rotation=45)
    #plt.xlabel(r'Date', fontdict=font)
    axx.set_yticks(range(0,nt,12))  
    yticklabels = [xtime[nn] for nn in range(0,nt,12)] 
    axx.set_yticklabels(yticklabels, size=16,rotation=45)
    plt.ylabel(r'LST', fontdict=font)
    #
    plt.subplot(2,2,2)
    dat=utc2ltc(nday,ndt,mclddu[:,:,0],tdt,dt)
    ax[0,1]=plt.contourf(xdat,zdat,dat,extend='both')
    marknm='(b) Cloud Water Content'
    plt.title(marknm,fontsize=16)
    plt.colorbar()
    axx=fig.add_subplot(2,2,2)
    plt.axis([0,nday,0,96])
    axx.set_xticks(range(0,nday,15))  
    xticklabels = [xdate[nn] for nn in range(0,nday,15)] 
    axx.set_xticklabels(xticklabels, size=16,rotation=45)
    #plt.xlabel(r'Date', fontdict=font)
    axx.set_yticks(range(0,nt,12))  
    yticklabels = [xtime[nn] for nn in range(0,nt,12)] 
    axx.set_yticklabels(yticklabels, size=16,rotation=45)
    plt.ylabel(r'LST', fontdict=font)
    #
    plt.subplot(2,2,3)
    dat=utc2ltc(nday,ndt,mclddu[:,:,1],tdt,dt)
    ax[1,0]=plt.contourf(xdat,zdat,dat,extend='both')
    marknm='(c) Max CWC'
    plt.title(marknm,fontsize=16)
    plt.colorbar()
    axx=fig.add_subplot(2,2,3)
    plt.axis([0,nday,0,96])
    axx.set_xticks(range(0,nday,15))  
    xticklabels = [xdate[nn] for nn in range(0,nday,15)] 
    axx.set_xticklabels(xticklabels, size=16,rotation=45)
    #plt.xlabel(r'Date', fontdict=font)
    axx.set_yticks(range(0,nt,12))  
    yticklabels = [xtime[nn] for nn in range(0,nt,12)] 
    axx.set_yticklabels(yticklabels, size=16,rotation=45)
    plt.ylabel(r'LST', fontdict=font)
    #
    plt.subplot(2,2,4)
    dat=utc2ltc(nday,ndt,mclddu[:,:,2],tdt,dt)
    ax[1,1]=plt.contourf(xdat,zdat,dat,extend='both')
    marknm='(d) Max CWC Lev.'
    plt.title(marknm,fontsize=16)
    plt.colorbar()
    axx=fig.add_subplot(2,2,4)
    plt.axis([0,nday,0,96])
    axx.set_xticks(range(0,nday,15))  
    xticklabels = [xdate[nn] for nn in range(0,nday,15)] 
    axx.set_xticklabels(xticklabels, size=16,rotation=45)
    #plt.xlabel(r'Date', fontdict=font)
    axx.set_yticks(range(0,nt,12))  
    yticklabels = [xtime[nn] for nn in range(0,nt,12)] 
    axx.set_yticklabels(yticklabels, size=16,rotation=45)
    plt.ylabel(r'LST', fontdict=font)
    '''
    plt.title(marknm,fontsize=16)    
    axx=plt.subplot(3,4,ij)
    xmajorLocator   = MultipleLocator(4)
    axx.xaxis.set_major_locator(xmajorLocator) 
    ymajorLocator   = MultipleLocator(4)
    axx.yaxis.set_major_locator(ymajorLocator)
    '''
    #plt.xlabel(r'Date', fontdict=font)
    #plt.ylabel(r'Time', fontdict=font)
    #cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
    plt.subplots_adjust(left = 0.08, wspace = 0.12, hspace = 0.4, \
        bottom = 0.1, right=0.98, top = 0.90)
    #plt.show()
    plt.savefig(dirpic+"du_rain+cld_evo_"+addstr+".png",dpi=300)          
    #plt.show()
    plt.close()
def plot2(qdday,nday,km,dirpic,addstr,xdate,Z):
    xdat=range(nday)
    zdat=Z
    nz=len(Z)
    dat=qdday[:,:,0]
    fig,ax=plt.subplots(nrows=1,ncols= 1,figsize=(12,4))
    plt.subplot(1,1,1)
    ax=plt.contourf(xdat,zdat,dat,extend='both')
    marknm='DCC cloud water content'
    plt.title(marknm,fontsize=16)
    plt.colorbar()
    axx=fig.add_subplot(1,1,1)
    plt.axis([0,nday,0,16])
    axx.set_xticks(range(0,nday,15))  
    xticklabels = [xdate[nn] for nn in range(0,nday,15)] 
    axx.set_xticklabels(xticklabels, size=16,rotation=45)   
    ymajorLocator   = MultipleLocator(4)
    axx.yaxis.set_major_locator(ymajorLocator)
    #plt.xlabel(r'Date', fontdict=font)
    plt.ylabel(r'Height (km)', fontdict=font)
    plt.xlabel(r'Date', fontdict=font)
    #plt.ylabel(r'Time', fontdict=font)
    #cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
    plt.savefig(dirpic+"time_evo_dcc_tcwc"+addstr+".png",dpi=300)          
    #plt.show()
    plt.close()
    dat=qdday[:,:,1]*100
    fig,ax=plt.subplots(nrows=1,ncols= 1,figsize=(12,4))
    plt.subplot(1,1,1)
    ax=plt.contourf(xdat,zdat,dat,extend='both')
    marknm='DCC Frequency'
    plt.title(marknm,fontsize=16)
    plt.colorbar()
    axx=fig.add_subplot(1,1,1)
    plt.axis([0,nday,0,16])
    axx.set_xticks(range(0,nday,15))  
    xticklabels = [xdate[nn] for nn in range(0,nday,15)] 
    axx.set_xticklabels(xticklabels, size=16,rotation=45)   
    ymajorLocator   = MultipleLocator(4)
    axx.yaxis.set_major_locator(ymajorLocator)
    #plt.xlabel(r'Date', fontdict=font)
    plt.ylabel(r'Height (km)', fontdict=font)
    plt.xlabel(r'Date', fontdict=font)
    #plt.ylabel(r'Time', fontdict=font)
    #cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
    plt.savefig(dirpic+"time_evo_dcc_frq_"+addstr+".png",dpi=300)          
    #plt.show()
    plt.close()
def plot3(ftday,nday,km,dirpic,addstr,xdate,Z,cloudlevs,cloudclors,ndays):
    mft=np.zeros(shape=(km,km),dtype=float)
    zdat=Z
    im=3 #
    it=0
    frames = []
    for i in range(0,nday):
        strs='%2.2i'%i
        adat=ftday[i,:,:]*10000
        '''
        fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(8,8))
        plt.subplot(1,1,1)
        #zdat[0,:]=0.0   ## the first level is below surface ground
        ax=plt.contourf(zdat,zdat,adat,colors=cloudclors, levels=cloudlevs,extend='both')
        marknm='Day'+strs
        plt.title(marknm,fontsize=16)
        axx=fig.add_subplot(1,1,1)
        plt.axis([0, 16, 0, 16])
        xmajorLocator   = MultipleLocator(4)
        axx.xaxis.set_major_locator(xmajorLocator) 
        ymajorLocator   = MultipleLocator(4)
        axx.yaxis.set_major_locator(ymajorLocator)
        plt.xlabel(r'Cloud Base Height ($km$)', fontdict=font)
        plt.ylabel(r'Cloud Top Height ($km$)', fontdict=font)
        figtitle = r"Frequency of all cloud cells ($10^{-2}$ %)"
        fig.text(0.5, 0.95, figtitle,
            horizontalalignment='center',
            fontproperties=FontProperties(size=18))
        #cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
        cax=fig.add_axes([0.92, 0.2, 0.05, 0.6])
        fig.colorbar(ax,cax,orientation='vertical',extend='both', # 'horizontal'
            extendfrac='auto',  spacing='uniform')
        #plt.show()
        fpath=dirpic+'Raw/'+addstr+"CloudCellsTopBase_fortran_color_DAY"+strs+".png"
        plt.savefig(fpath,dpi=180)          
        #plt.show()
        plt.close()
        img = imageio.imread(fpath)
        frames.append(img)
        '''
        ####
        if it==ndays[im]:
            monstr='Mon'+'%2.2i'%(im+1)
            fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(8,8))
            plt.subplot(1,1,1)
            #zdat[0,:]=0.0   ## the first level is below surface ground
            ax=plt.contourf(zdat,zdat,mft,colors=cloudclors, levels=cloudlevs,extend='both')
            marknm=monstr
            plt.title(marknm,fontsize=16)    
            plt.axis([0, 16, 0, 16])
            axx=fig.add_subplot(1,1,1)
            xmajorLocator   = MultipleLocator(4)
            axx.xaxis.set_major_locator(xmajorLocator) 
            ymajorLocator   = MultipleLocator(4)
            axx.yaxis.set_major_locator(ymajorLocator)
            plt.xlabel(r'Cloud Base Height ($km$)', fontdict=font)
            plt.ylabel(r'Cloud Top Height ($km$)', fontdict=font)
            figtitle = r"Frequency of all cloud cells ($10^{-2}$ %)"
            fig.text(0.5, 0.95, figtitle,
                horizontalalignment='center',
                fontproperties=FontProperties(size=20))
            #cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
            cax=fig.add_axes([0.92, 0.2, 0.05, 0.6])
            fig.colorbar(ax,cax,orientation='vertical',extend='both', # 'horizontal'
                extendfrac='auto',  spacing='uniform')
            #plt.show()
            plt.savefig(dirpic+addstr+"CloudCellsTopBase_fortran_color_"+monstr+".png",dpi=300)          
            #plt.show()
            plt.close()
            mft=np.zeros(shape=(km,km),dtype=float)
            it=0
            im=im+1      
        else:
            for ik in range(0,km):
                for iz in range(0,km):
                    frg=1.0/(ndays[im]*1.0)
                    mft[ik,iz]=mft[ik,iz]+ftday[i,ik,iz]*frg*10000
                    #if mft[ik,iz]>0:
                    #    print mft[ik,iz]
        it=it+1
    #gifname=dirpic+addstr+'CloudCellsTopBase_fortran_color_Dayly_evo.gif'    
    #imageio.mimsave(gifname,frames,'GIF',duration=0.1)
def plot4(datin,nday,nb,ndp,dirpic,addstr,rainbin,dpbin,rainstr,dptstr,
          cldty,ndays,cloudclors,cloudlevs):
    xdat=range(nb)
    ydat=range(ndp)
    mdat=np.zeros(shape=(nb,ndp),dtype=float)
    it=1
    im=3
    frames = []
    #print 'xdat',xdat
    for i in range(0,nday):
        strs='%2.2i'%i
        adat=datin[i,:,:]
        '''
        fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(8,8))
        plt.subplot(1,1,1)
        #zdat[0,:]=0.0   ## the first level is below surface ground
        ax=plt.contourf(ydat,xdat,adat,extend='both')
        marknm='Day'+strs
        plt.title(marknm,fontsize=16)
        plt.axis([0, ndp-1, 0, nb-1])
        axx=fig.add_subplot(1,1,1)
        plt.axis([0, ndp-1, 0, nb-1])
        #print 'nb',nb
        axx.set_yticks(range(0,nb,2))  
        yticklabels = [rainstr[nn] for nn in range(0,nb,2)] 
        axx.set_yticklabels(yticklabels, size=16,rotation=45)   
        axx.set_xticks(range(0,ndp,2))  
        xticklabels = [dptstr[nn] for nn in range(0,ndp,2)] 
        axx.set_xticklabels(xticklabels, size=16,rotation=45) 
        #xmajorLocator   = MultipleLocator(4)
        #axx.xaxis.set_major_locator(xmajorLocator) 
        #ymajorLocator   = MultipleLocator(4)        
        plt.xlabel(r'Cloud Depth', fontdict=font)
        plt.ylabel(r'Rainfall Rate', fontdict=font)
        #figtitle = r"Frequency of all cloud cells ($10^{-2}$ %)"
        #fig.text(0.5, 0.95, figtitle,
        #    horizontalalignment='center',
        #    fontproperties=FontProperties(size=20))
        #cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
        cax = fig.add_axes([0.92, 0.2, 0.03, 0.6])
        fig.colorbar(ax,cax,orientation='vertical',extend='both', # 'horizontal'
            extendfrac='auto',  spacing='uniform')
        #plt.show()
        fpath=dirpic+'Raw/'+addstr+cldty+"2dpt_fortran_color_DAY"+strs+".png"
        plt.savefig(fpath,dpi=180)          
        #plt.show()
        plt.close()
        img = imageio.imread(fpath)
        frames.append(img)
        '''
        if it==ndays[im]:
            monstr='Mon'+'%2.2i'%(im+1)
            fig,ax=plt.subplots(nrows=1,ncols=1,figsize=(8,8))
            plt.subplot(1,1,1)
            #zdat[0,:]=0.0   ## the first level is below surface ground
            ax=plt.contourf(ydat,xdat,mdat,colors=cloudclors, levels=cloudlevs,extend='both')
            marknm=monstr
            plt.title(marknm,fontsize=16)
            axx=fig.add_subplot(1,1,1)
            axx=fig.add_subplot(1,1,1)
            plt.axis([0, ndp-1, 0, nb-1])
            axx=fig.add_subplot(1,1,1)
            plt.axis([0, ndp-1, 0, nb-1])
            axx.set_yticks(range(0,nb,2))  
            yticklabels = [rainstr[nn] for nn in range(0,nb-1,2)] 
            axx.set_yticklabels(yticklabels, size=16,rotation=45)   
            axx.set_xticks(range(0,ndp,2))  
            xticklabels = [dptstr[nn] for nn in range(0,ndp,2)] 
            axx.set_xticklabels(xticklabels, size=16,rotation=45)    
            plt.xlabel(r'Cloud Depth', fontdict=font)
            plt.ylabel(r'Rainfall Rate', fontdict=font)
            #cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
            cax = fig.add_axes([0.90, 0.2, 0.03, 0.6])
            fig.colorbar(ax,cax,orientation='vertical',extend='both', # 'horizontal'
                extendfrac='auto',  spacing='uniform')
            #plt.show()
            plt.savefig(dirpic+addstr+cldty+"2dpt_fortran_color_"+monstr+".png",dpi=300)          
            #plt.show()
            plt.close()
            mdat=np.zeros(shape=(nb,ndp),dtype=float)
            it=0
            im=im+1      
        else:
            for ik in range(0,nb):
                for iz in range(0,ndp):
                    frg=1.0/(ndays[im]*1.0)
                    mdat[ik,iz]=mdat[ik,iz]+datin[i,ik,iz]*frg*100
        it=it+1
    #gifname=dirpic+addstr+cldty+"2dpt_fortran_color_dayly.gif"    
    #imageio.mimsave(gifname,frames,'GIF',duration=0.1)
#def plot5(datin,nm,ndt,nb,ndp,dirpic,addstr,rainbin,dpbin,rainstr,dptstr,cldty):
#    for im in range(0,nm):
#        print im
def plot6(dccdu,nm,ndt,dirpic,addstr,xtime,dccfeas):
    linec=["#E16A86","#AA9000","#00AA5A","#00A6CA","#B675E0","#E16A86"]
    nx=len(xtime)
    xdat=range(ndt)
    tdt=6
    dt=15
    for im in range(0,nm):
        monstrs='Mon'+'%2.2i'%(im+4)
        fig,ax=plt.subplots(nrows=2,ncols=3,figsize=(20,10))
        jc=0
        jr=0
        for i in range(0,5):
            if jc==2:
                jc=0
                jr=jr+1
            adat=dccdu[im,:,i]
            newdat=np.zeros(shape=(ndt),dtype=float)
            ddt=int(tdt*60/dt)
            for it in range(0,ndt):
                a=adat[it]
                itt=it+ddt
                if itt>(ndt-1):
                    itt=itt-ndt+1
                newdat[itt]=a
            ax[jc,jr].plot(xdat,newdat,c=linec[i],label=dccfeas[i])
            ax[jc,jr].set_xticks(range(0,ndt,6))  
            xticklabels = [xtime[nn] for nn in range(0,ndt,6)] 
            ax[jc,jr].set_xticklabels(xticklabels, size=16,rotation=45)
            ax[jc,jr].legend()
            jc=jc+1
        plt.savefig(dirpic+addstr+"_dcc_feas_du_"+monstrs+".png",dpi=300)          
        plt.close()
def plot7(qddu,nm,ndt,km,dirpic,addstr,xtime,Z): #nm,ndt,km
    nx=len(xtime)
    xdat=range(0,nx)
    nz=len(Z)
    zdat=Z
    tdt=6
    dt=15
    for im in range(0,nm):
        monstrs='Mon'+'%2.2i'%(im+4)
        fig,ax=plt.subplots(nrows=1,ncols=2,figsize=(16,6))
        adat=qddu[im,:,:,0]
        dat=utc2ltc2(km,ndt,adat,tdt,dt)      #utc2ltc(nday,ndt,cdat,tdt,dt)
        plt.subplot(1,2,1)
        ax[0]=plt.contourf(xdat,zdat,dat,extend='both')
        marknm='(a) DCC cloud water content'
        plt.title(marknm,fontsize=16)
        plt.colorbar()
        #
        axx=fig.add_subplot(1,2,1)
        plt.axis([0,ndt,0,16])
        axx.set_xticks(range(0,ndt,12))  
        xticklabels = [xtime[nn] for nn in range(0,ndt,12)] 
        axx.set_xticklabels(xticklabels, size=16,rotation=45)
        plt.xlabel(r'LST', fontdict=font)        
        #
        adat=qddu[im,:,:,1]*100.0
        dat=utc2ltc2(km,ndt,adat,tdt,dt)      #utc2ltc(nday,ndt,cdat,tdt,dt)
        plt.subplot(1,2,2)
        ax[0]=plt.contourf(xdat,zdat,dat,extend='both')
        marknm='(b) DCC Frequency'
        plt.title(marknm,fontsize=16)
        plt.colorbar()
        #
        axx=fig.add_subplot(1,2,2)
        plt.axis([0,ndt,0,16])
        axx.set_xticks(range(0,ndt,12))  
        xticklabels = [xtime[nn] for nn in range(0,ndt,12)] 
        axx.set_xticklabels(xticklabels, size=16,rotation=45)
        plt.xlabel(r'LST', fontdict=font)  

        plt.savefig(dirpic+addstr+"_dcc_frq+cwc_du_"+monstrs+".png",dpi=300)          
        plt.close()
def getmonmm(datin,ndays,nday,nm,nb,ndp):
    datout=np.zeros(shape=(nm,nb,ndp),dtype=float)
    im=3
    for ib in range(0,nb):
        for i in range(0,ndp):
            ij=0
            a=0.0
            im=3
            for idy in range(0,nday): 
                a=a+datin[idy,ib,i]
                ij=ij+1
                if ij==ndays[im]:
                    datout[im-3,ib,i]=a/(ij*1.0)
                    ij=0
                    a=0.0
                    im=im+1
    return datout
def getmean(allqdday,allftday,allpre5dptday,allpre5dccday,alldcc,\
    allpre5dptdu,allpre5dccdu,alldccdu,allqddu, \
    allraindu,allmclddu,nt,km,nday,nb,ndp,ndt,nm,years):
    #####
    qdday=np.zeros(shape=(km,nday,2),dtype=float)
    ftday=np.zeros(shape=(nday,km,km),dtype=float)
    pre5dptday=np.zeros(shape=(nday,nb,ndp),dtype=float)
    pre5dccday=np.zeros(shape=(nday,nb,ndp),dtype=float)
    dcc=np.zeros(shape=(nt,5),dtype=float)
    pre5dptdu=np.zeros(shape=(nm,ndt,nb,ndp),dtype=float)
    pre5dccdu=np.zeros(shape=(nm,ndt,nb,ndp),dtype=float)
    dccdu=np.zeros(shape=(nm,ndt,5),dtype=float)
    qddu=np.zeros(shape=(nm,km,ndt,2),dtype=float)
    ftdu=np.zeros(shape=(nm,ndt,km,km),dtype=float)
    raindu=np.zeros(shape=(nday,ndt),dtype=float)
    mclddu=np.zeros(shape=(nday,ndt,3),dtype=float)   
    ny=len(years)
    print years
    print len(allqdday)
    for iy in range(0,ny):
        iyy=years[iy]-1990
        print iyy,years[iy]
        a=allqdday[iyy]
        for i in range(0,nday):
            for k in range(0,km):
                for j in range(0,2): 
                    qdday[k,i,j]=qdday[k,i,j]+a[k,i,j]/(ny*1.0)
        a=allftday[iyy]
        for i in range(0,nday):
            for k in range(0,km):
                for j in range(0,km):
                    ftday[i,j,k]=ftday[i,j,k]+a[i,j,k]/(ny*1.0)
        a=allpre5dptday[iyy]
        for i in range(0,nday):
            for k in range(0,nb):
                for j in range(0,ndp):
                    pre5dptday[i,k,j]=pre5dptday[i,k,j]+a[i,k,j]/(ny*1.0)
        a=allpre5dccday[iyy]
        for i in range(0,nday):
            for k in range(0,nb):
                for j in range(0,ndp):
                    pre5dccday[i,k,j]=pre5dccday[i,k,j]+a[i,k,j]/(ny*1.0)
        a=alldcc[iyy]
        for i in range(0,nt):
            for j in range(0,5):
                dcc[i,j]=dcc[i,j]+a[i,j]/(ny*1.0)
        a=allpre5dptdu[iyy]
        for im in range(0,nm):
            for it in range(0,ndt):
                for i in range(0,nb):
                    for j in range(0,ndp):
                        pre5dptdu[im,it,i,j]=pre5dptdu[im,it,i,j]+a[im,it,i,j]/(ny*1.0)
        a=allpre5dccdu[iyy]
        for im in range(0,nm):
            for it in range(0,ndt):
                for i in range(0,nb):
                    for j in range(0,ndp):
                        pre5dccdu[im,it,i,j]=pre5dccdu[im,it,i,j]+a[im,it,i,j]/(ny*1.0)
        a=alldccdu[iyy]
        for im in range(0,nm):
            for it in range(0,ndt):
                for i in range(0,5):   
                    dccdu[im,it,i]=dccdu[im,it,i]+a[im,it,i]/(ny*1.0)
        a=allqddu[iyy]
        for im in range(0,nm):
            for it in range(0,ndt):
                for i in range(0,km):
                    for j in range(0,2):    
                        qddu[im,i,it,j]=qddu[im,i,it,j]+a[im,i,it,j]/(ny*1.0)
        a=a=allftdu[iyy]
        for im in range(0,nm):
            for it in range(0,ndt):
                for i in range(0,km):
                    for j in range(0,km):  
                        ftdu[im,it,i,j]=ftdu[im,it,i,j]+a[im,it,i,j]/(ny*1.0)
        a=allraindu[iyy]
        b=allmclddu[iyy]
        for im in range(0,nday):
            for it in range(0,ndt):
                for j in range(0,4):                  
                    if j==0:
                        raindu[im,it]=raindu[im,it]+a[im,it]/(ny*1.0)
                    else:
                        mclddu[im,it,j-1]=mclddu[im,it,j-1]+b[im,it,j-1]/(ny*1.0)
    return qdday,ftday,pre5dptday,pre5dccday,dcc,pre5dptdu,pre5dccdu,dccdu,qddu,raindu,mclddu
#def plot8(ftdu,nm,ndt,km,dirpic,addstr,xtime,Z):
#############################################################################
#################################3
dirin='/Volumes/MacHD/Work/Papers/INDMosoon_TP/Data/'
dirpic='/Volumes/MacHD/Work/Papers/INDMosoon_TP/Pics/'
casenm='ETP2D0'

addstr='08norm'
filenames=['IND_file09_qd_day_',
  'IND_file10_ft_day_',
  'IND_file11_pre2clddpt_day_',
  'IND_file12_pre2dccdpt_day_',
  'IND_file13_dcc_feas_',
  'IND_file15_pre2clddpt_monthly_du_',
  'IND_file16_pre2dccdpt_monthly_du_',
  'IND_file17_dcc_feas_monthly_du_',
  'IND_file18_qd_monthly_du_',
  'IND_file19_ft_monthly_du_',
  'IND_file20_pre_cld_du_evo_',
   'IND_file21_pre2clddpt_mon_',
  'IND_file22_pre2dccdpt_mon_',]
Z=[ 0.0500000, 0.1643000, 0.3071000, 0.4786000 
    , 0.6786000, 0.9071000, 1.1640000, 1.4500000, 1.7640001 
    , 2.1070001, 2.4790001, 2.8789999, 3.3069999, 3.7639999 
    , 4.2500000, 4.7639999, 5.3070002, 5.8790002, 6.4790001 
    , 7.1069999, 7.7639999, 8.4499998, 9.1639996, 9.9069996 
    ,10.6800003,11.4799995,12.3100004,13.1599998,14.0500002 
    ,14.9600000,15.9099998,16.8799992,17.8799992,18.9099998]
rainbin=[0.0, 0.1,  0.2, 0.3, 0.4, 
        0.6, 0.8,  1.0, 1.2, 1.4, 
        1.6, 1.8,  2.0, 2.4, 2.8, 
        3.2, 3.6,  4.0, 4.6, 5.2, 
        5.8, 6.4,  7.0, 7.8, 8.6, 
        9.4, 10.2,  11, 12, 13]
nb=len(rainbin)
dpbin=[0.5,  1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 
    4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0,7.5, 
    8.0, 8.5, 9.0, 9.5,10]
monstrs=['April','May','June','July','Aug.','Sept.']
ndp=len(dpbin)+1
ndays=np.zeros(shape=(12),dtype=int)
for i in range(0,12):
    ndays[i]=31
ndays[1]=28
ndays[3]=30
ndays[5]=30
ndays[8]=30
ndays[10]=30
nday=30+31+30+31+31+30
nt=nday*96
nm=6
km=34
ndt=96
#################################################
nf=len(filenames)
allqdday=[]
allftday=[]
allpre5dptday=[]
allpre5dccday=[]
alldcc=[]
allpre5dptdu=[]
allpre5dccdu=[]
alldccdu=[]
allqddu=[]
allftdu=[]
allraindu=[]
allmclddu=[]
for iy in range(1990,2010):
    atrs='%4d'%iy
    addstr=atrs[2:4]+'norm'
    for l in range(0,nf):
        fpath=dirin+casenm+filenames[l]+addstr+'.txt'
        onedim=readAscii(fpath,0)
        if l==0:
            qdday=np.zeros(shape=(km,nday,2),dtype=float)
            for i in range(0,nday):
                for k in range(0,km):
                    for j in range(0,2):    # 0 cloud water, 1 frequency 
                        kk=i*km*2+k*2+j
                        qdday[k,i,j]=onedim[kk]
            allqdday.append(qdday)
        if l==1:
            ftday=np.zeros(shape=(nday,km,km),dtype=float)
            for i in range(0,nday):
                for k in range(0,km):
                    for j in range(0,km):
                        kk=i*km*km+k*km+j
                        ftday[i,j,k]=onedim[kk]
                        if k==0 or j==0:
                            ftday[i,j,k]=0
            allftday.append(ftday)
        if l==2:
            pre5dptday=np.zeros(shape=(nday,nb,ndp),dtype=float)
            for i in range(0,nday):
                for k in range(0,nb):
                    for j in range(0,ndp):
                        kk=i*nb*ndp+k*ndp+j
                        pre5dptday[i,k,j]=onedim[kk]*100
            allpre5dptday.append(pre5dptday)
        if l==3:
            pre5dccday=np.zeros(shape=(nday,nb,ndp),dtype=float)
            for i in range(0,nday):
                for k in range(0,nb):
                    for j in range(0,ndp):
                        kk=i*nb*ndp+k*ndp+j
                        pre5dccday[i,k,j]=onedim[kk]*100
            allpre5dccday.append(pre5dccday)
        if l==4:
            dcc=np.zeros(shape=(nt,5),dtype=float)
            for i in range(0,nt):
                for j in range(0,5):   # 0 depth 1 cloud water 2 max cw 3 max cw lev 4 pre
                    kk=i*5+j
                    dcc[i,j]=onedim[kk]
            alldcc.append(dcc)
        if l==5:
            pre5dptdu=np.zeros(shape=(nm,ndt,nb,ndp),dtype=float)
            for im in range(0,nm):
                for it in range(0,ndt):
                    for i in range(0,nb):
                        for j in range(0,ndp):
                            kk=im*ndt*nb*ndp+it*nb*ndp+i*ndp+j
                            pre5dptdu[im,it,i,j]=onedim[kk]*100
            allpre5dptdu.append(pre5dptdu)
        if l==6:
            pre5dccdu=np.zeros(shape=(nm,ndt,nb,ndp),dtype=float)
            for im in range(0,nm):
                for it in range(0,ndt):
                    for i in range(0,nb):
                        for j in range(0,ndp):
                            kk=im*ndt*nb*ndp+it*nb*ndp+i*ndp+j
                            pre5dccdu[im,it,i,j]=onedim[kk]*100
            allpre5dccdu.append(pre5dccdu)
        if l==7:
            dccdu=np.zeros(shape=(nm,ndt,5),dtype=float)
            for im in range(0,nm):
                for it in range(0,ndt):
                    for i in range(0,5):                    
                        kk=im*ndt*5+it*5+i
                        dccdu[im,it,i]=onedim[kk]
            alldccdu.append(dccdu)
        if l==8:
            qddu=np.zeros(shape=(nm,km,ndt,2),dtype=float)
            for im in range(0,nm):
                for it in range(0,ndt):
                    for i in range(0,km):
                        for j in range(0,2):                    
                            kk=im*ndt*km*2+it*km*2+i*2+j
                            qddu[im,i,it,j]=onedim[kk]
            allqddu.append(qddu)
        if l==9:
            ftdu=np.zeros(shape=(nm,ndt,km,km),dtype=float)
            for im in range(0,nm):
                for it in range(0,ndt):
                    for i in range(0,km):
                        for j in range(0,km):                    
                            kk=im*ndt*km*km+it*km*km+i*km+j
                            ftdu[im,it,i,j]=onedim[kk]
            allftdu.append(ftdu)
        if l==10:
            raindu=np.zeros(shape=(nday,ndt),dtype=float)
            mclddu=np.zeros(shape=(nday,ndt,3),dtype=float)       
            for im in range(0,nday):
                for it in range(0,ndt):
                    for j in range(0,4):                  
                        kk=im*ndt*4+it*4+j
                        if j==0:
                            raindu[im,it]=onedim[kk]
                        else:
                            mclddu[im,it,j-1]=onedim[kk]    # 0 CWC 1 max CWC 2 max CWC lev
            allraindu.append(raindu)
            allmclddu.append(mclddu)
####################################################################################
#--------------plot-------------------------------
font = {'family' : 'serif',
        'color'  : 'k',
        'weight' : 'normal',
        'size'   : 12,
        } 
cloudlevs=[5,10,15,20,30,40,50,60,70,80,90,100,110,120,130]
difflevs=[-70,-60,-50,-40,-30,-20,-10,-5,0,5,10,20,30,40,50,60,70]
cloudclors=['w','lightgray','plum','darkorchid','darkviolet','b','dodgerblue','skyblue','aqua',
            'greenyellow','lime','yellow','darkorange','chocolate','tomato','r']
cloudclors1=['w',"#FCF5F2","#FFEFE8","#FFE6DE","#FFDBD3","#FFD0CA","#FFC3C1",
            "#FFB6BA","#FDA8B4","#FA99B0","#F589AC","#F078AA","#EA67A9",
            "#E352A8","#DC3AA9","#CC2AA5","#B9229E","#A51A95","#91138B",
            "#7D0A81","#6B0176","#59006B","#490062"]
difcols=["#C75DAA","#CD72B2","#D385BB","#D897C3","#DEA9CC","#E3BBD5","#E8CDDE",'w',#"#ECDFE7",
    "w","#D6E5E6","#BADADC","#9DD0D1","#7DC5C7","#55BABD","#00B0B3","#00A5A9","#009B9F"]
cldcols=["#001889","#40058A","#67008C","#84008D","#9C008B","#B11E86","#C3367E","#D24E71",
    "#DE655F","#E67D45","#EB9619","#EDAF00","#EAC800","#E3E300","#DAFF47"]   
datestart=datetime.datetime(2019,1,1,0,0,0)
det=datetime.timedelta(minutes=15)            
dateiso=[]            
for dt in range(0,96):
    dateiso.append(datestart+dt*det) 
xtime=[]              
for tm in dateiso:
    xtime.append(datetime.datetime.strftime(tm,"%H")) 
###
datestart=datetime.datetime(1994,4,1,0,0,0)
det=datetime.timedelta(hours=24)            
dateiso=[]            
for dt in range(0,nday):
    dateiso.append(datestart+dt*det) 
xdate=[]              
for tm in dateiso:
    xdate.append(datetime.datetime.strftime(tm,"%d/%b"))
rainstr=[]
rainstr.append('0')
for a in rainbin:
    rainstr.append('%.1f'%a)
dptstr=[]
dptstr.append('0')
for a in dpbin:
     dptstr.append('%.1f'%a)    
dccfeas=['Depth','CWC', 'Max. CWC','Max. CWC lev.','Pre']
    #--------------raindu-----------------------------
    # plot
xdat=range(nday)
zdat=range(ndt)
#######################################
cls_raindu=[]
cls_mclddu=[]
cls_qdday=[]
cls_ftday=[]
cls_pre5dptday=[] 
cls_pre5dccday=[]
cls_dccdu=[]
cls_qddu=[]
cls_dcc=[]
cls_pre5dptdu=[]
cls_pre5dccdu=[]
for ity in range(0,3):
    if ity==0:
        strss='norm'
        slct_year=range(1990,2010)
        #slct_year=[1993,1998,2007]
    elif ity==1:
        strss='strong'
        slct_year=[1991,1992,1994,1996,2000,2001]
    elif ity==2:
        strss='weak'
        slct_year=[1995,1997,1999,2002,2008,2009]
    qdday,ftday,pre5dptday,pre5dccday,dcc,pre5dptdu,pre5dccdu,dccdu,qddu,raindu,mclddu=     \
        getmean(allqdday, allftday,allpre5dptday,allpre5dccday,alldcc,\
        allpre5dptdu,allpre5dccdu,alldccdu,allqddu, \
        allraindu,allmclddu, nt,km,nday,nb,ndp,ndt,nm,slct_year)
    cls_raindu.append(raindu)
    cls_mclddu.append(mclddu)
    cls_qdday.append(qdday)
    cls_ftday.append(ftday)
    cls_pre5dptday.append(pre5dptday) 
    cls_pre5dccday.append(pre5dccday)
    cls_dccdu.append(dccdu)
    cls_qddu.append(qddu)
    cls_pre5dptdu.append(pre5dptdu) 
    cls_pre5dccdu.append(pre5dccdu)
    cls_dcc.append(dcc)
##########################################
abstr=[r'(a)',r'(b)',r'(c)',r'(d)',r'(e)',r'(f)',r'(g)',r'(h)',r'(i)',r'(j)',
       r'(k)',r'(l)',r'(m)',r'(n)',r'(o)',r'(p)',r'(q)',r'(r)',r'(s)',r'(t)',
       r'(u)',r'(v)',r'(w)',r'(x)',r'(y)',r'(z)']
fig,ax=plt.subplots(nrows=3,ncols=nm,figsize=(16,8))
ij=1
for ity in range(0,3):
    ftday=cls_ftday[ity]
    ftday0=cls_ftday[0]
    for im in range(0,nm):        
        if ity==0:
            strss='Averaged '
            adat=ftday[im,:,:]*10000
        elif ity==1:
            strss='Strong '
            adat=ftday[im,:,:]*10000-ftday0[im,:,:]*10000
        elif ity==2:
            strss='Weak '
            adat=ftday[im,:,:]*10000-ftday0[im,:,:]*10000
        ################
        addstr=strss
        monstr=abstr[ij-1]+addstr+monstrs[im] #'Mon'+'%2.2i'%(im+4)
        plt.subplot(3,nm,ij)        
        #zdat[0,:]=0.0   ## the first level is below surface ground
        if ity==0:
            ax[ity,im]=plt.contourf(Z,Z,adat,colors=cloudclors, levels=cloudlevs,extend='both')
        else:
            ax[ity,im]=plt.contourf(Z,Z,adat,colors=difcols, levels=difflevs,extend='both')
        marknm=monstr
        plt.title(marknm,fontsize=12)    
        plt.axis([0, 16, 0, 16])
        axx=fig.add_subplot(3,nm,ij)
        xmajorLocator   = MultipleLocator(4)
        axx.xaxis.set_major_locator(xmajorLocator) 
        ymajorLocator   = MultipleLocator(4)
        axx.yaxis.set_major_locator(ymajorLocator)
        if ity==2:
            plt.xlabel(r'Cloud Base Height ($km$)', fontdict=font)
        if im==0:
            plt.ylabel(r'Cloud Top Height ($km$)', fontdict=font)
        ij=ij+1
figtitle = r"Frequency of all cloud cells ($10^{-2}$ %)"
fig.text(0.5, 0.95, figtitle,
    horizontalalignment='center',
    fontproperties=FontProperties(size=12))
plt.subplots_adjust(left = 0.06, wspace = 0.3, hspace = 0.25, \
        bottom = 0.15, right=0.92, top = 0.90)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
cax=fig.add_axes([0.95, 0.2, 0.02, 0.65])
fig.colorbar(ax[0,0],cax,orientation='vertical',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
cax=fig.add_axes([0.15, 0.03, 0.65, 0.03])
fig.colorbar(ax[1,1],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
plt.savefig(dirpic+"CLS_CloudCellsTopBase_fortran_color.png",dpi=300)          
#plt.show()
plt.close()
#
#plot1(raindu,mclddu,ndt,nday,xdat,zdat,dirpic,addstr,xtime,xdate)
monstrs=['April','May','June','July','Aug.','Sept.']
lev10=[0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4]
lev20=[5,10,20,30,40]
lev1=[-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5]
lev2=[-0.04,-0.02,-0.01,-0.001,0.001,0.01,0.02,0.04]
lev2=[-6,-4,-2,2,4,6]
hatch=['/////','////','///','//',None,'..','...','....','.....']
hthcol=['r','r','r','r','w','g','g','g','g']
fig,ax=plt.subplots(nrows=3,ncols=nm,figsize=(16,8))
ij=1
for ity in range(0,3):
    qddu=cls_qddu[ity]
    qddu0=cls_qddu[0]
    for im in range(0,nm):        
        if ity==0:
            strss='Averaged '
            adat=qddu[im,:,:,0]
            adat1=qddu[im,:,:,1]*10000
        elif ity==1:
            strss='Strong '
            adat=qddu[im,:,:,0]-qddu0[im,:,:,0]
            adat1=qddu[im,:,:,1]*10000-qddu0[im,:,:,1]*10000
        elif ity==2:
            strss='Weak '
            adat=qddu[im,:,:,0]-qddu0[im,:,:,0]
            adat1=qddu[im,:,:,1]*10000-qddu0[im,:,:,1]*10000
        nx=len(xtime)
        xdat=range(0,nx)
        nz=len(Z)
        zdat=Z
        tdt=6
        dt=15
        ####
        #monstrs=monstrs[im] #'Mon'+'%2.2i'%(im+4)
        #adat=qddu[im,:,:,0]
        dat=utc2ltc2(km,ndt,adat,tdt,dt)      #utc2ltc(nday,ndt,cdat,tdt,dt)
        plt.subplot(3,nm,ij)
        if ity==0:
            ax[ity,im]=plt.contourf(xdat,zdat,dat,cmap='plasma',levels=lev10,extend='both')
        else:
            ax[ity,im]=plt.contourf(xdat,zdat,dat,cmap='PiYG',levels=lev1,extend='both')
        marknm=abstr[ij-1]+strss+monstrs[im] #'(a) DCC cloud water content'
        plt.title(marknm,fontsize=12)
        #plt.xlabel(r'LST', fontdict=font)
        if ity==0:
            axbar0= ax[ity,im]
        else:
            axbar1= ax[ity,im] 
        #
        dat=utc2ltc2(km,ndt,adat1,tdt,dt)      #utc2ltc(nday,ndt,cdat,tdt,dt)
        if ity==0:
            ax[ity,im]=plt.contour(xdat,zdat,dat,colors='w',
                linewidths=1.2,levels=lev20 )
            plt.clabel(ax[ity,im],inline=1,fmt='%d',fontsize=12)
        else:            
            ax[ity,im]=plt.contour(xdat,zdat,dat,colors='k',
                linewidths=1.2,levels=lev2 )
            plt.clabel(ax[ity,im],inline=1,fmt='%d',fontsize=12)
            '''
            ax[ity,im]=plt.contourf(xdat,zdat,dat,hatches=hatch,
                colors='none',levels=lev2,extend='both', alpha=0.1)        
            axbar3=ax[ity,im]
            '''
        #
        axx=fig.add_subplot(3,nm,ij)
        plt.axis([0,ndt,0,16])
        axx.set_xticks(range(0,ndt,12))  
        xticklabels = [xtime[nn] for nn in range(0,ndt,12)] 
        axx.set_xticklabels(xticklabels, size=12,rotation=45)
        #plt.xlabel(r'LST', fontdict=font)  
        if ity==2:
            plt.xlabel(r'LST', fontdict=font)
        if im==0:
            plt.ylabel(r'Height ($km$)', fontdict=font)
        ij=ij+1
figtitle = r"Cloud water content and frequency($10^{-2}$%) for DCC"
fig.text(0.5, 0.95, figtitle,
    horizontalalignment='center',
    fontproperties=FontProperties(size=12))
plt.subplots_adjust(left = 0.06, wspace = 0.3, hspace = 0.35, \
        bottom = 0.15, right=0.92, top = 0.90)
cax=fig.add_axes([0.95, 0.2, 0.02, 0.65])
fig.colorbar(axbar0,cax,orientation='vertical',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
cax=fig.add_axes([0.2, 0.03, 0.6, 0.03])
fig.colorbar(axbar1,cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
#cax=fig.add_axes([0.5, 0.03, 0.45, 0.03])
#fig.colorbar(axbar3,cax,orientation='horizontal',extend='both', # 'horizontal'
#    extendfrac='auto',  spacing='uniform')
plt.savefig(dirpic+"CLS_dcc_frq+cwc_du.png",dpi=300)          
plt.close()
#####
cloudlevs=[5,10,15,20,30,40,50,60,70,80,90,100,110,120,130]
difflevs=[-40,-35,-30,-25,-20,-15,-10,-5,-1,0,1,5,10,15,20,25,30,35,40]
difcols2=["#841859","#A43373","#C4498D","#DA66A3","#EA84B7","#F69FC9",
          "#FFB7D9","#FFCDE6","#FFE0F1","w","w","#D6F2D6",
          "#BDE7BE","#A2DAA3","#84C985","#63B764","#3BA23C","#008B03",
          "#007100","#005600"]
fig,ax=plt.subplots(nrows=3,ncols=nm,figsize=(16,9))
ij=1
xdat=range(nb)
ydat=range(ndp)
for ity in range(0,3):
    pre5dptday=getmonmm(cls_pre5dptday[ity],ndays,nday,nm,nb,ndp)  #pre5dptday=np.zeros(shape=(nday,nb,ndp)
    pre5dptday0=getmonmm(cls_pre5dptday[0],ndays,nday,nm,nb,ndp)
    for im in range(0,nm):        
        if ity==0:
            strss='Averaged '
            adat=pre5dptday[im,:,:]*100            
        elif ity==1:
            strss='Strong '
            adat=pre5dptday[im,:,:]*100-pre5dptday0[im,:,:]*100             
        elif ity==2:
            strss='Weak '
            adat=pre5dptday[im,:,:]*100-pre5dptday0[im,:,:]*100       
        plt.subplot(3,nm,ij)
        #zdat[0,:]=0.0   ## the first level is below surface ground
        if ity==0:
            ax[ity,im]=plt.contourf(ydat,xdat,adat,colors=cloudclors, levels=cloudlevs,extend='both')
        else:
            ax[ity,im]=plt.contourf(ydat,xdat,adat,colors=difcols2, levels=difflevs,extend='both')
        marknm=abstr[ij-1]+strss+monstrs[im]
        plt.title(marknm,fontsize=12)
        axx=fig.add_subplot(3,nm,ij)
        axx=fig.add_subplot(3,nm,ij)
        plt.axis([0, ndp-1, 0, nb-1])
        axx=fig.add_subplot(3,nm,ij)
        plt.axis([0, ndp-1, 0, nb-1])
        axx.set_yticks(range(0,nb,4))  
        yticklabels = [rainstr[nn] for nn in range(0,nb-1,4)] 
        axx.set_yticklabels(yticklabels, size=12,rotation=45)   
        axx.set_xticks(range(0,ndp,3))  
        xticklabels = [dptstr[nn] for nn in range(0,ndp,3)] 
        axx.set_xticklabels(xticklabels, size=12,rotation=45) 
        if ity==2: 
            plt.xlabel(r'Cloud Depth (km)', fontdict=font)
        if im==0:
            plt.ylabel(r'Rainfall Rate (mm $hr^{-1}$)', fontdict=font)
        ij=ij+1
plt.subplots_adjust(left = 0.06, wspace = 0.3, hspace = 0.35, \
        bottom = 0.15, right=0.92, top = 0.90)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
cax=fig.add_axes([0.95, 0.2, 0.02, 0.65])
fig.colorbar(ax[0,0],cax,orientation='vertical',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
cax=fig.add_axes([0.15, 0.03, 0.65, 0.03])
fig.colorbar(ax[1,1],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
plt.savefig(dirpic+"CLD_cld2dpt_fortran_color_.png",dpi=300)          
#plt.show()
plt.close()
#####
fig,ax=plt.subplots(nrows=3,ncols=nm,figsize=(16,9))
ij=1
xdat=range(nb)
ydat=range(ndp)
for ity in range(0,3):
    pre5dptday=getmonmm(cls_pre5dccday[ity],ndays,nday,nm,nb,ndp)  #pre5dptday=np.zeros(shape=(nday,nb,ndp)
    pre5dptday0=getmonmm(cls_pre5dccday[0],ndays,nday,nm,nb,ndp)
    for im in range(0,nm):        
        if ity==0:
            strss='Averaged '
            adat=pre5dptday[im,:,:]*100            
        elif ity==1:
            strss='Strong '
            adat=pre5dptday[im,:,:]*100-pre5dptday0[im,:,:]*100             
        elif ity==2:
            strss='Weak '
            adat=pre5dptday[im,:,:]*100-pre5dptday0[im,:,:]*100       
        plt.subplot(3,nm,ij)
        #zdat[0,:]=0.0   ## the first level is below surface ground
        if ity==0:
            ax[ity,im]=plt.contourf(ydat,xdat,adat,colors=cloudclors, levels=cloudlevs,extend='both')
        else:
            ax[ity,im]=plt.contourf(ydat,xdat,adat,colors=difcols2, levels=difflevs,extend='both')
        marknm=abstr[ij-1]+strss+monstrs[im]
        plt.title(marknm,fontsize=12)
        axx=fig.add_subplot(3,nm,ij)
        axx=fig.add_subplot(3,nm,ij)
        plt.axis([0, ndp-1, 0, nb-1])
        axx=fig.add_subplot(3,nm,ij)
        plt.axis([0, ndp-1, 0, nb-1])
        axx.set_yticks(range(0,nb,4))  
        yticklabels = [rainstr[nn] for nn in range(0,nb-1,4)] 
        axx.set_yticklabels(yticklabels, size=12,rotation=45)   
        axx.set_xticks(range(0,ndp,3))  
        xticklabels = [dptstr[nn] for nn in range(0,ndp,3)] 
        axx.set_xticklabels(xticklabels, size=12,rotation=45) 
        if ity==2: 
            plt.xlabel(r'Cloud Depth (km)', fontdict=font)
        if im==0:
            plt.ylabel(r'Rainfall Rate (mm $hr^{-1}$)', fontdict=font)
        ij=ij+1
plt.subplots_adjust(left = 0.06, wspace = 0.3, hspace = 0.35, \
        bottom = 0.15, right=0.92, top = 0.90)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
cax=fig.add_axes([0.95, 0.2, 0.02, 0.65])
fig.colorbar(ax[0,0],cax,orientation='vertical',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
cax=fig.add_axes([0.15, 0.03, 0.65, 0.03])
fig.colorbar(ax[1,1],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
plt.savefig(dirpic+"CLD_dcc2dpt_fortran_color_.png",dpi=300)          
#plt.show()
plt.close()
################
lev2=[-0.5,-0.4,-0.3,-0.2,-0.1,-0.05,0,0.05,0.1,0.2,0.3,0.4,0.5]
lev1=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4]
difcols3=["#841859","#B33D7F","#D964A1","#EF8EBE","#FFB3D6","#FFD3EA",
          "w","w","#C5EBC5","#9ED79E","#70BE71","#37A039",
          "#007D00","#005600"]
difcols3=["#005600","#007D00", "#37A039","#70BE71","#9ED79E","#C5EBC5",
          "w","w","#FFD3EA","#FFB3D6","#EF8EBE","#D964A1","#B33D7F","#841859"]
fig,ax=plt.subplots(nrows=3,ncols=1,figsize=(12,12))
ij=1
for ity in range(0,3):
    qdday=cls_qdday[ity]
    qdday0=cls_qdday[0]
    if ity==0:
        strss='Averaged '
        adat=qdday[:,:,0]           
    elif ity==1:
        strss='Strong '
        adat=qdday[:,:,0]-qdday0[:,:,0]           
    elif ity==2:
        strss='Weak '
        adat=qdday[:,:,0]-qdday0[:,:,0]
    xdat=range(nday)
    zdat=Z
    nz=len(Z)
    plt.subplot(3,1,ij)
    if ity==0:
        ax[ity]=plt.contourf(xdat,zdat,adat,cmap='viridis', levels=lev1,extend='both')
    else:
        ax[ity]=plt.contourf(xdat,zdat,adat,colors=difcols3, levels=lev2,extend='both')
    marknm=abstr[ij-1]+strss+' DCC cloud water content'
    plt.title(marknm,fontsize=12)
    #plt.colorbar()
    axx=fig.add_subplot(3,1,ij)
    plt.axis([0,nday,0,16])
    axx.set_xticks(range(0,nday,15))  
    xticklabels = [xdate[nn] for nn in range(0,nday,15)] 
    axx.set_xticklabels(xticklabels, size=12,rotation=45)   
    ymajorLocator   = MultipleLocator(4)
    axx.yaxis.set_major_locator(ymajorLocator)
    #plt.xlabel(r'Date', fontdict=font)
    plt.ylabel(r'Height (km)', fontdict=font)
    if ij==3:
        plt.xlabel(r'Date', fontdict=font)
    ij=ij+1
plt.subplots_adjust(left = 0.06, wspace = 0.3, hspace = 0.35, \
        bottom = 0.15, right=0.95, top = 0.90)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
cax=fig.add_axes([0.1, 0.03, 0.4, 0.03])
fig.colorbar(ax[0],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
cax=fig.add_axes([0.55, 0.03, 0.4, 0.03])
fig.colorbar(ax[1],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
#plt.ylabel(r'Time', fontdict=font)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
plt.savefig(dirpic+"CLS_time_evo_dcc_tcwc.png",dpi=300)          
#plt.show()
plt.close()
#####
lev2=[-10,-8,-6,-4,-2,-1,-0.5,0,0.5,1,2,4,6,8,10]
lev1=[0,2,4,6,8,10,12,14,16,18,20,22,24]
difcol4=["#005600","#008400","#4FAC50","#8ACC8B","#BBE6BB","#E4F6E4",
         "w","w","#FFEBF5","#FFCBE5","#F8A3CC","#E274AC","#BB4386","#841859"]
fig,ax=plt.subplots(nrows=3,ncols=1,figsize=(12,12))
ij=1
for ity in range(0,3):
    qdday=cls_qdday[ity]
    qdday0=cls_qdday[0]
    if ity==0:
        strss='Averaged '
        adat=qdday[:,:,1]*10000           
    elif ity==1:
        strss='Strong '
        adat=qdday[:,:,1]*10000-qdday0[:,:,1]*10000           
    elif ity==2:
        strss='Weak '
        adat=qdday[:,:,1]*10000-qdday0[:,:,1]*10000
    xdat=range(nday)
    zdat=Z
    nz=len(Z)
    plt.subplot(3,1,ij)
    if ity==0:
        ax[ity]=plt.contourf(xdat,zdat,adat,cmap='plasma', levels=lev1,extend='both')
    else:
        ax[ity]=plt.contourf(xdat,zdat,adat,colors=difcol4, levels=lev2,extend='both')
    marknm=abstr[ij-1]+strss+' DCC Frequency ($10^{-2}$%)'
    plt.title(marknm,fontsize=12)
    #plt.colorbar()
    axx=fig.add_subplot(3,1,ij)
    plt.axis([0,nday,0,16])
    axx.set_xticks(range(0,nday,15))  
    xticklabels = [xdate[nn] for nn in range(0,nday,15)] 
    axx.set_xticklabels(xticklabels, size=12,rotation=45)   
    ymajorLocator   = MultipleLocator(4)
    axx.yaxis.set_major_locator(ymajorLocator)
    #plt.xlabel(r'Date', fontdict=font)
    plt.ylabel(r'Height (km)', fontdict=font)
    if ij==3:
        plt.xlabel(r'Date', fontdict=font)
    ij=ij+1
plt.subplots_adjust(left = 0.06, wspace = 0.3, hspace = 0.35, \
        bottom = 0.15, right=0.95, top = 0.90)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
cax=fig.add_axes([0.1, 0.03, 0.4, 0.03])
fig.colorbar(ax[0],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
cax=fig.add_axes([0.55, 0.03, 0.4, 0.03])
fig.colorbar(ax[1],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
#plt.ylabel(r'Time', fontdict=font)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
plt.savefig(dirpic+"CLS_time_evo_dcc_freq.png",dpi=300)          
#plt.show()
plt.close()
##############
lev2=[-0.3,-0.25,-0.2,-0.15,-0.1,-0.05,-0.01,0,0.01,0.05,0.1,0.15,0.2,0.25,0.3]
lev1=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
difcol4=["#005600","#008400","#4FAC50","#8ACC8B","#BBE6BB","#E4F6E4",
         "w","w","#FFEBF5","#FFCBE5","#F8A3CC","#E274AC","#BB4386","#841859"]
fig,ax=plt.subplots(nrows=3,ncols=1,figsize=(12,12))
ij=1
zdat=range(ndt)
for ity in range(0,3):
    qdday=cls_raindu[ity]
    qdday0=cls_raindu[0]
    if ity==0:
        strss='Averaged '
        adat=qdday           
    elif ity==1:
        strss='Strong '
        adat=qdday-qdday0        
    elif ity==2:
        strss='Weak '
        adat=qdday-qdday0
    xdat=range(nday)
    plt.subplot(3,1,ij)
    dat=utc2ltc(nday,ndt,adat,tdt,dt)
    if ity==0:
        ax[ity]=plt.contourf(xdat,zdat,dat,cmap='plasma', levels=lev1,extend='both')
    else:
        ax[ity]=plt.contourf(xdat,zdat,dat,colors=difcol4, levels=lev2,extend='both')
    marknm=abstr[ij-1]+strss+' rainfall ($mm$ $hr^{-1}$)'
    plt.title(marknm,fontsize=12)
    #plt.colorbar()
    axx=fig.add_subplot(3,1,ij)
    plt.axis([0,nday,0,96])
    axx.set_xticks(range(0,nday,15))  
    xticklabels = [xdate[nn] for nn in range(0,nday,15)] 
    axx.set_xticklabels(xticklabels, size=12,rotation=45)
    #plt.xlabel(r'Date', fontdict=font)
    axx.set_yticks(range(0,ndt,12))  
    yticklabels = [xtime[nn] for nn in range(0,ndt,12)] 
    axx.set_yticklabels(yticklabels, size=12,rotation=45)
    plt.ylabel(r'LST', fontdict=font)
    if ij==3:
        plt.xlabel(r'Date', fontdict=font)
    ij=ij+1
plt.subplots_adjust(left = 0.06, wspace = 0.3, hspace = 0.35, \
        bottom = 0.15, right=0.95, top = 0.95)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
cax=fig.add_axes([0.1, 0.03, 0.4, 0.03])
fig.colorbar(ax[0],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
cax=fig.add_axes([0.55, 0.03, 0.4, 0.03])
fig.colorbar(ax[1],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
#plt.ylabel(r'Time', fontdict=font)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
plt.savefig(dirpic+"CLS_du_rain_evo_IND.png",dpi=300)          
#plt.show()
plt.close()
##############
lev2=[-3,-2.5,-2,-1.5,-1,-0.5,-0.1,0,0.1,0.5,1,1.5,2,2.5,3.0]
lev1=[2.0,2.3,2.6,2.9,3.2,3.5,3.8,4.1,4.4,4.7]
cols3=["#EEC8CA","#E7AFB1","#DE9597","#D47A7E",   #
    "#C85E63","#BA4047","#A4242F","#86131F","#69000C"]
difcol4=["#005600","#008400","#4FAC50","#8ACC8B","#BBE6BB","#E4F6E4",
         "w","w","#FFEBF5","#FFCBE5","#F8A3CC","#E274AC","#BB4386","#841859"]
fig,ax=plt.subplots(nrows=3,ncols=1,figsize=(12,12))
ij=1
zdat=range(ndt)
for ity in range(0,3):
    qdday=cls_mclddu[ity]
    qdday0=cls_mclddu[0]
    if ity==0:
        strss='Averaged '
        adat=qdday[:,:,2]
        print 'averaged',adat.mean()         
    elif ity==1:
        strss='Strong '
        adat=(qdday[:,:,2]-qdday0[:,:,2])#/qdday0[:,:,2]
        print 'strong',adat.mean()
    elif ity==2:
        strss='Weak '
        adat=(qdday[:,:,2]-qdday0[:,:,2])#/qdday0[:,:,2]
        print 'weak',adat.mean()
    xdat=range(nday)
    plt.subplot(3,1,ij)
    dat=utc2ltc(nday,ndt,adat,tdt,dt)
    if ity==0:
        ax[ity]=plt.contourf(xdat,zdat,dat,cmap='Reds', levels=lev1,extend='both')
    else:
        ax[ity]=plt.contourf(xdat,zdat,dat,colors=difcol4, levels=lev2,extend='both')
    marknm=abstr[ij-1]+strss+' Max. CWC level (km)'
    plt.title(marknm,fontsize=12)
    #plt.colorbar()
    axx=fig.add_subplot(3,1,ij)
    plt.axis([0,nday,0,96])
    axx.set_xticks(range(0,nday,15))  
    xticklabels = [xdate[nn] for nn in range(0,nday,15)] 
    axx.set_xticklabels(xticklabels, size=12,rotation=45)
    #plt.xlabel(r'Date', fontdict=font)
    axx.set_yticks(range(0,ndt,12))  
    yticklabels = [xtime[nn] for nn in range(0,ndt,12)] 
    axx.set_yticklabels(yticklabels, size=12,rotation=45)
    plt.ylabel(r'LST', fontdict=font)
    if ij==3:
        plt.xlabel(r'Date', fontdict=font)
    ij=ij+1
plt.subplots_adjust(left = 0.06, wspace = 0.3, hspace = 0.35, \
        bottom = 0.15, right=0.95, top = 0.95)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
cax=fig.add_axes([0.1, 0.03, 0.4, 0.03])
fig.colorbar(ax[0],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
cax=fig.add_axes([0.55, 0.03, 0.4, 0.03])
fig.colorbar(ax[1],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
#plt.ylabel(r'Time', fontdict=font)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
plt.savefig(dirpic+"CLS_du_MaxLevel_evo_IND.png",dpi=300)          
#plt.show()
plt.close()
##########################################################
lev2=[-0.5,-0.4,-0.3,-0.2,-0.1,-0.05,-0.01,0,0.01,0.05,0.1,0.2,0.3,0.4,0.5]
lev1=[1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0]
cols3=["#EEC8CA","#E7AFB1","#DE9597","#D47A7E",   #
    "#C85E63","#BA4047","#A4242F","#86131F","#69000C"]
difcol4=["#005600","#008400","#4FAC50","#8ACC8B","#BBE6BB","#E4F6E4",
         "w","w","#FFEBF5","#FFCBE5","#F8A3CC","#E274AC","#BB4386","#841859"]
fig,ax=plt.subplots(nrows=3,ncols=1,figsize=(12,12))
ij=1
zdat=range(ndt)
for ity in range(0,3):
    qdday=cls_mclddu[ity]
    qdday0=cls_mclddu[0]
    if ity==0:
        strss='Averaged '
        adat=qdday[:,:,2]
        print 'averaged',adat.mean()         
    elif ity==1:
        strss='Strong '
        adat=(qdday[:,:,2]-qdday0[:,:,2])#/qdday0[:,:,2]
        print 'strong',adat.mean()
    elif ity==2:
        strss='Weak '
        adat=(qdday[:,:,2]-qdday0[:,:,2])#/qdday0[:,:,2]
        print 'weak',adat.mean()
    xdat=range(nday)
    plt.subplot(3,1,ij)
    dat=utc2ltc(nday,ndt,adat,tdt,dt)
    mon_dat=getmonmean(dat,ndays)
    #nm=len(ndays)
    xdat=range(0,nm)
    if ity==0:
        ax[ity]=plt.contourf(zdat,xdat,mon_dat,cmap='Reds', levels=lev1,extend='both')
    else:
        ax[ity]=plt.contourf(zdat,xdat,mon_dat,colors=difcol4, levels=lev2,extend='both')
    marknm=abstr[ij-1]+strss+' Max. CWC level (km)'
    plt.title(marknm,fontsize=12)
    #plt.colorbar()
    axx=fig.add_subplot(3,1,ij)
    plt.axis([0,96-1,0,nm-1])
    axx.set_yticks(range(0,nm,1))  
    yticklabels = [monstrs[nn] for nn in range(0,nm,1)] 
    axx.set_yticklabels(yticklabels, size=12,rotation=45)
    #plt.xlabel(r'Date', fontdict=font)
    axx.set_xticks(range(0,ndt,12))  
    xticklabels = [xtime[nn] for nn in range(0,ndt,12)] 
    axx.set_xticklabels(xticklabels, size=12,rotation=45)
    plt.ylabel(r'Month', fontdict=font)
    if ij==3:
        plt.xlabel(r'Time', fontdict=font)
    ij=ij+1
plt.subplots_adjust(left = 0.06, wspace = 0.3, hspace = 0.35, \
        bottom = 0.15, right=0.95, top = 0.95)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
cax=fig.add_axes([0.1, 0.03, 0.4, 0.03])
fig.colorbar(ax[0],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
cax=fig.add_axes([0.55, 0.03, 0.4, 0.03])
fig.colorbar(ax[1],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
#plt.ylabel(r'Time', fontdict=font)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
plt.savefig(dirpic+"CLS_Mon_du_MaxLevel_evo_IND.png",dpi=300)          
#plt.show()
plt.close()
##################################
lev2=[-0.12,-0.1,-0.08,-0.06,-0.04,-0.02,-0.01,0,
      0.01,0.02,0.04,0.06,0.08,0.1,0.12]
lev1=[0.0,0.01,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1]
cols3=["#EEC8CA","#E7AFB1","#DE9597","#D47A7E",   #
    "#C85E63","#BA4047","#A4242F","#86131F","#69000C"]
difcol4=["#005600","#008400","#4FAC50","#8ACC8B","#BBE6BB","#E4F6E4",
         "w","w","#FFEBF5","#FFCBE5","#F8A3CC","#E274AC","#BB4386","#841859"]
fig,ax=plt.subplots(nrows=3,ncols=1,figsize=(12,12))
ij=1
zdat=range(ndt)
for ity in range(0,3):
    qdday=cls_raindu[ity]
    qdday0=cls_raindu[0]
    if ity==0:
        strss='Averaged '
        adat=qdday
        print 'averaged',adat.mean()         
    elif ity==1:
        strss='Strong '
        adat=(qdday-qdday0)#/qdday0[:,:,2]
        print 'strong',adat.mean()
    elif ity==2:
        strss='Weak '
        adat=(qdday-qdday0)#/qdday0[:,:,2]
        print 'weak',adat.mean()
    xdat=range(nday)
    plt.subplot(3,1,ij)
    dat=utc2ltc(nday,ndt,adat,tdt,dt)
    mon_dat=getmonmean(dat,ndays)
    #nm=len(ndays)
    xdat=range(0,nm)
    if ity==0:
        ax[ity]=plt.contourf(zdat,xdat,mon_dat,cmap='Reds', levels=lev1,extend='both')
    else:
        ax[ity]=plt.contourf(zdat,xdat,mon_dat,colors=difcol4, levels=lev2,extend='both')
    marknm=abstr[ij-1]+strss+' rainfall (mm $hr^{-1}$)'
    plt.title(marknm,fontsize=12)
    #plt.colorbar()
    axx=fig.add_subplot(3,1,ij)
    plt.axis([0,96-1,0,nm-1])
    axx.set_yticks(range(0,nm,1))  
    yticklabels = [monstrs[nn] for nn in range(0,nm,1)] 
    axx.set_yticklabels(yticklabels, size=12,rotation=45)
    #plt.xlabel(r'Date', fontdict=font)
    axx.set_xticks(range(0,ndt,12))  
    xticklabels = [xtime[nn] for nn in range(0,ndt,12)] 
    axx.set_xticklabels(xticklabels, size=12,rotation=45)
    plt.ylabel(r'Month', fontdict=font)
    if ij==3:
        plt.xlabel(r'Time', fontdict=font)
    ij=ij+1
plt.subplots_adjust(left = 0.06, wspace = 0.3, hspace = 0.35, \
        bottom = 0.15, right=0.95, top = 0.95)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
cax=fig.add_axes([0.1, 0.03, 0.4, 0.03])
fig.colorbar(ax[0],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
cax=fig.add_axes([0.55, 0.03, 0.4, 0.03])
fig.colorbar(ax[1],cax,orientation='horizontal',extend='both', # 'horizontal'
    extendfrac='auto',  spacing='uniform')
#plt.ylabel(r'Time', fontdict=font)
#cax = fig.add_axes([0.2, 0.025, 0.6, 0.02])
plt.savefig(dirpic+"CLS_Mon_du_rain_evo_IND.png",dpi=300)          
#plt.show()
plt.close()
'''
    #
    #qdday[i,k,j]
    plot2(qdday,nday,km,dirpic,addstr,xdate,Z)
    #
    plot3(ftday,nday,km,dirpic,addstr,xdate,Z,cloudlevs,cloudclors,ndays)
    #####
    plot4(pre5dptday,nday,nb,ndp,dirpic,addstr,rainbin,dpbin,rainstr,dptstr,'cld',
      ndays,cloudclors,cloudlevs)
    #
    plot4(pre5dccday,nday,nb,ndp,dirpic,addstr,rainbin,dpbin,rainstr,dptstr,'dcc',
      ndays,cloudclors,cloudlevs)
    #
    #plot5(pre5dptdu,nm,ndt,nb,ndp,dirpic,addstr,rainbin,dpbin,rainstr,dptstr,'dcc')
 
    plot6(dccdu,nm,ndt,dirpic,addstr,xtime,dccfeas) 
    # 
    plot7(qddu,nm,ndt,km,dirpic,addstr,xtime,Z) 
    # 
    #plot8(ftdu,nm,ndt,km,dirpic,addstr,xtime,Z) 
'''

















