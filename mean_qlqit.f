      PARAMETER (im=1202, km=52, inn=480, itt=2880, ii=121, ifi=6)
      parameter (imm=1200,kmm=34)
      dimension qc(im,km),qr(im,km),qa(im,km),qb(im,km),rho(km)
      dimension qrl(im,km),qrs(im,km)
      dimension u(im,km),w(im,km),th(im,km),q(im,km),rh(im,km)
!      dimension te(im,km)
      dimension te(km),ps(km),potf(km),pote(km)
c
      dimension smql(itt,imm,kmm),smqi(itt,imm,kmm),tc(itt,imm,kmm)
      dimension den(itt,kmm),tmden(ii,kmm),smtc(itt,imm,kmm)
      dimension tmql(ii,imm,kmm),tmqi(ii,imm,kmm),tmtc(ii,imm,kmm)
      character*100 chenm, path ! case name ,must be recorded 
      character casenm*20,fold*20
      casenm='casename'
      fold='runfold'
      if(casenm(1:3)=='MLY')then
        path='/nuist/p/work/chenjh/CRM/SurfaceHeatFlux/'//casenm(1:4)//
     +   '/'//trim(fold)
      else
        path='/nuist/p/work/chenjh/CRM/SurfaceHeatFlux/'//casenm(1:3)//
     +   '/'//trim(fold)
      endif
      chenm=trim(path)//'/'//trim(casenm)    !'whereisthe_data_tgn2d1_(1-6)'      
       open(81,file=trim(chenm)//'_1'
     * ,form='UNFORMATTED',status='OLD',convert='big_endian') 
      open(82,file=trim(chenm)//'_2'
     *,form='unformatted',status='old',convert='big_endian') 
      open(83,file=trim(chenm)//'_3'
     *,form='unformatted',status='old',convert='big_endian') 
      open(84,file=trim(chenm)//'_4'
     *,form='unformatted',status='old',convert='big_endian') 
      open(85,file=trim(chenm)//'_5'
     *,form='unformatted',status='old',convert='big_endian') 
      open(86,file=trim(chenm)//'_6'
     *,form='unformatted',status='old',convert='big_endian') 
c      open(40,file=trim(chenm)//'_All'
c     * ,form='unformatted')
      open(45,file=trim(chenm)//'_qlqit',form='unformatted')
c      open(50,file=trim(chenm)//'_qlqit.txt')
      open(50,file=trim(chenm)//'ql_2880x1200x52.binary',form='binary')
      open(51,file=trim(chenm)//'qi_2880x1200x52.binary',form='binary')
      open(52,file=trim(chenm)//'tc_2880x1200x52.binary',form='binary')
      open(53,file=trim(chenm)//'den_2880x52.binary',form='binary')
c      open(51,file=trim(chenm)//'_omgqrlqrs.txt')
c      open(51,file=trim(chenm)//'_rho.txt')
cc      open(52,file=trim(chenm)//'_Raw_qcqaqbqr.txt')
c      open(53,file=trim(chenm)//'_Raw_tqrhuvw.txt')
      it=0
      do 999 if=1,ifi
      IH=80+if
      do 100 in=1,inn
      it=it+1
      read(IH) qc,qr 
      read(IH) qa,qb 
      read(IH) th,q
      read(IH) rh,te,ps
      read(IH) u,w
      read(IH) 
      read(IH) rho,potf,pote
      read(IH) qrl, qrs
C
C
      do 40 k=2,kmm+1
      ij=0
      den(it,k)=rho(k)
      do 30 i=2,im-1
      ij=ij+1
      smql(it,ij,k)=qc(i,k)*1000.+ qr(i,k)*1000.
      smqi(it,ij,k)=qa(i,k)*1000.+qb(i,k)*1000.
      tmptc=th(i,k)*te(k)/potf(k)/(1.+pote(k))-273.16 ! convert theta to temp in C degree
      smtc(it,ij,k)=tmptc
!      write(50,99)smql(it,ij,k),smqi(it,ij,k),tmptc,
!      write(51,99)smql(it,i,k),smqi(it,i,k),w(i,k),qrs(i,k),qrl(i,k)
  30  continue
      write(50,99)den(it,k),smql(it,:,k),smqi(it,:,k),smtc(it,:,k)
  40  continue
! 
      do I=2,IM-1    !1,kmm
      do K=2,KMM+1
!     ij=ij+1
       smqltmp=qc(i,k)*1000.+ qr(i,k)*1000.
       smqitmp=qa(i,k)*1000.+qb(i,k)*1000.
!      tmptc=th(i,k)*te(k)/potf(k)/(1.+pote(k))-273.16 ! convert theta to temp in C degree
!      smtc(it,ij,k)=tmptc
!      write(50,99)smql(it,ij,k),smqi(it,ij,k),tmptc,
c       write(51,99)smqltmp,smqitmp,w(i,k),qrs(i,k),qrl(i,k)
      enddo
      enddo
!    continue
!     write(50,99)den(it,k),smql(it,:,k),smqi(it,:,k),smtc(it,:,k)
! continue
!
 100  continue   
 999  continue  
 
      do 300 i=1,imm
      do 200 k=1,kmm
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
      tmql(mt,i,k)=0.
      tmqi(mt,i,k)=0.
      tmtc(mt,i,k)=0.
      tmden(mt,k)=0.0
      do 11 n=n1,n2 
      tmql(mt,i,k)=tmql(mt,i,k)+smql(n,i,k)/float(n2-n1+1)
      tmqi(mt,i,k)=tmqi(mt,i,k)+smqi(n,i,k)/float(n2-n1+1)
      tmtc(mt,i,k)=tmtc(mt,i,k)+smtc(n,i,k)/float(n2-n1+1)
      tmden(mt,k)=tmden(mt,k)+den(n,k)
  11  continue
  50  continue
 200  continue
300   continue
      write(45) tmql
      write(45) tmqi
      write(45) tmtc
      write(45) tmden
!      print*,'tmql(1,1,1)= , tmqi(1,1,1)= ',tmt(1,1,1),tmq(1,1,1)
!      print*,'tmtc(80,5,3)=  ',tmtc(80,5,3)
c
!      do mt=1,ii
!      write(50,99) tmql(mt,:),tmqi(mt,:),tmtc(mt,:),tmden(mt,:) !,tmqc(mt,:),
!     +tmqr(mt,:),tmqa(mt,:),tmqb(mt,:), tmrh(mt,:),
!     +tmfqv(mt,:),tmftc(mt,:),tmrat(mt,:) 
!      enddo
99    format(8e12.4)
c  units:              
c     horizontal velocity (tmu  m/s)
c     vertical velocity (tmw  m/s)
c     temperature (tmt  K)
c     water vapor mixing ratio (tmq  g/kg)
c     relative humidity (tmrh  %)
c     cloud water mixing ratio (tmqc  g/kg)
c     rain water mixing ratio  (tmqr  g/kg)
c     type A ice water mixing ratio (tmqa  g/kg)
c     type B ice water mixing ratio (tmqb  g/kg)
      stop
      end
