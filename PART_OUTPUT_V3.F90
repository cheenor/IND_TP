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
      real mcld(3),dpdcc,tmprr,mcp,mcpc
      character casenm*20,fpath*200,fold*20,dirin*200,strs*3
      character dirout*200,addstr*20,yearstr*4,strs2*5
      !
      DATA Z/            0.0500000, 0.1643000, 0.3071000, 0.4786000 &
    &      , 0.6786000, 0.9071000, 1.1640000, 1.4500000, 1.7640001 &
    &      , 2.1070001, 2.4790001, 2.8789999, 3.3069999, 3.7639999 &
    &      , 4.2500000, 4.7639999, 5.3070002, 5.8790002, 6.4790001 &
    &      , 7.1069999, 7.7639999, 8.4499998, 9.1639996, 9.9069996 &
    &      ,10.6800003,11.4799995,12.3100004,13.1599998,14.0500002 &
    &      ,14.9600000,15.9099998,16.8799992,17.8799992,18.9099998/
      DATA rainbin/0.0, 0.1,  0.2, 0.3, 0.4, &
    &          0.6, 0.8,  1.0, 1.2, 1.4, &
    &          1.6, 1.8,  2.0, 2.4, 2.8, &
    &          3.2, 3.6,  4.0, 4.6, 5.2, &
    &          5.8, 6.4,  7.0, 7.8, 8.6, &
    &          9.4, 10.2,  11, 12, 13/
      DATA dpbin/0.5,  1.0, 1.5, 2.0, 2.5, 3.0, 3.5, &
    &        4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0,7.5, &
    &        8.0, 8.5, 9.0, 9.5,10/
      ! to filt DCC
      do i=1,nb
        rainbin(i)=rainbin(i)
      enddo
      DCB=10 ! ~1
      DCT=19 ! 7.1km
      !
      yearstr='1994'
      casenm='ETP2D0'
      fold='run'
      addstr='norm'
      dirout='/chenjh2/Work/INDMSN_TP/Data/' 
      dirin='/chenjh2/Work/INDMSN_TP/'//yearstr//'/'//trim(fold)//'/'
      !if(casenm(1:3)=='MLY')then
      !  dirin='/chenjh2/Work/INDMSN_TP/'//casenm(1:4)// &
    !&   '/'//trim(fold)
    !  else
    !    dirin='/chenjh2/Work/INDMSN_TP/'//casenm(1:3)// &
    !&   '/'//trim(fold)
    !  endif
      !
      open(81,file=trim(dirin)//'postdata/'//'preci_'//trim(casenm), &
    &   form='UNFORMATTED',status='OLD')
      !call getbin(rainbin,dpbin,nb,ndp)
      it=0
      do ifl=1,nfl
        IH=80
        fpath=trim(dirin)//trim(casenm)
        write(strs,'(I3.3)')ifl   
        open(80,file=trim(fpath)//'_'//trim(strs),form='UNFORMATTED',status='OLD',convert='big_endian')
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
          read(81) preci 
          read(81) fsh,flh
          ! end of reading data 
          contpre=0.0
          contpredcc=0.0
          dcc=0.0
          qd=0.0 
          FRG=1.0/(nx-2)
          ft=0.0
          tmprain=0.0
          mcld=0.0
          idcc=0
          dpdcc=0.0
          !print*,'it=',it
          do ib=1,nb
            do idp=1,ndp+1
            pre5dpt(ib,idp)=0.0
            pre5dptdcc(ib,idp)=0.0
            enddo 
          enddo
          do i=1,6
            dcc(i)=0.0
          enddo
          do i=1,kmm
            do j=1,3
            qd(i,j)=0.0
            enddo      
          enddo
          do i=1,kmm
          do j=1,kmm
          ft(i,j)=0.0
          enddo        
          enddo
          tmprain=0.0
          do j=1,3
          mcld(j)=0.0
          enddo
          mcp=0
          mcpc=0
          if(pre5dptdcc(1,16)>0)print*,'bf nxloop',pre5dptdcc(1,16)
          do ixx=2,nx-1
            !print*,'ixx0',ixx,pre5dptdcc(1,16)
            ib=-1
            idp=-1
            idcc=0
            ix=ixx-1
            mcp=0.0
            mcpc=0.0
            tmprain=tmprain+preci(ixx)*1.e3*3.6e3*FRG
            !if (preci(ixx)*1.e3*3.6e3>4.0)then
            !  print*,'pre=',preci(ixx)*1.e3*3.6e3,ifl,n
            !endif
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
            
            do l=1,ns
            KB = KCB(l)
            KE = KCE(l)
            dp=z(Ke)-z(kb)
            if (dp>dpmax)then
              dpmax=dp
            endif
            mcp=mcp+dp
            mcpc=mcpc+1.0
            tmprr=preci(ixx)*1.e3*3.6e3
            !#  deep CONVECTION
            IF( (KE.GE. DCT .AND. KB .LE. DCB .and. KB>1 .and.tmprr>0.5) .or. &
              (tmprr>=4.5 .and. dp>4.0)) THEN
              idcc=1
              dpdcc=dp
              call get_cld_feas(rho,km,z,kmm,ql,qi,kb,ke,cw,am,amz)
              dcc(1)=dcc(1)+dp
              dcc(2)=dcc(2)+cw
              dcc(3)=dcc(3)+am
              dcc(4)=dcc(4)+amz
              dcc(5)=dcc(5)+preci(ixx)*1.e3*3.6e3
              dcc(6)=dcc(6)+1.0
              !
              DO K = KB,KE
                QD(K,1) = QD(K,1) + C(K) ! TOTAL WATER CONTENT
                QD(K,2) = QD(K,2) + FRG    ! C(K)/QZD  ! cloud water/mean cloud water
                qD(K,3)   = qD(K,3)   + 1.
              ENDDO              
            ENDIF
            enddo
            if (mcpc>0)then
               mcp=mcp/mcpc
            endif
            !if (preci(ixx)*1.e3*3.6e3>4.0)then
            !  print*,'pre=',preci(ixx)*1.e3*3.6e3,dpmax
            !endif
            !call getidp(dpmax,dpbin,ndp,idp)
            !print*,'ixx1',ixx,pre5dptdcc(1,16)
            if (idcc>0 )then
              ib=-1
              idp=-1
              call getib(preci(ixx)*1.e3*3.6e3,rainbin,nb,ib)
              !rint*,'Dcc, ib',ib,tmprr
              call getidp(dpdcc,dpbin,ndp,idp)
              !print*,'dcc pre',ib,idp,preci(ixx)*1.e3*3.6e3
              !print*,'dcc dph',dpmax,dpdcc
              pre5dptdcc(ib,idp)=pre5dptdcc(ib,idp)+1.0
              contpredcc=contpredcc+1.0
              print*,'dcc,ib,idp',ib,idp,tmprr,dpdcc
              if (ib==1 .and. idp==16 )then
                 print*,ib,preci(ixx)*1.e3*3.6e3,dpdcc
                 stop
              endif
              dpdcc=0
              !idcc=0
            endif
            !print*,'ixx2',ixx,pre5dptdcc(1,16)
          !pre5dpt(ib,idp)=pre5dpt(ib,idp)+1.0
            if (preci(ixx)*1.e3*3.6e3>0.01.and. idcc==0)then
              ib=-1
              idp=-1
             call getib(preci(ixx)*1.e3*3.6e3,rainbin,nb,ib)
             call getidp(mcp,dpbin,ndp,idp)
              !print*,'cld pre',ib,idp,preci(ixx)*1.e3*3.6e3
             contpre=contpre+1.0
             pre5dpt(ib,idp)=pre5dpt(ib,idp)+1.0
            endif
            !print*,'ixx3',ixx,pre5dptdcc(1,16)
          enddo  ! loop ixx
          !Output file
          if (contpredcc>0)print*,'contpredcc=',contpredcc,pre5dptdcc(1,16)
          write(strs2,"(I5.5)")it
          fpath=trim(dirout)//yearstr//'_Cloud_Pre_F90_output_'//strs2//trim(addstr)//'.txt'
          open(90,file=trim(fpath))
          !#
          !print*, 'AAAA'
          !print*,'contpredcc=',pre5dptdcc(1,16),pre5dptdcc(31,15)
          do ib=1,nb
            do idp=1,ndp+1
              if (contpre>0)then         
                pre5dpt(ib,idp)=pre5dpt(ib,idp)/contpre
              endif
              if (contpredcc>0)then         
                pre5dptdcc(ib,idp)=pre5dptdcc(ib,idp)/contpredcc
                if (ib==1 .and.pre5dptdcc(ib,idp)>0 )then
                  print*,pre5dptdcc(ib,idp),ib,idp,contpredcc
                  stop
                endif
              endif
            enddo
          enddo

          !print*, 'AAAA',ndp+1
          !print*, pre5dpt(ib,:)
          write(90,*)contpre
          write(90,*)contpredcc
          do ib=1,nb
            do idp=1,ndp+1
            write(90,*) pre5dpt(ib,idp)
            pre5dpt(ib,idp)=0.0
            write(90,*) pre5dptdcc(ib,idp)
            pre5dptdcc(ib,idp)=0.0
            enddo 
          enddo
          contpredcc=0.0
          contpre=0.0
          !
          if(dcc(6)>0)then
            do i=1,5
            dcc(i)=dcc(i)/dcc(6)
            enddo
          endif
          write(90,*)dcc(6)
          dcc(6)=0.0
          do i=1,5
            write(90,*)dcc(i)
            dcc(i)=0.0
          enddo
          !write(90,*)dcc(6)
          do i=1,kmm
            write(90,*) qd(i,3)
            if (qD(i,3) >0)then
              do j=1,2
              QD(i,j) = QD(i,j)/qd(i,3)
              enddo
            endif
            do j=1,2
            write(90,*) qd(i,j)
            qd(i,j)=0.0
            enddo      
          enddo
          qd(:,3)=0.0
        do i=1,kmm
          do j=1,kmm
          write(90,*) ft(i,j)
          ft(i,j)=0.0
          enddo        
        enddo
        write(90,*)tmprain
        tmprain=0.0
        do j=1,3
          write(90,*)mcld(j)
          mcld(j)=0.0
        enddo
        close(90)     
        enddo ! loop inn
        close(80)  
      enddo ! loop nfl
      close(81)
99    format('e10.6')
98    format('e10.6')
97    format('e10.6')
96    format('E10.6')
95    format('e10.6')
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
      if (a<=0.01)then
        rr=0
      else
        rr=a
      endif
      if(rr>rainbin(nb))then
      ib=nb
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
      cw=cw+dz*1.*rho(i)*(ql(i)+qi(i))
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

 


