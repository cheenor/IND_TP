Program GetStationData 
    implicit none
    integer nm,ndays(12),ny
    integer ncol(6)
    character filehead*50, vars(6)*3, fstring(6)*5
    character yearstr*4,monstr*2,daystr*2
    character filename*100,fpath*200,dirin*100,dirout*100
    integer idx(3)
    character varstrings*300,datestr*10
    !
    integer i,j,k,kk,nn,nc,ni
    integer id,im,iy,iv
    integer yy,mm,dd
    real lon,lat
    real tmp(17),region(4)
    real pdat(3),num(3)
    real defv
    !
    defv=32700
    dirin='/Volumes/DATA02/DATA/data/'
    dirout='/Volumes/MacHD/Work/Papers/INDMosoon_TP/Data/'
    filehead='SURF_CLI_CHN_MUL_DAY-'
    vars(1)='PRE'
    vars(2)='RHU'
    vars(3)='SSD'
    vars(4)='TEM'
    vars(5)='WIN'
    vars(6)='PRS'
    fstring(1)='13011'
    fstring(2)='13003'
    fstring(3)='14032'
    fstring(4)='12001'
    fstring(5)='11002'
    fstring(6)='10004'
    region(1)=89.9
    region(2)=100
    region(3)=34.9
    region(4)=37.5
    ncol(1)=13
    ncol(2)=11
    ncol(3)=9
    ncol(4)=13
    ncol(5)=17
    ncol(6)=13
    do i=1,12
        ndays(i)=31
    enddo
    ndays(4)=30
    ndays(6)=30
    ndays(9)=30
    ndays(11)=30
    nm=12
    ny=2009-1990+1
    idx(1)=8
    idx(2)=9
    idx(3)=10
    do iy=1990,2009
        print*,iy
        ndays(2)=28
        if (mod(iy,4)== 0 .and. mod(iy,100) /= 0)then
            ndays(2)=29
        elseif (mod(iy,100) == 0)then  
            ndays(2)=29
        endif
        write(yearstr,'(I4.4)')iy
        varstrings='Date '
        do iv=1,6
            if (vars(iv)=='PRE' )then
                varstrings=trim(varstrings)//' 20-8Pre '//'8-20Pre '//'20-20Pre '
            endif
            if (vars(iv)=='RHU' )then
                varstrings=trim(varstrings)//' RH '
            endif
            if (vars(iv)=='SSD' )then
                varstrings=trim(varstrings)//' SSD '
            endif
            if (vars(iv)=='TEM' )then
                varstrings=trim(varstrings)//' Temp '//'MaxTemp '//'MinTemp '
            endif
            if (vars(iv)=='PRS' )then
                varstrings=trim(varstrings)//' Pres '//'MaxPres '//'MinPres '
            endif
            if (vars(iv)=='WIN' )then
                varstrings=trim(varstrings)//' WSPD '//'MaxWSPD '//'MaxDir '
            endif
        enddo
        filename=yearstr//'_StationData_daily.txt'
        fpath=trim(dirout)//trim(filename)
        open(20,file=trim(fpath))
        print*,varstrings
        write(20,*)trim(varstrings)
        !--------------------------------------------------
        do im =1,nm
            write(monstr,'(I2.2)')im
            do id=1,ndays(im)                
                write(daystr,'(I2.2)')id
                datestr=yearstr//monstr//daystr//' '
                write(20,99)trim(datestr)
                do iv=1,6
                    if (vars(iv)=='PRE' )then
                    ni=3
                    endif
                    if (vars(iv)=='RHU' )then
                    ni=1
                    endif
                    if (vars(iv)=='SSD' )then
                    ni=1
                    endif
                    if (vars(iv)=='TEM' )then
                    ni=3
                    endif
                    if (vars(iv)=='PRS' )then
                    ni=3
                    endif
                    if (vars(iv)=='WIN' )then
                    ni=3
                    endif
                    filename=trim(filehead)//vars(iv)//'-'//fstring(iv)//'-'//yearstr//monstr//'.txt'
                    fpath=trim(dirin)//yearstr//'/'//trim(filename)
                    open(10,file=trim(fpath))
                    !print*,fpath
                    nn=ncol(iv)
                    num=0.0
                    pdat=0.0
                    !print*,'nn',nn
                    do while (.true.)
                        !print*,'num',num
                        read(10,*,end=100)(tmp(i),i=1,nn)
                        !print*,'tmp',tmp(1:nn)
                        lat=tmp(2)/100.
                        lon=tmp(3)/100.
                        !print*,'lat,lon',lat,lon
                        yy=int(tmp(5))
                        mm=int(tmp(6))
                        dd=int(tmp(7))
                        if (iy==yy .and. mm==im .and. dd==id)then
                            if (lon>region(1) .and. lon<region(2))then
                                if (lat>region(3) .and. lat<region(4))then                                    
                                    do i =1,ni
                                        k=idx(i)
                                        if (tmp(k)<defv)then
                                            pdat(i)=pdat(i)+tmp(k)
                                            num(i)=num(i)+1.0
                                        endif
                                    enddo
                                    
                                endif
                            endif
                        endif
                    enddo
                    100 continue
                    close(10)
                    do i =1,ni
                        if (num(i)>0)then
                            k=idx(i)
                            pdat(i)=pdat(i)/num(i)
                        else
                            pdat(i)=-999
                        endif
                        if (iv<6)then
                                write(20,"(E12.6)")pdat(i)
                        elseif(iv==6)then
                            if (i<ni)then
                                write(20,"(E12.6)")pdat(i)
                            else
                                write(20,"(E12.6)")pdat(i)
                            endif
                        endif
                    enddo 
                enddo
            enddo
        enddo
        close(20)
    enddo
    99 format(A100)
end Program
