subroutine eachfile(onedim,region,idx,yy0,im,idd,nl,ncol,nn,n4,nc,cnt,tmp)
     implicit none
     integer, intent(in) :: yy0,im,idd,nl,ncol
     integer, intent(in) :: nn,n4,nc     
     real,dimension(nn),intent(in) :: onedim
     real,dimension(n4),intent(in) :: region
     integer,dimension(nc),intent(in) :: idx
     real,intent(out) :: cnt
     real,dimension(nc),intent(out) :: tmp

     !
     integer i,j,k,kk
     integer yy,mm,dd
     real lon,lat
     real tmpr(nl,ncol)

     cnt=0
     tmp=0.0
     do i =1,nl
        do j=1,ncol
            tmpr(i,j)=0.0
            k=(i-1)*ncol+j
            tmpr(i,j)=onedim(k)
        enddo
        lat=tmpr(i,2)/100.
        lon=tmpr(i,3)/100.
        yy=int(tmpr(i,5))
        mm=int(tmpr(i,6))
        dd=int(tmpr(i,7))
        if(yy==yy0 .and. mm==im .and. dd==idd)then
            if(lon>region(1) .and. lon<=region(2))then
                if(lat>region(3) .and. lat<= region(4))then
                    do j=1,nc
                        kk=idx(j)
                        tmp(j)=tmp(j)+tmpr(i,kk)
                    enddo
                    cnt=cnt+1.0
                endif
            endif
        endif
     enddo
     return
end subroutine eachfile
