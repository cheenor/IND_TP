subroutine meantrmm_loop(precip,lon,lat,slon,elon,slat,elat,nx,ny,tmp)
implicit none
integer, intent(in):: nx,ny
real, dimension(nx,ny), intent(in)::precip
real, dimension(nx), intent(in)::lon
real, dimension(ny), intent(in)::lat
real, intent(in):: slon,elon,slat,elat
real,intent(out):: tmp
integer ix,iy
real cont
cont=0.
tmp=0.
do ix=1,nx 
	if (lon(ix)>slon .and. lon(ix)<elon)then
		do iy =1, ny 
			if ( lat(iy)>slat .and. lat(iy)<elat)then
				if precip[ix,iy]>=0.0 :
					tmp=tmp+precip(ix,iy)
					cont=cont+1.
				endif
			endif
		enddo
	endif
enddo
if (cont>0)then
	tmp=tmp/cont
endif
return
end subroutine
