#!/bin/bash

for protocol in tcp udp ; 
do 
    #echo "protocol $protocol" ; 
    for ipportinode in `cat /proc/net/tcp | awk '/.*:.*:.*/{print $2"|"$3"|"$10 ;}'` ; 
    do 
        #echo "#ipportinode=$ipportinode"
        inode=`echo "$ipportinode" | cut -d"|" -f3` ;
        if [ "#$inode" = "#" ] ; then continue ; fi 
        lspid=`ls -l /proc/*/fd/* 2>/dev/null | grep "socket:\[$inode\]" 2>/dev/null` ; 
        pid=`echo "lspid=$lspid" | awk 'BEGIN{FS="/"} /socket/{print $3}'` ;
        if [ "#$pid" = "#" ] ; then continue ; fi
        exefile=`ls -l /proc/$pid/exe | awk 'BEGIN{FS=" -> "}/->/{print $2;}'`
        #echo "$protocol|$pid|$ipportinode" 
        echo "$protocol|$pid|$ipportinode|$exefile" | awk '
            BEGIN{FS="|"}
            function iphex2dec(ipport){ 
                ret=sprintf("%d.%d.%d.%d:    %d","0x"substr(ipport,1,2),"0x"substr(ipport,3,2),
                "0x"substr(ipport,5,2),"0x"substr(ipport,7,2),"0x"substr(ipport,10,4)) ;
                if( ret == "0.0.0.0:0" ) #compatibility others awk versions 
                {
                    ret=        strtonum("0x"substr(ipport,1,2)) ;
                    ret=ret "." strtonum("0x"substr(ipport,3,2)) ;
                    ret=ret "." strtonum("0x"substr(ipport,5,2)) ;
                    ret=ret "." strtonum("0x"substr(ipport,7,2)) ;
                    ret=ret ":" strtonum("0x"substr(ipport,10)) ;
                }
                return ret ;
            }
            { 
            print $1" pid:"$2" local="iphex2dec($3)" remote="iphex2dec($4)" inode:"$5" exe=" $6 ;  
            }
            ' ; 
        #ls -l /proc/$pid/exe ; 
    done ; 
done

