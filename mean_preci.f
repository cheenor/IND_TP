      PARAMETER (im=1202, km=52, itt=2880, ii=121, ifi=6)
      dimension preci(im),fsh(im),flh(im)
      dimension smp(itt),ssh(itt),slh(itt)
      dimension tmp(ii),tsh(ii),tlh(ii)
      character casenm*20,path*100,fold*20
      casenm='casename'
      fold='runfold'
      if(casenm(1:3)=='MLY')then
        path='/nuist/p/work/chenjh/CRM/SurfaceHeatFlux/'//casenm(1:4)//
     +   '/'//trim(fold)//'/postdata/'
      else
        path='/nuist/p/work/chenjh/CRM/SurfaceHeatFlux/'//casenm(1:3)//
     +   '/'//trim(fold)//'/postdata/'
      endif
!      path ='/nuist/p/work/chenjh/CRM/SurfaceHeatFlux/ETP/'//trim(fold)
!     + //'/postdata/'
      open(81,file=
     *trim(path)//'preci_'//trim(casenm)
     * ,form='UNFORMATTED',status='OLD') 
      open(40,file=
c    *'/mnt/raid51/wuxq/crm_toga/toga30_dat/rain_tgn2d0',
     *trim(path)//'rain_'//trim(casenm),
     1 form='unformatted')
      open(50,file=
c    *'/mnt/raid51/wuxq/crm_toga/toga30_dat/sflux_tgn2d6',
     *trim(path)//'sflux_'//trim(casenm),
     1 form='unformatted')
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      open(41,file=
c    *'/mnt/raid51/wuxq/crm_toga/toga30_dat/rain_tgn2d0',
     *trim(path)//'rain_'//trim(casenm)//'.txt')
      open(51,file=
c    *'/mnt/raid51/wuxq/crm_toga/toga30_dat/sflux_tgn2d6',
     *trim(path)//'sflux_'//trim(casenm)//'.txt')
c    
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      it=0
      do 999 jf=1,ifi
      IH=81
      inn=480
      do 100 in=1,inn
      it=it+1
      read(IH,end=200) preci 
      read(IH,end=200) fsh,flh 
      smp(it)=0.
      ssh(it)=0.
      slh(it)=0.
      do 30 i=2,im-1
      smp(it)=smp(it)+preci(i)*1.e3*3.6e3/float(im-2) 
      ssh(it)=ssh(it)+fsh(i)/float(im-2) 
      slh(it)=slh(it)+flh(i)/float(im-2) 
  30  continue
 100  continue   
 999  continue   
 200  continue   
      atsh=0.
      atlh=0.
      do 50 mt=1,ii
      n1=(mt-1)*24-11
      n2=(mt-1)*24+12
      if(mt.eq.1) then
      n1=1
      n2=12
      endif
      if(mt.eq.ii) then
      n1=itt-11
      n2=itt
      endif
      tmp(mt)=0.
      tsh(mt)=0.
      tlh(mt)=0.
      do 11 n=n1,n2 
      tmp(mt)=tmp(mt)+smp(n)/float(n2-n1+1)
      tsh(mt)=tsh(mt)+ssh(n)/float(n2-n1+1)
      tlh(mt)=tlh(mt)+slh(n)/float(n2-n1+1)
  11  continue
      atsh=atsh+tsh(mt)/float(ii)
      atlh=atlh+tlh(mt)/float(ii)
c     print*,tsh(mt),tlh(mt)
  50  continue
      write(40) tmp
      write(50) tsh,tlh
      write(41,*)tmp
      write(51,*)tsh,tlh
c     print*,atsh,atlh
c  units:                
c     rain rate (tmp  mm/hour)
      stop
      end

