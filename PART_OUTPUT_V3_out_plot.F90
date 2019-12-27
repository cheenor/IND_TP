Program Cloud_Pre_out_plot
  implicit none
  integer,PARAMETER :: kmm=34,nfl=73,INN=480
  integer,PARAMETER :: ndt=96,nday=30+31+30+31+31+30
  integer,PARAMETER :: nb=30,ndp=20
  !!!
  real z(kmm)
  integer nt
  integer ifl,it,idt,i,j,im,n
  integer ib,idp,iut
  real rainbin(nb),dpbin(ndp),rain,mcld(3)
  !
  real pre5dpt(nb,ndp+1),pre5dptdcc(nb,ndp+1)
  real dcc(5),qd(kmm,2)
  real ft(kmm,kmm)
  ! dayliy
  real ftday(kmm,kmm),qdday(kmm,2)
  real pre5dptday(nb,ndp+1),pre5dptdccday(nb,ndp+1)
  real pre5dptmon(nb,ndp+1),pre5dptdccmon(nb,ndp+1)
  real con5mon
  ! diurnal
  real qddu(ndt,kmm,2),dccdu(ndt,5)
  real pre5dptdu(ndt,nb,ndp+1),pre5dptdccdu(ndt,nb,ndp+1)
  real ftdu(ndt,kmm,kmm),contdu,raindu(ndt),mclddu(ndt,3)
  !
  character casenm*20,fpath*200,fold*20,dirin*200,strs*20
  character dirout*200,addstr*20,yearstr*4
  integer days(6),its,ite,itt,ndd
  real contpre,contpredcc,cnt_dcc,cnt_qd(kmm)
  real day_cnt_precld,day_cnt_qd(kmm),day_cnt_predcc
  real du_cnt_predcc(ndt),du_cnt_precld(ndt),du_cnt_dcc(ndt),du_cnt_qd(kmm,ndt)
  real mon_cnt_precld,mon_cnt_predcc
  data days/30,31,30,31,31,30/
  nt=ndt*nday
  !
  yearstr='1994'
  casenm='ETP2D0'
  fold='runfold'
  addstr='94norm'
  dirin='/chenjh2/Work/INDMSN_TP/Data/'
  dirout=dirin
  !if(casenm(1:3)=='MLY')then
  !      dirin='/nuist/p/work/chenjh/CRM/SurfaceHeatFlux/'//casenm(1:4)// &
  !  &   '/'//trim(fold)
  !    else
  !      dirin='/nuist/p/work/chenjh/CRM/SurfaceHeatFlux/'//casenm(1:3)// &
  !  &   '/'//trim(fold)
  !endif
  !open(81,file=trim(dirin)//'postdata/'//'preci_'//trim(casenm),convert='big_endian', &
  !  & form='UNFORMATTED',status='OLD')
  !call getbin(rainbin,dpbin,nb,ndp)
  iut=0
  idt=0
  ftday=0.0
  qdday=0.0
  pre5dptday=0.0
  pre5dptdccday=0.0
  ftday=0.0
  contdu=0.0
  dccdu=0.0
  qddu=0.0
  pre5dptdu=0.0
  pre5dptdccdu=0.0
  pre5dptday=0.0
  pre5dptdccday=0.0
  raindu=0.0
  ftdu=0.0
  con5mon=0
  pre5dptmon=0.0
  pre5dptdccmon=0.0
  day_cnt_precld=0.0
  day_cnt_predcc=0.0
  day_cnt_qd=0.0
  du_cnt_dcc=0.0
  du_cnt_precld=0.0
  du_cnt_predcc=0.0
  mon_cnt_predcc=0.0
  mon_cnt_precld=0.0
  du_cnt_qd=0.0 
  im=1
  it=1
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  fpath=trim(dirout)//trim(casenm)//'IND_file09_qd_day_'//trim(addstr)//'.txt'
  open(9,file=trim(fpath))
  fpath=trim(dirout)//trim(casenm)//'IND_file10_ft_day_'//trim(addstr)//'.txt'
  open(10,file=trim(fpath))
  fpath=trim(dirout)//trim(casenm)//'IND_file11_pre2clddpt_day_'//trim(addstr)//'.txt'
  open(11,file=trim(fpath))
  fpath=trim(dirout)//trim(casenm)//'IND_file12_pre2dccdpt_day_'//trim(addstr)//'.txt'
  open(12,file=trim(fpath))

  fpath=trim(dirout)//trim(casenm)//'IND_file13_dcc_feas_'//trim(addstr)//'.txt'
  open(13,file=trim(fpath))
  !fpath=trim(dirout)//trim(casenm)//'IND_file14_qd_feas_'//trim(addstr)//'.txt'
  !open(14,file=trim(fpath))
  fpath=trim(dirout)//trim(casenm)//'IND_file15_pre2clddpt_monthly_du_'//trim(addstr)//'.txt'
  open(15,file=trim(fpath))
  fpath=trim(dirout)//trim(casenm)//'IND_file16_pre2dccdpt_monthly_du_'//trim(addstr)//'.txt'
  open(16,file=trim(fpath))
  fpath=trim(dirout)//trim(casenm)//'IND_file17_dcc_feas_monthly_du_'//trim(addstr)//'.txt'
  open(17,file=trim(fpath))
  fpath=trim(dirout)//trim(casenm)//'IND_file18_qd_monthly_du_'//trim(addstr)//'.txt'
  open(18,file=trim(fpath))
  fpath=trim(dirout)//trim(casenm)//'IND_file19_ft_monthly_du_'//trim(addstr)//'.txt'
  open(19,file=trim(fpath))
  fpath=trim(dirout)//trim(casenm)//'IND_file20_pre_cld_du_evo_'//trim(addstr)//'.txt'
  open(20,file=trim(fpath))
  !!!!!!

  fpath=trim(dirout)//trim(casenm)//'IND_file21_pre2clddpt_mon_'//trim(addstr)//'.txt'
  open(21,file=trim(fpath))
  fpath=trim(dirout)//trim(casenm)//'IND_file22_pre2dccdpt_mon_'//trim(addstr)//'.txt'
  open(22,file=trim(fpath))
  !!!
  its=(31+28+31)*96+1
  ite=its+nday*96
  print*,'its,ite=',its,ite,days
  ndd=0
  do it=its,ite
    !do n=1,inn
      iut=iut+1
      idt=idt+1
      !it=it+1
      write(strs,'(I5.5)')it
      fpath=trim(dirout)//yearstr//'_Cloud_Pre_F90_output_'//trim(strs)//trim(addstr)//'.txt'
      open(90,file=trim(fpath))
      !#
      contpre=0.0
      contpredcc=0.0
      read(90,*) contpre
      read(90,*) contpredcc  
      do i=1,nb
        do idp=1,ndp+1
        read(90,*) pre5dpt(i,idp)
        read(90,*) pre5dptdcc(i,idp) 
        enddo
      enddo
      !
      cnt_dcc=0.0
      cnt_qd=0.0
      read(90,*)cnt_dcc
      do i=1,5
        read(90,*) dcc(i)
      enddo
      do i=1,kmm
        read(90,*)cnt_qd(i)
        do j=1,2
          read(90,*) qd(i,j)
        enddo       
      enddo
      do i=1,kmm
        do j=1,kmm
          read(90,*) ft(i,j)
        enddo        
      enddo
      read(90,*)rain
      do i=1,3
        read(90,*) mcld(i)
      enddo
      close(90)
      do i=1,5
        write(13,*) dcc(i)
      enddo
      !write(14,'(34e12.6)') (qd(i,1),i=1,34)
      !write(14,'(34e12.6)') (qd(i,2),i=1,34)       
      if (idt<=ndt)then
        ! dayliy mean
           
        do i=1,kmm
          day_cnt_qd(i)=  day_cnt_qd(i)+ cnt_qd(i) 
          !do j=1,2
          qdday(i,1)=qdday(i,1)+qd(i,1)*cnt_qd(i) !/(ndt*1.0)
          !enddo
          qdday(i,2)=qdday(i,2)+qd(i,2)/(ndt*1.0)
          do j=1,kmm
            ftday(i,j)=ftday(i,j)+ft(i,j)/(ndt*1.0)
            ftdu(iut,i,j)=ftdu(iut,i,j)+ft(i,j)
          enddo
        enddo
        day_cnt_precld=day_cnt_precld+contpre
        mon_cnt_precld=mon_cnt_precld+contpre
        du_cnt_precld(iut)=du_cnt_precld(iut)+contpre     
        do i=1,nb
          do j=1,ndp+1
            pre5dptday(i,j)=pre5dptday(i,j)+pre5dpt(i,j)*contpre  !/(ndt*1.0)            
            pre5dptmon(i,j)=pre5dptmon(i,j)+pre5dpt(i,j)*contpre  !/(ndt*1.0)/days(im)            
            pre5dptdu(iut,i,j)=pre5dptdu(iut,i,j)+pre5dpt(i,j)*contpre 
          enddo
        enddo
        day_cnt_predcc=day_cnt_predcc+contpredcc
        mon_cnt_predcc=mon_cnt_predcc+contpredcc
        du_cnt_predcc(iut)=du_cnt_predcc(iut)+contpredcc
        do i=1,nb
          do j=1,ndp+1
            pre5dptdccdu(iut,i,j)=pre5dptdccdu(iut,i,j)+pre5dptdcc(i,j)*contpredcc
            pre5dptdccday(i,j)=pre5dptdccday(i,j)+pre5dptdcc(i,j)*contpredcc!/(ndt*1.0)
            pre5dptdccmon(i,j)=pre5dptdccmon(i,j)+pre5dptdcc(i,j)*contpredcc !/(ndt*1.0)/days(im)
          enddo
        enddo
        !
        du_cnt_dcc(iut)=du_cnt_dcc(iut)+cnt_dcc
        do j=1,5
          dccdu(iut,j)=dccdu(iut,j)+dcc(j)*cnt_dcc
        enddo
        raindu(iut)=raindu(iut)+rain
        do j=1,3
          mclddu(iut,j)=mclddu(iut,j)+mcld(j)
        enddo
        raindu(iut)=raindu(iut)+rain
        
        do i=1,kmm
          du_cnt_qd(i,iut)= du_cnt_qd(i,iut)+ cnt_qd(i)
          qddu(iut,i,1)=qddu(iut,i,1)+qd(i,1)*cnt_qd(i)
          !do j=1,2
          qddu(iut,i,2)=qddu(iut,i,2)+qd(i,2) !*cnt_qd(i)
          !enddo
        enddo
      endif
      if(idt==ndt)then
        do i=1,kmm
          !do j=1,1
            if (day_cnt_qd(i)>0)then
              qdday(i,1)=qdday(i,1)/day_cnt_qd(i)
            else
              qdday(i,1)=0.0
            endif
            write(9,*) qdday(i,1)
            qdday(i,1)=0.0
            !enddo
            write(9,*) qdday(i,2)
            qdday(i,2)=0.0
          do j=1,34
            write(10,*) ftday(i,j)
            ftday(i,j)=0.0
          enddo       
        enddo
        ftday=0.0
        qdday=0.0
        do ib=1,nb 
          do idp=1,ndp+1
            if (day_cnt_precld>0 ) pre5dptday(ib,idp)=pre5dptday(ib,idp)/day_cnt_precld    
            write(11,*) pre5dptday(ib,idp)
            if (day_cnt_predcc>0 ) pre5dptdccday(ib,idp)=pre5dptdccday(ib,idp)/day_cnt_predcc
            write(12,*) pre5dptdccday(ib,idp)
            if (ib==1 .and.pre5dptdccday(ib,idp)>0 )then
              print*,pre5dptdccday(ib,idp),ib,idp
              stop
            endif
            pre5dptday(ib,idp)=0.0
            pre5dptdccday(ib,idp)=0.0
          enddo
        enddo 
        do itt=1,ndt
          write(20,*)raindu(itt)
          raindu(itt)=0.0
          do j=1,3
            write(20,*)mclddu(itt,j)
            mclddu(itt,j)=0.0
          enddo
        enddo 
        day_cnt_precld=0.0
        day_cnt_predcc=0.0
        day_cnt_qd=0.0   
        pre5dptday=0.0
        pre5dptdccday=0.0
        idt=0
        iut=0
        contdu=contdu+1.0
        ndd=ndd+1
      endif
      print*,'contdu=',contdu,im,idt
      if (contdu==days(im))then        
        do itt=1,ndt
          do i=1,5
            if(du_cnt_dcc(itt)>0)dccdu(itt,i)=dccdu(itt,i)/du_cnt_dcc(itt)
            write(17,*) dccdu(itt,i) !/contdu
          enddo
          do ib=1,nb 
            do idp=1,ndp+1
              if (du_cnt_precld(itt)>0)pre5dptdu(itt,ib,idp)=pre5dptdu(itt,ib,idp)/du_cnt_precld(itt)
              write(15,*) pre5dptdu(itt,ib,idp)!/contdu
              if (du_cnt_predcc(itt)>0)pre5dptdccdu(itt,ib,idp)=pre5dptdccdu(itt,ib,idp)/du_cnt_predcc(itt)
              write(16,*) pre5dptdccdu(itt,ib,idp)!/contdu
              !if(mon_cnt_predcc>0)pre5dptdccmon(ib,idp)=pre5dptdccmon(ib,idp)/mon_cnt_predcc
              !if(mon_cnt_precld>0)pre5dptmon(ib,idp)=pre5dptmon(ib,idp)/mon_cnt_precld
              !write(21,*)pre5dptmon(ib,idp)
              !write(22,*)pre5dptdccmon(ib,idp)
            enddo
          enddo
          do i=1,kmm
            do j=1,1
              if(du_cnt_qd(i,itt)>0)qddu(itt,i,j)=qddu(itt,i,j)/du_cnt_qd(i,itt)
              write(18,*) qddu(itt,i,j) !/contdu
            enddo
            write(18,*) qddu(itt,i,2)/contdu
            do j=1,kmm
              write(19,*) ftdu(itt,i,j)/contdu
            enddo
          enddo
        enddo
        do ib=1,nb 
          do idp=1,ndp+1
            if(mon_cnt_predcc>0)pre5dptdccmon(ib,idp)=pre5dptdccmon(ib,idp)/mon_cnt_predcc
            if(mon_cnt_precld>0)pre5dptmon(ib,idp)=pre5dptmon(ib,idp)/mon_cnt_precld
            write(21,*)pre5dptmon(ib,idp)
            write(22,*)pre5dptdccmon(ib,idp)
          enddo
        enddo
        du_cnt_dcc=0.0
        du_cnt_precld=0.0
        du_cnt_predcc=0.0
        mon_cnt_predcc=0.0
        mon_cnt_precld=0.0
        du_cnt_qd=0.0
        contdu=0.0
        dccdu=0.0
        qddu=0.0
        pre5dptdu=0.0
        pre5dptdccdu=0.0
        pre5dptmon=0.0
        pre5dptdccmon=0.0
        ftdu=0.0
        im=im+1
        print*,'im=',days(im-1),im-1
      endif
    !enddo ! loop inn  
  enddo ! loop nfl
do i=9,20
    close(i)
enddo 
print*,'ndd=',ndd 
!99 format(1X,21e12.6)
 end Program

!SUBROUTINE getbin(rainbin,dpbin,nb,ndp)
!  implicit none
!  integer nb,ndp
!  real rainbin(nb),dpbin(ndp)
!  DATA rainbin/0.0, 0.1,  0.2, 0.3, 0.4,
!    &          0.6, 0.8,  1.0, 1.2, 1.4,
!    &          1.6, 1.8,  2.0, 2.4, 2.8,
!    &          3.2, 3.6,  4.0, 4.6, 5.2,
!    &          5.8, 6.4,  7.0, 7.8, 8.6,
!    &          9.4, 10.2,  11, 12, 13/
!  DATA dpbin/0.5,  1.0, 1.5, 2.0, 2.5, 3.0, 3.5
!    &        4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0,7.5
!    &        8.0, 8.5, 9.0, 9.5,10/
!  RETURN
!end SUBROUTINE


 


