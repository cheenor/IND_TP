      program CN5_2
	implicit none
	integer,parameter :: NX=142
	integer,parameter :: NY=82
      character fnm*100,dir*100,nm(2)*80
	integer i,j,k,it,day(12)
	integer iy,iyy,nd,id,im
	real raw(2,50,12,31,NX,NY) !,rian(50,366,NX,NY)
    real, parameter (blat=14.75,blon=69.75,intr=0.5)




!------- path strings--------------
	dir='Z:\DATA\CN05\CN05.2\'
      nm(2)='2400_China_Pre_1961_2010_Full_daily_05x05.dat'
	nm(1)='2400_China_Tm_1961_2010_Full_daily_05x05.dat'
!---------------------------------------------------------
      do i=1,12
	day(i)=30
	enddo
	day(1)=31;day(3)=31;day(5)=31;day(7)=31
	day(8)=31;day(10)=31;day(12)=31


	do k=1,2
	 fnm=trim(dir)//trim(nm(k))
	 open(10,file=trim(fnm),form='binary') 
	  do iyy=1961,2010
	    iy=iyy-1960
         day(2)=28
!-------------- 
	    if(mod(iyy,4)==0.and.mod(iyy,100)/=0)then
	     day(2)=29
	    elseif(mod(iyy,400)==0)then
	   	 day(2)=29
	    endif
!-----------------------------          
		do im=1,12
	       nd=day(im)
           do id=1,nd
	      do j=1,NY
	       do i=1,NX
              read(10)raw(k,iy,im,id,i,j)
	       enddo
	      enddo
	     enddo
	   enddo
	  enddo
	enddo
!----------test raw(1,1,im,id,i,j)
	print*, raw(1,1,1,1,1,1),raw(1,1,1,1,1,2)
	print*, raw(1,1,1,1,2,1),raw(1,1,1,1,2,1)
	print*, raw(1,1,1,1,1,81),raw(1,1,1,1,1,82)
!------- the result  --------------------
	call output(raw)
	
	
	
	end

	subroutine output(input)
	implicit none
	integer,parameter :: NX=142
	integer,parameter :: NY=82
	real input(2,50,12,31,NX,NY)
	real out(2,3,12,5),lon,lat !!! 98-00 monthly
	real tlons,tlone,tlats,tlate
	real temp(2,5),XYD
	integer iys,iye,ims,ime,ids,ide
	integer lons(5),lone(5),lats(5),late(5)
	integer day(12),kk(2,5)
	integer iy,im,nd,id,ig,i,j,k,iyy

!-----------EA--------------------------------------------------
	lons(1)=100;lone(1)=140
	lats(1)=10;late(1)=55
!-----------PRD--------------------------------------------------
	lons(2)=110;lone(2)=118
	lats(2)=21;late(2)=25
!-----------MLYR--------------------------------------------------
	lons(3)=110;lone(3)=122
	lats(3)=27;late(3)=33
!-----------NPC--------------------------------------------------
	lons(4)=112;lone(4)=120
	lats(4)=34;late(4)=42
!-----------NEC--------------------------------------------------
	lons(5)=120;lone(5)=130
	lats(5)=43;late(5)=49
!++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
!---------------------------------------------------------
      do i=1,12
	day(i)=30
	enddo
	day(1)=31;day(3)=31;day(5)=31;day(7)=31
	day(8)=31;day(10)=31;day(12)=31
!!!!!------ the output data period
	iys=1998;iye=2000
	ims=1;ime=12
	ids=1;ide=31
      
	do k=1,2  ! temp, rian 
        do iyy=1998,2000
	    iy=iyy-1960
	    day(2)=28
!-------------- 
	    if(mod(iyy,4)==0.and.mod(iyy,100)/=0)then
	     day(2)=29
	    elseif(mod(iyy,400)==0)then
	   	 day(2)=29
	    endif
!----------------------------
          do im=1,12
	 nd=day(im)
		  kk=0
	      temp=0.
           do ig=1,5 ! region

	      tlons= lons(ig);tlone= lone(ig)
	      tlats= lats(ig);tlate= late(ig)
	      do id=1,nd
	       do j=1,NY
	         lat=14.75+0.5*(j-1)
	        do i=1,NX
	          lon=69.75+0.5*(i-1)
	if(input(k,iy,im,id,i,j)/=-9999.0)then
	 if(lon>=tlons.and.lon<=tlone)then 
	   if(lat>=tlats.and.lat<=tlate)then
	          temp(k,ig)=temp(k,ig)+input(k,iy,im,id,i,j)
	          kk(k,ig)=kk(k,ig)+1
      endif
	endif
	endif
	          enddo !NX
	        enddo !NY
	       enddo ! nd
	       XYD=kk(k,ig) !*nd*1.0
!	print*,kk(k,ig)
	      out(k,iyy-1997,im,ig)=temp(k,ig)/XYD
	     enddo !ig
	  enddo !im
       enddo !iy
	enddo !K
	open(100,file='tm_mon36.txt')
	open(200,file='Pre_mon36.txt')
	write(100,99)'month','EA','PRD','MLYR','NPC','NEC'
	write(200,99)'month','EA','PRD','MLYR','NPC','NEC'
	do iy=1,3
	  do im=1,12
	    write(100,98)im,(out(1,iy,im,ig),ig=1,5)
	    write(200,98)im,(out(2,iy,im,ig),ig=1,5)
	  enddo
	enddo
99    format(1X,A5,5(1X,A4))
98    format(1X,I2,5(1X,F12.6))
	end subroutine
