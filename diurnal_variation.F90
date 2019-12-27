    PROGRAM Diurnal_Variation
    implicit none
    INTEGER,PARAMETER ::KM=34,kbn=20,np=3,no=3,ne=1
    real ft(km,km)
    real FA(0:NO+1,NE),FB(KM,KM,NO,NE)
    real z(km),wd(km,kbn),td(km,kbn)
    real qd(km,km,np),qs(km,np),qp(km,km,np)
    real WS(km),TR(km),TS(km),wp(km,km)
    character*200 fpath,dirout,dirin
    character CASENM*20,CASENMSTR(3)*20
    character cloudtyp(5)*40,filestr*20
    CHARACTER DAYSTR*3,stepstr*2
    integer ity
    integer ign,j,k,i,days(12),nday,ise
    real ftse(96,4,km,km),ftmo(96,12,km,km)
    real contse(96,4,km,km),contmo(96,12,km,km)
    real fase(96,4,0:NO+1,NE),famo(96,12,0:NO+1,NE)
    real contfase(96,4,0:NO+1,NE),contfamo(96,12,0:NO+1,NE) 
    real fbse(96,4,KM,KM,NO,NE),fbmo(96,12,KM,KM,NO,NE)
    real contfbse(96,4,KM,KM,NO,NE),contfbmo(96,12,KM,KM,NO,NE)
    real tdse(96,4,km,km),tdmo(96,12,km,km)
    real conttdse(96,4,km,km),conttdmo(96,12,km,km)
    real qdse(96,4,3,km,km),qdmo(96,12,3,km,km)
    real contqdse(96,4,3,km,km),contqdmo(96,12,3,km,km)
    real wpse(96,4,km,km),wpmo(96,12,km,km)
    real contwpse(96,4,km,km),contwpmo(96,12,km,km)
    real qpse(96,4,3,km,km),qpmo(96,12,3,km,km)
    real contqpse(96,4,3,km,km),contqpmo(96,12,3,km,km)
    real wsse(96,4,km),wsmo(96,12,km)
    real contwsse(96,4,km),contwsmo(96,12,km)
    real trse(96,4,km),trmo(96,12,km)
    real conttrse(96,4,km),conttrmo(96,12,km)
    real tsse(96,4,km),tsmo(96,12,km)
    real conttsse(96,4,km),conttsmo(96,12,km)
    real qsse(96,4,3,km),qsmo(96,12,3,km)
    real contqsse(96,4,3,km),contqsmo(96,12,3,km)
    integer kb,ke,io,lc,id,im,idd,it
    integer ip
    CASENMSTR(3)='MLYR2D0' 
    CASENMSTR(2)='WTP2D0'
    CASENMSTR(1)='ETP2D0'
    cloudtyp(1)="DEEPCONVECTION_INFO"
    cloudtyp(2)="PBLDEEPCONVECTION_INFO"
    cloudtyp(3)="SHALLOWCONVECTION_INFO"
    cloudtyp(4)="ALLCLOUDCELSS_FREQUENC"
    cloudtyp(5)="OVERLAPCLOUDCELSS_FREQUENCY"
    dirin='../Data/'
    dirout='../Data/'
    do i=1,12
    days(i)=31
    enddo
    days(2)=28
    days(4)=30
    days(6)=30
    days(9)=30
    days(11)=30
    do ign =1,1
        CASENM=CASENMSTR(ign)(1:3)
        if (CASENM=="MLY")then
            CASENM=CASENMSTR(ign)(1:4)
        endif
        do ity=1,5
            ! all cloud cells
            ftse=0.0
            ftmo=0.0
            contse=0.0
            contmo=0.0
            ise=0
            id=0
            ! over lap
            fase=0.0;famo=0.0
            contfase=0.0;contfamo=0.0
            fbse=0.0;fbmo=0.0
            contfbse=0.0;contfbmo=0.0  
            !  deep cloud info
            tdse=0.0; tdmo=0.0
            conttdse=0.0; conttdmo=0.0
            qdse=0.0; qdmo=0.0
            contqdse=0.0; contqdmo=0.0
            ! PBL convection
            wpse=0.0; wpmo=0.0
            contwpse=0.0; contwpmo=0.0
            qpse=0.0; qpmo=0.0
            contqpse=0.0; contqpmo=0.0
            ! Showllow convection
            wsse=0.0; wsmo=0.0
            contwsse=0.0; contwsmo=0.0
            qsse=0.0; qsmo=0.0
            contqsse=0.0; contqsmo=0.0
            trse=0.0; trmo=0.0
            conttrse=0.0; conttrmo=0.0
            tsse=0.0; tsmo=0.0
            conttsse=0.0; conttsmo=0.0
            do im =1,12
                if (im==1 .or. im==2 .or. im==12)then
                    ise=4
                elseif(im==3.or. im==4 .or. im==5)then
                    ise=1
                elseif(im==6 .or. im==7 .or. im==8)then
                    ise=2
                elseif(im==9 .or. im==10 .or. im==11)then
                    ise=3
                endif                    
                do idd =1,days(im)
                    id=id+1
                WRITE(DAYSTR,'(I3.3)')ID
                do it=1,96
                    write(stepstr,'(I2.2)') it
                    FILESTR="Day"//DAYSTR//stepstr
                    FPATH =TRIM(DIRIN)//TRIM(CASENM)//'_'//trim(cloudtyp(ity))//      &
                               '_F90'//TRIM(filestr)//'.TXT'      ! ASCII
                    call readfile(fpath,km,kbn,np,ity,  &
                            ne,no, ft,fa,fb,  &
                         z,wd,td,qd,qs,WS,TR,TS)                            
                    if (ity==1) then ! DEEP
                        do kb=1,km
                            do ke=1,km
                                tdse(it,ise,kb,ke)=tdse(it,ise,kb,ke)+td(kb,ke)
                                tdmo(it,im,kb,ke)=tdmo(it,im,kb,ke)+td(kb,ke)
                                conttdse(it,ise,kb,ke)=conttdse(it,ise,kb,ke)+1.0
                                conttdmo(it,im,kb,ke)=conttdmo(it,im,kb,ke)+1.0
                                do ip =1,np
                                    qdse(it,ise,ip,kb,ke)=qdse(it,ise,ip,kb,ke)+qd(kb,ke,ip)
                                    qdmo(it,im,ip,kb,ke)=qdmo(it,ise,ip,kb,ke)+qd(kb,ke,ip)
                                    contqdse(it,ise,ip,kb,ke)=contqdse(it,ise,ip,kb,ke)+1.0
                                    contqdmo(it,im,ip,kb,ke)=contqdmo(it,im,ip,kb,ke)+1.0
                                enddo        
                            enddo
                        enddo      
                    elseif(ity==2)then !# PBL convection
                        do kb=1,km
                            do ke=1,km
                                wpse(it,ise,kb,ke)=wpse(it,ise,kb,ke)+wd(kb,ke)
                                wpmo(it,im,kb,ke)=wpmo(it,im,kb,ke)+wd(kb,ke)
                                contwpse(it,ise,kb,ke)=contwpse(it,ise,kb,ke)+1.0
                                contwpmo(it,im,kb,ke)=contwpmo(it,im,kb,ke)+1.0
                                do ip =1,np
                                    qpse(it,ise,ip,kb,ke)=qpse(it,ise,ip,kb,ke)+qd(kb,ke,ip)
                                    qpmo(it,im,ip,kb,ke)=qpmo(it,ise,ip,kb,ke)+qd(kb,ke,ip)
                                    contqpse(it,ise,ip,kb,ke)=contqpse(it,ise,ip,kb,ke)+1.0
                                    contqpmo(it,im,ip,kb,ke)=contqpmo(it,im,ip,kb,ke)+1.0
                                enddo        
                            enddo
                        enddo 
                    elseif(ity==3)then ! showllow convection
                        do kb=1,km
                            wsse(it,ise,kb)=wsse(it,ise,kb)+ws(kb)
                            trse(it,ise,kb)=trse(it,ise,kb)+tr(kb)
                            tsse(it,ise,kb)=tsse(it,ise,kb)+ts(kb)
                            trmo(it,im,kb)=trmo(it,im,kb)+tr(kb)
                            wsmo(it,im,kb)=wsmo(it,im,kb)+ws(kb)
                            tsmo(it,im,kb)=tsmo(it,im,kb)+ts(kb)
                            contwsmo(it,im,kb)=contwsmo(it,im,kb)+1.0
                            contwsse(it,ise,kb)=contwsse(it,ise,kb)+1.0
                            conttrmo(it,im,kb)=conttrmo(it,im,kb)+1.0
                            conttrse(it,ise,kb)=conttrse(it,ise,kb)+1.0
                            conttsmo(it,im,kb)=conttsmo(it,im,kb)+1.0
                            conttsse(it,ise,kb)=conttsse(it,ise,kb)+1.0
                            do ip=1,np
                               qsse(it,ise,ip,kb)=qsse(it,ise,ip,kb)+qs(kb,ip)
                               qsmo(it,im,ip,kb)= qsmo(it,im,ip,kb)+qs(kb,ip)
                               contqsmo(it,im,ip,kb)= contqsmo(it,im,ip,kb)+1.0
                               contqsse(it,ise,ip,kb)= contqsse(it,ise,ip,kb)+1.0
                            enddo
                        enddo
                    elseif(ity==4)then
                        do kb=1,km
                            do ke=1,km
                                ftse(it,ise,kb,ke)=ftse(it,ise,kb,ke)+ft(kb,ke)
                                ftmo(it,im,kb,ke)=ftmo(it,im,kb,ke)+ft(kb,ke)
                                contse(it,ise,kb,ke)=contse(it,ise,kb,ke)+1.0
                                contmo(it,im,kb,ke)=contmo(it,im,kb,ke)+1.0
                            enddo
                        enddo
                    elseif(ity==5)then
                        do lc=1,ne
                            do io=0,no+1
                                fase(it,ise,io,lc)=fase(it,ise,io,lc)+fa(io,lc)
                                contfase(it,ise,io,lc)=contfase(it,ise,io,lc)+1.0
                                famo(it,im,io,lc)=famo(it,im,io,lc)+fa(io,lc)
                                contfamo(it,im,io,lc)=contfamo(it,im,io,lc)+1.0                            
                            enddo
                            do io=1,no
                                do kb=1,km
                                do ke=1,km
                                    fbse(it,ise,kb,ke,io,lc)=fbse(it,ise,kb,ke,io,lc)+fb(kb,ke,io,lc)
                                    fbmo(it,im,kb,ke,io,lc)=fbmo(it,im,kb,ke,io,lc)+fb(kb,ke,io,lc)
                                    contfbse(it,ise,kb,ke,io,lc)=contfbse(it,ise,kb,ke,io,lc)+1.0
                                    contfbmo(it,im,kb,ke,io,lc)=contfbmo(it,im,kb,ke,io,lc)+1.0
                                enddo
                                enddo
                            enddo
                        enddo
                    endif
                enddo
                enddo
            enddo 
            call output(4,km,kbn,np,no,ne,ity, &
                dirout,CASENM,cloudtyp(ity),  &
                   ftse,contse,     &
                fase,contfase,    &
                fbse,contfbse,    &
                tdse,               &
                conttdse,       &
                qdse,               &
                contqdse,       &
                wpse,               &
                contwpse,       &
                qpse,               &
                contqpse,       &
                wsse,               &
                contwsse,       &
                trse,               &
                conttrse,       &
                tsse,               &
                conttsse,       &
                qsse,               &
                contqsse          )
            call output(12,km,kbn,np,no,ne,ity, &
                dirout,CASENM,cloudtyp(ity),  &
                   ftmo,contmo,     &
                famo,contfamo,    &
                fbmo,contfbmo,    &
                tdmo,               &
                conttdmo,       &
                qdmo,               &
                contqdmo,       &
                wpmo,               &
                contwpmo,       &
                qpmo,               &
                contqpmo,       &
                wsmo,               &
                contwsmo,       &
                trmo,               &
                conttrmo,       &
                tsmo,               &
                conttsmo,       &
                qsmo,               &
                contqsmo          )
        enddo
    enddo
    end PROGRAM
    SUBROUTINE readfile(fpath,km,kbn,np,ity,  &
                            ne,no, ft,fa,fb,  &
                          z,wd,td,qd,qs,WS,TR,TS)
    implicit none
    character*200 fpath
    integer km,kbn,np,ity
    real z(km),wd(km,kbn),td(km,kbn)
    real qd(km,kbn,np),qs(km,np)
    real ft(km,km)
    real WS(km),TR(km),TS(km)
    integer i,k,ip,kb,ig
    integer lc,io,ne,no,ic,itmp2
    real itmp6
    real FA(0:NO+1,NE),FB(KM,KM,NO,NE)
    character*10 str1,str2,str3,str5
    z=0.0
    wd=0.0
    td=0.0
    qd=0.0
    qs=0.0
    ws=0.0
    tr=0.0
    ts=0.0
    ft=0.0
    fa=0.0
    fb=0.0
    open(10,file=trim(fpath))
    if (ity==1 .or. ity==2) then 
        read(10,*)
        do k=km,1,-1 ! top to srf
        read(10,'(21E12.4)')Z(K),(WD(K,KB),KB=1,kbn) ! samples
        enddo
        if (ity==1)then
            read(10,*)
            read(10,*)
            do k=km,1,-1 ! top to srf
                read(10,'(21E12.4)')Z(K),(TD(K,KB),KB=1,kbn) ! POT TEMPERATURE
            enddo 
        endif   
        read(10,*)
        do ip=1,np
        read(10,*)
        do k=km,1,-1 ! top to srf
        read(10,'(21E12.4)')Z(K),(QD(K,KB,ip),KB=1,kbn) ! profile KB cloud base 
        enddo
        read(10,*)
        enddo
    elseif (ity==3)then
        read(10,*)
        read(10,*)
        do k=km,1,-1 ! top to srf
            read(10,'(10E12.4)')Z(K),WS(K),TR(K),TS(K),(QS(K,IP),IP=1,NP)
        enddo
    elseif(ity==4)then !# read cloud cover
        do ig=1,4     ! why skip these lines, see Part_output.F 
                      ! this file just get domain cloud cover,grid 001-200
            read(10,*)
            do K=km,1,-1
            read(10,*)
            enddo
            read(10,*)
        enddo 
        read(10,*)
        do K=km,1,-1
            read(10,'(37E12.4)') Z(K),(FT(KB,K),KB=1,KM)
        enddo
        read(10,*)
    elseif(ity==5)then
        do lc=1, ne 
            do io=1, no 
                read(10,'(A,I2,F8.3,A)'),str1,itmp2,itmp6,str2
                read(10,'(A,I2,A,10G12.5)')str3,itmp2, str5,(FA(IC,LC),IC=0,NO+1)
                do k=km,1,-1
                read(10,'(37E12.4)')Z(K),(FB(KB,K,IO,LC),KB=1,KM)
                enddo
                read(10,*)
            enddo
        enddo
    endif
    return     
    end SUBROUTINE
    SUBROUTINE output(nt,km,kbn,np,no,ne,ity, &
                dirout,CASENM,cloudtyp,  &
                   ftse,contse,     &
                fase,contfase,    &
                fbse,contfbse,    &
                tdse,               &
                conttdse,       &
                qdse,               &
                contqdse,       &
                wpse,               &
                contwpse,       &
                qpse,               &
                contqpse,       &
                wsse,               &
                contwsse,       &
                trse,               &
                conttrse,       &
                tsse,               &
                conttsse,       &
                qsse,               &
                contqsse          )
    integer km,kbn,np,no,ne,ity,nt
    character*200, dirout
    character CASENM*20,cloudtyp*40
    !===========================================
    real ftse(96,nt,km,km)
    real contse(96,nt,km,km)
    real fase(96,nt,0:NO+1,NE)
    real contfase(96,nt,0:NO+1,NE)
    real fbse(96,nt,KM,KM,NO,NE)
    real contfbse(96,nt,KM,KM,NO,NE)
    real tdse(96,nt,km,km)
    real conttdse(96,nt,km,km)
    real qdse(96,nt,3,km,km)
    real contqdse(96,nt,3,km,km)
    real wpse(96,nt,km,km)
    real contwpse(96,nt,km,km)
    real qpse(96,nt,3,km,km)
    real contqpse(96,nt,3,km,km)
    real wsse(96,nt,km)
    real contwsse(96,nt,km)
    real trse(96,nt,km)
    real conttrse(96,nt,km)
    real tsse(96,nt,km)
    real conttsse(96,nt,km)
    real qsse(96,nt,3,km)
    real contqsse(96,nt,3,km)
    !===============================================  
    character season(4)*20,fpath*200,monstr*2
    integer i,j,k,im,kb,ke,io,lc,ip,it
    real aout(km,km)
    season(1)='Spring'
    season(2)='Summer'
    season(3)='Autumn'
    season(4)='Winter'
    ! season 
    do i=1,nt
        if (nt==4)then
            fpath=trim(dirout)//trim(CASENM)//trim(season(i))//'_'//trim(cloudtyp)//'.txt'
        else
            write(monstr,'(I2.2)')i
            fpath=trim(dirout)//trim(CASENM)//'Mon'//monstr//'_'//trim(cloudtyp)//'.txt'
        endif
        open(10,file=trim(fpath))
        do it=1,96
            if (ity==1) then ! DEEP
                call calmean(tdse(it,i,:,:),conttdse(it,i,:,:),km,aout)
                do kb=1,km
                    write(10,'(34E12.4)')(aout(kb,ke),ke=1,km)
                enddo
                do ip =1,np
                    call calmean(qdse(it,i,ip,:,:),contqdse(it,i,ip,:,:),km,aout)
                    do kb=1,km
                        write(10,'(34E12.4)')(aout(kb,ke),ke=1,km)
                    enddo       
                enddo       
            elseif(ity==2)then !# PBL convection
                call calmean(wpse(it,i,:,:),contwpse(it,i,:,:),km,aout)
                do kb=1,km
                    write(10,'(34E12.4)')(aout(kb,ke),ke=1,km)
                enddo
                do ip =1,np
                    call calmean(qpse(it,i,ip,:,:),contqpse(it,i,ip,:,:),km,aout)
                    do kb=1,km
                        write(10,'(34E12.4)')(aout(kb,ke),ke=1,km)
                    enddo       
                enddo    
            elseif(ity==3)then ! showllow convection
                do kb=1,km
                    if (contwsse(it,i,kb)> 0 )then
                        wsse(it,i,kb)=wsse(it,i,kb)/contwsse(it,i,kb)
                    endif
                    if (conttrse(it,i,kb)> 0 )then
                        trse(it,i,kb)=trse(it,i,kb)/conttrse(it,i,kb)
                    endif                   
                    if (conttsse(it,i,kb)> 0 )then
                        tsse(it,i,kb)=tsse(it,i,kb)/conttsse(it,i,kb)
                    endif

                    do ip=1,np
                        if (contqsse(it,i,ip,kb)> 0 )then
                            qsse(it,i,ip,kb)=qsse(it,i,ip,kb)/contqsse(it,i,ip,kb)
                        endif
                    enddo
                enddo
                write(10,'(34E12.4)')(wsse(it,i,k),k=1,km)
                write(10,'(34E12.4)')(trse(it,i,k),k=1,km)
                write(10,'(34E12.4)')(tsse(it,i,k),k=1,km)
                do ip=1,np
                    write(10,'(34E12.4)')(qsse(it,i,ip,k),k=1,km)
                enddo
            elseif(ity==4)then
                call calmean(ftse(it,i,:,:),contse(it,i,:,:),km,aout)
                do kb=1,km
                    write(10,'(34E12.4)')(aout(kb,ke),ke=1,km)
                enddo 
            elseif(ity==5)then
                do lc=1,ne
                    do io=0,no+1
                        if (contfase(it,ise,io,lc)>0)then
                            fase(it,ise,io,lc)=fase(it,ise,io,lc)/contfase(it,ise,io,lc)
                        endif
                    enddo
                    write(10,'(5E12.4)')(fase(it,ise,io,lc),io=0,no+1)
                enddo
                do lc=1,ne
                do io=1,no
                    call calmean(fbse(it,i,:,:,io,lc),contfbse(it,i,:,:,io,lc),km,aout)
                    do kb=1,km
                        write(10,'(34E12.4)')(aout(kb,ke),ke=1,km)
                    enddo
                enddo 
                enddo          
            endif
        enddo ! it
        close(10)
    enddo
    return
    end SUBROUTINE
    SUBROUTINE calmean(datin,cont,km,aout)
    integer km
    real datin(km,km),cont(km,km),aout(km,km)
    integer i,j
    do i=1,km
        do j=1,km
            aout(i,j)=0.0
            if (cont(i,j)>0)then
                aout(i,j)=datin(i,j)/cont(i,j)
            endif
        enddo
    enddo
    return
    end SUBROUTINE
