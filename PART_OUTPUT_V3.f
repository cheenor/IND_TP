      Program Cloud_Pre
      implicit none
      integer,PARAMETER :: nx=202, km=52, inn=480,kmm=34
      integer,PARAMETER :: itt=365*96, nfl=73
      integer,PARAMETER :: nb=30,ndp=20
      REAL, PARAMETER :: QCC=1.0E-3, qce=1.0-4                ! LOW LIMIT FOR CONVECTION CLOUD (G/KG)
                                                          ! QCE LOW LIMIT FOR CLOUD ENSEMBLE (G/KG)
      real,dimension(nx,km):: qc,qr,qa,qb,qrl,qrs,u,w,th,q,rh 
      real,dimension(km):: te,ps,potf,pote,rho
      !!!!
      real,dimension(nx):: preci,fsh,flh
      !!!
      real z(kmm)
      integer DCB,DCT,IH
      integer ifl,ix,it,n,ixx,l,i,j,k
      integer ik
      real tmprain,tcwc(kmm),ql(kmm),qi(kmm),C(kmm)
      real CM(KMM)
      integer NS,KCB(KMM),KCE(KMM),kb,KE
      integer ib,idp,idcc
      real rainbin(nb),dpbin(ndp)
      real dpmax,dp
      ! 
      real pre5dpt(nb,ndp+1),contpre,contpredcc
      real cw,am,amz
      real dcc(6),qd(kmm,3),pre5dptdcc(nb,ndp+1)
      real FRG,ft(kmm,kmm)
      real mcld(3)
      character casenm*20,fpath*200,fold*20,dirin*200,strs*3
      character dirout*200,addstr*20
      !
      DATA Z/            0.0500000, 0.1643000, 0.3071000, 0.4786000
    &      , 0.6786000, 0.9071000, 1.1640000, 1.4500000, 1.7640001
    &      , 2.1070001, 2.4790001, 2.8789999, 3.3069999, 3.7639999
    &      , 4.2500000, 4.7639999, 5.3070002, 5.8790002, 6.4790001
    &      , 7.1069999, 7.7639999, 8.4499998, 9.1639996, 9.9069996
    &      ,10.6800003,11.4799995,12.3100004,13.1599998,14.0500002
    &      ,14.9600000,15.9099998,16.8799992,17.8799992,18.9099998/
      DATA rainbin/0.0, 0.1,  0.2, 0.3, 0.4,
    &          0.6, 0.8,  1.0, 1.2, 1.4,
    &          1.6, 1.8,  2.0, 2.4, 2.8,
    &          3.2, 3.6,  4.0, 4.6, 5.2,
    &          5.8, 6.4,  7.0, 7.8, 8.6,
    &          9.4, 10.2,  11, 12, 13/
      DATA dpbin/0.5,  1.0, 1.5, 2.0, 2.5, 3.0, 3.5,
    &        4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0,7.5,
    &        8.0, 8.5, 9.0, 9.5,10/
      ! to filt DCC 
      DCB=10 ! ~0.6
      DCT=19 ! 6.5km
      !
      casenm='casename'
      fold='runfold'
      addstr='norm'
      dirout='/chenjh2/Work/INDMSN_TP/Data/'  
      if(casenm(1:3)=='MLY')then
        dirin='/chenjh2/Work/INDMSN_TP/'//casenm(1:4)// &
    &   '/'//trim(fold)
      else
        dirin='/chenjh2/Work/INDMSN_TP/'//casenm(1:3)// &
    &   '/'//trim(fold)
      endif
      !
      open(81,file=trim(dirin)//'postdata/'//'preci_'//trim(casenm),convert='big_endian', &
    &   form='UNFORMATTED',status='OLD')
      !call getbin(rainbin,dpbin,nb,ndp)
      it=0
      do ifl=1,nfl
        IH=80
        fpath=trim(dirin)//'/'//trim(casenm)
        write(strs,'(I3.3)')ifl   
        open(81,file=trim(dirin)//trim(strs),form='UNFORMATTED',status='OLD',convert='big_endian')
        do n=1,inn
          it=it+1
          read(IH) qc,qr 
          read(IH) qa,qb 
          read(IH) th,q
          read(IH) rh,te,ps
          read(IH) u,w
          read(IH) 
          read(IH) rho,potf,pote
          read(IH) qrl, qrs
          !
          read(IH) preci 
          read(IH) fsh,flh
          ! end of reading data 
          pre5dpt=0.0
          contpre=0.0
          pre5dptdcc=0.0
          contpredcc=0.0
          dcc=0.0
          qd=0.0 
          FRG=1.0/(nx-2)
          ft=0.0
          tmprain=0.0
          mcld=0.0
          do ixx=2,nx-1
            ix=ixx-1
            tmprain=tmprain+preci(ixx)*1.e3*3.6e3*FRG
            call getib(preci(ixx)*1.e3*3.6e3,rainbin,nb,ib)
            do ik=1,kmm            
            ql(ik)=qc(ixx,ik)*1000 +qr(ixx,ik)*1000
            qi(ik)=qa(ixx,ik)*1000+qb(ixx,ik)*1000
            tcwc(ik)=ql(ik)+qi(ik)
            enddo
            DO iK = 1,KMM
            C(IK) = tcwc(ik)
            IF (C(IK).LT.QCC) C(IK) = 0.
            ENDDO
            CALL INFCLD(C,KMM,KCB,KCE,CM,NS)
            DO l = 1,NS ! NS: LAYERS OF CLOUDS
            KB = KCB(l)
            KE = KCE(l)
            FT(KB,KE) = FT(KB,KE) + FRG !CLOUD COVER OF EVERY LAYER
            ENDDO
            call get_cld_feas(rho,km,z,kmm,ql,qi,2,kmm-1,cw,am,amz)
            mcld(1)=mcld(1)+cw*FRG
            mcld(2)=mcld(2)+am*FRG
            mcld(3)=mcld(3)+amz*FRG
            dpmax=-99.0
            idcc=0
            do l=1,ns
            KB = KCB(l)
            KE = KCE(l)
            dp=z(Ke)-z(kb)
            if (dp>dpmax)then
              dpmax=dp
            endif
            !#  deep CONVECTION
            IF(KE.GE. DCT .AND. KB .LE. DCB .and. KB>1) THEN
              idcc=1
              call get_cld_feas(rho,km,z,kmm,ql,qi,kb,ke,cw,am,amz)
              dcc(1)=dp
              dcc(2)=cw
              dcc(3)=am
              dcc(4)=amz
              dcc(5)=preci(ixx)*1.e3*3.6e3
              dcc(6)=dcc(6)+1.0
              !
              DO K = KB,KE
                QD(K,1) = QD(K,1) + C(K) ! TOTAL WATER CONTENT
                QD(K,2) = QD(K,2) + FRG    ! C(K)/QZD  ! cloud water/mean cloud water
                qD(K,3)   = qD(K,3)   + 1.
              ENDDO              
            ENDIF
          enddo
          call getidp(dpmax,dpbin,ndp,idp)
          if (idcc>0)then
            pre5dptdcc(ib,idp)=pre5dptdcc(ib,idp)+1.0
            contpredcc=contpredcc+1.0
          endif
          pre5dpt(ib,idp)=pre5dpt(ib,idp)+1.0
          if (preci(ixx)*1.e3*3.6e3>0.0001)then
            contpre=contpre+1.0
          endif
        enddo  ! loop ixx
        !Output file
        write(strs,"(I3.3)")it
        fpath=trim(dirout)//trim(casenm)//'Cloud_Pre_F90_output_'//strs//trim(addstr)//'.txt'
        open(90,file=trim(fpath))
        !#
      
        do i=1,nb
          do j=1,ndp+1
            if (contpre>0)then         
            pre5dpt(ib,idp)=pre5dpt(ib,idp)/contpre
            endif
            if (contpredcc>0)then         
            pre5dptdcc(ib,idp)=pre5dptdcc(ib,idp)/contpredcc
            endif
          enddo
          write(90,99) (pre5dpt(ib,idp),idp=1,ndp+1)
          write(90,99) (pre5dptdcc(ib,idp),idp=1,ndp+1) 
        enddo
        !
        if(dcc(6)>0)then
          do i=1,5
            dcc(i)=dcc(i)/dcc(6)
          enddo
        endif
        write(90,"(5e8.4)")(dcc(i),i=1,5)
        do i=1,kmm
          if (qD(i,3) >0)then
            do j=1,2
              QD(i,j) = QD(i,j)/qd(i,3)
            enddo
          endif
          write(90,"(2e8.4)") (qd(i,j),j=1,2)        
        enddo
        do i=1,kmm
          write(90,"(34e8.4)") (ft(i,j),j=1,34)        
        enddo
        write(90,"(4e8.4)")tmprain,(mcld(j),j=1,3)
        close(90)     
        enddo ! loop inn
        close(80)  
      enddo ! loop nfl
      close(81)
99    format("21e8.4")
      end Program

      SUBROUTINE INFCLD(C,NL,KB,KE,CM,NA) !KB BASE; KE TOP, NA: LAYERS OF CLOUDS
!C     -----------------------------------
!C     -----------------------------------
!C
!C     FIND INFORMATION ABOUT ADJACENT CLOUD LAYERS
!C
      IMPLICIT NONE
!C
      INTEGER NL,KB(*),KE(*),NA,K1,K2,K
      REAL C(NL),CM(*),AA
!C
      NA = 0
      IF (C(1).GT.0.) THEN
          K1 = 1
          K2 = 1
          AA = C(1)
      ELSE
          AA = 0.
      ENDIF
      DO K = 2,NL
         IF (C(K-1).LE.0..AND.C(K).GT.0.) THEN
             K1 = K
             K2 = K
             AA = MAX(AA,C(K))
         ELSEIF (C(K-1).GT.0..AND.C(K).GT.0.) THEN
             K2 = K
             AA = MAX(AA,C(K))
         ELSEIF (C(K-1).GT.0..AND.C(K).LE.0.) THEN
             NA = NA + 1
             KB(NA) = K1
             KE(NA) = K2
             CM(NA) = AA
             AA = 0.
         ENDIF
      ENDDO
      IF (C(NL).GT.0.) THEN  !TOP
          NA = NA + 1
          KB(NA) = K1
          KE(NA) = K2
          CM(NA) = AA
      ENDIF
      RETURN
      END SUBROUTINE
!SUBROUTINE getbin(rainbin,dpbin,nb,ndp)
!  implicit none
!  integer nb,ndp
!  real rainbin(nb),dpbin(ndp)
!  DATA rainbin/0.0, 0.1,  0.2, 0.3, 0.4, & 
!    &          0.6, 0.8,  1.0, 1.2, 1.4, & 
!    &          1.6, 1.8,  2.0, 2.4, 2.8, & 
!    &          3.2, 3.6,  4.0, 4.6, 5.2, & 
!    &          5.8, 6.4,  7.0, 7.8, 8.6, & 
!    &          9.4, 10.2,  11, 12, 13/
!  DATA dpbin/0.5,  1.0, 1.5, 2.0, 2.5, 3.0, 3.5, & 
!   &        4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0,7.5, & 
!    &        8.0, 8.5, 9.0, 9.5,10/
!  RETURN
!end SUBROUTINE
      SUBROUTINE getib(a,rainbin,nb,ib)
      implicit none
      integer nb,ib
      real rainbin(nb)
      real rr,a
      integer i
      ib=-1
      if (a<=0.0001)then
      rr=0
      else
      rr=a
      endif
      if(rr>rainbin(nb))then
      ib=nb+1
      else
      do i=2,nb
        if (rr>rainbin(i-1) .and.rr<=rainbin(i) ) then
          ib=i-1
          exit
        endif
      enddo
      endif
      RETURN
      end SUBROUTINE
      SUBROUTINE getidp(h,dpbin,ndp,idp)
      implicit none
      integer ndp,idp
      real dpbin(ndp)
      real h
      integer i
      idp=-1
      if(h<=dpbin(1))then
      idp=1
      elseif(h>dpbin(ndp))then
      idp=ndp+1
      else
      do i=2,ndp
        if (h>dpbin(i-1) .and.h<=dpbin(i) ) then
          idp=i
          exit
        endif
      enddo
      endif
      RETURN
      end SUBROUTINE
      SUBROUTINE get_cld_feas(rho,km,z,kmm,ql,qi,kb,ke,cw,am,amz) 
      implicit none
      integer km,kmm,ke,kb
      real rho(km)
      real,dimension(kmm) :: z,ql,qi
      integer i,j,k
      real dz
      real ca,cw,am,amz

      am=-99
      ca=0.0
      cw=0.0
      do i =kb,ke
      if ( (ql(i)+qi(i)) >am )then
        am= ql(i)+qi(i)
        amz=z(i)
      endif
      dz=(z(kb+1)-z(kb-1))*0.5
      ca=ca+dz*1.*rho(i)
      cw=cw+ca*(ql(i)+qi(i))
      enddo
      if(ca>0)then
      cw=cw/ca
      endif
      RETURN
      end SUBROUTINE
!C     -------------------
!C     -------------------
      FUNCTION LENCHR(CH)
!C     -------------------
!C     -------------------
!C
!C     RETURNS POSITION OF LAST NON-BLANK CHARACTER IN CH,
!C     OR 1 IF CH IS ALL BLANKS.
!C
      CHARACTER*(*) CH
      DO 10 I=LEN(CH),1,-1
         IF (CH(I:I).NE.' ') THEN
            LENCHR = I
            RETURN
         ENDIF
   10 CONTINUE
      LENCHR = 1
      RETURN
      END FUNCTION LENCHR

 


