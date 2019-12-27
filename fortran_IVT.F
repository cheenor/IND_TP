subroutine cal_IVT(u,v,qv,srf,plv,iz1,iz2,nt,nz,ny,nx,ivt)
implicit none
integer, intent(in):: nt,nz,ny,nx
integer, intent(in):: iz1,iz2
real, dimension(nt,nz,ny,nx), intent(in):: u,v,qv
real, dimension(ny,nx), intent(in):: srf
real, dimension(nz), intent(in):: plv
real, dimension(nt,ny,nx), intent(out):: ivt
integer it,iz,ix,iy
ivt=0
do it=1,nt
    do ix=1,nx
        do iy=1,ny
            ivt(it,iy,ix)=0
            do iz=iz1+1,iz2+1 !differecs between fortran and fortran
                



            enddo
        enddo
    enddo
enddo
return
end subroutine