Program Cloud_Pre_out_plot
  implicit none
  integer,PARAMETER :: kmm=34
  integer,PARAMETER :: ndt=96,nday=30+31+30+31+31+30
  integer,PARAMETER :: nb=30,ndp=20
  !!!
  real z(kmm)
  integer nt
  integer ifl,it,idt,i,j,im
  integer ib,idp
  real rainbin(nb),dpbin(ndp),rain,mcld(3)
  !
  real pre5dpt(nb,ndp+1),pre5dptdcc(nb,ndp+1)
  real dcc(5),qd(kmm,2)
  real ft(kmm,kmm)
  ! dayliy
  real ftday(kmm,kmm),qdday(kmm,2)
  real pre5dptday(nb,ndp+1),pre5dptdccday(nb,ndp+1)
  ! diurnal
  real qddu(ndt,kmm,2),dccdu(ndt,5)
  real pre5dptdu(ndt,nb,ndp+1),pre5dptdccdu(ndt,nb,ndp+1)
  real ftdu(ndt,kmm,kmm),contdu,raindu(ndt),mclddu(ndt,3)
  !
  character casenm*20,fpath*200,fold*20,dirin*200,strs*20
  character strs*3,dirout*200,addstr*20,yearstr*4
  integer days(6)
  data days/30,31,30,31,31,30/
  nt=ndt*nday
  !
  yearstr='1994'
  casenm='ETP2D0'
  fold='runfold'
  addstr='norm'
  if(casenm(1:3)=='MLY')then
        dirin='/nuist/p/work/chenjh/CRM/SurfaceHeatFlux/'//casenm(1:4)// &
    &   '/'//trim(fold)
      else
        dirin='/nuist/p/work/chenjh/CRM/SurfaceHeatFlux/'//casenm(1:3)// &
    &   '/'//trim(fold)
  endif
  open(81,file=trim(dirin)//'postdata/'//'preci_'//trim(casenm),convert='big_endian', &
    & form='UNFORMATTED',status='OLD')
  call getbin(rainbin,dpbin,nb,ndp)
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
  im=1
  it=0
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
  do ifl=1,nfl
    do n=1,inn
      iut=iut+1
      idt=idt+1
      it=it+1
      write(strs,'(I3.3)')it
      fpath=trim(dirout)//yearstr//'_Cloud_Pre_F90_output_'//strs//trim(addstr)//'.txt'
      open(90,file=trim(fpath))
      !#      
      do i=1,nb
        do idp=1,ndp+1
        read(90,*) pre5dpt(i,idp)
        read(90,*) pre5dptdcc(i,idp) 
        enddo
      enddo
      !
      do i=1,5
        read(90,*) dcc(i)
      enddo
      do i=1,kmm
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
      write(13,'(5e12.6)') (dcc(i),i=1,5)
      !write(14,'(34e12.6)') (qd(i,1),i=1,34)
      !write(14,'(34e12.6)') (qd(i,2),i=1,34)       
      if (idt<=ndt)then
        do i=1,kmm
          do j=1,2
            qdday(i,j)=qdday(i,j)+qd(i,j)/(ndt*1.0)
          enddo
          do j=1,kmm
            ftday(i,j)=ftday(i,j)+ft(i,j)/(ndt*1.0)
            ftdu(iut,i,j)=ftdu(iut,i,j)+ft(i,j)
          enddo
        enddo
         do i=1,nb
          do j=1,ndp+1
            pre5dptday(i,j)=pre5dptday(i,j)+pre5dpt(i,j)/(ndt*1.0)
            pre5dptdccday(i,j)=pre5dptdccday(i,j)+pre5dptdcc(i,j)/(ndt*1.0)
            pre5dptdu(iut,i,j)=pre5dptdu(iut,i,j)+pre5dpt(i,j)
            pre5dptdccdu(iut,i,j)=pre5dptdccdu(iut,i,j)+pre5dptdcc(i,j)
          enddo
        enddo
        !
        do j=1,5
          dccdu(iut,j)=dccdu(iut,j)+dcc(j)
        enddo
        raindu(iut)=raindu(iut)+rain
        do j=1,3
          mclddu(iut,j)=mclddudu(iut,j)+mclddu(j)
        enddo
        raindu(idt)=raindu(idt)+rain
        do i=1,kmm
          do j=1,2
            qddu(iut,i,j)=qddu(iut,i,j)+qd(i,j)
          enddo
        enddo
      endif
      if(idt==ndt)then
        do i=1,kmm
          write(9,'(1X,2e12.6)') (qdday(i,j),j=1,2) 
          write(10,'(1X,34e12.6)') (ftday(i,j),j=1,34)        
        enddo
        ftday=0.0
        qdday=0.0
        do i=1,nb          
          write(11,99) (pre5dptday(ib,idp),idp=1,ndp+1)
          write(12,99) (pre5dptdccday(ib,idp),idp=1,ndp+1) 
        enddo 
        do idt=1,ndt
          write(20,'(1X,4e12.6)') raindu(idt),(mclddu(j),j=1,3)
        enddo      
        pre5dptday=0.0
        pre5dptdccday=0.0
        idt=0
        iut=0
        contdu=contdu+1.0
      endif
      if (contdu==days(im))then        
        do idt=1,ndt
          write(17,'(1X,5e12.6)') (dccdu(idt,i)/contdu,i=1,5)
          do i=1,nb          
            write(15,99) (pre5dptdu(idt,ib,idp)/contdu,idp=1,ndp+1)
            write(16,99) (pre5dptdccdu(idt,ib,idp)/contdu,idp=1,ndp+1) 
          enddo
          do i=1,kmm
            write(18,'(1X,2e12.6)') (qddu(idt,i,j)/contdu,j=1,2) 
            write(19,'(1X,34e12.6)') (ftdu(idt,i,j)/contdu,j=1,34) 
        enddo     
        contdu=0.0
        dccdu=0.0
        qddu=0.0
        pre5dptdu=0.0
        pre5dptdccdu=0.0
        ftdu=0.0
        im=im+1
        print*,'im=',days(im-1),im-1
      endif
    enddo ! loop inn  
  enddo ! loop nfl
do i=9,20
    close(i)
enddo  
!99 format(1X,21e12.6)
 end Program

SUBROUTINE getbin(rainbin,dpbin,nb,ndp)
  implicit none
  integer nb,ndp
  real rainbin(nb),dpbin(ndp)
  DATA rainbin/0.0, 0.1,  0.2, 0.3, 0.4,
    &          0.6, 0.8,  1.0, 1.2, 1.4,
    &          1.6, 1.8,  2.0, 2.4, 2.8,
    &          3.2, 3.6,  4.0, 4.6, 5.2,
    &          5.8, 6.4,  7.0, 7.8, 8.6,
    &          9.4, 10.2,  11, 12, 13/
  DATA dpbin/0.5,  1.0, 1.5, 2.0, 2.5, 3.0, 3.5
    &        4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0,7.5
    &        8.0, 8.5, 9.0, 9.5,10/
  RETURN
end SUBROUTINE


 


