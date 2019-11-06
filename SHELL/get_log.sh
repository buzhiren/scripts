#!/usr/bin/env bash

#!/bin/bash

source /etc/profile

time=$(date +%F)
ftp_ip="59.110.44.143"
base_path=$(cd $(dirname $0);pwd)
buss_dir="/mnt/business"
type=$(awk -F"|" '{print $2}' $base_path/log_type.txt)
project="xx|172.16.0.100 xx|172.16.0.91"


Log(){
        local log_type=$1
        local log_info=$2
        local times=$(date +%F-%H:%M:%S)
        echo -e "[ $times ] [ $log_type ] [ $log_info ]"
}

Op_thread(){
    local operation=$1
    local thread_file=$2
    local thread_num=$3
    case $operation in
        init)
            rm -rf $thread_file
            mkfifo $thread_file
            exec 9<>$thread_file
            for num in $(seq $thread_num);do
                echo " " 1>&9
            done
            ;;
        insert)
            echo " " 1>&9
            ;;
        delete)
            read -u 9
            ;;
        close)
            exec 9<&-
            ;;
    esac
}


Arg(){
    while getopts s:e: opt;do
        case "$opt" in
            s)
                start_time="$OPTARG"
                ;;
            e)
                end_time="$OPTARG"
                ;;
            ?)
                echo "Usage: args [-s] [-e]"
                exit 1
        esac
    done
}


Begin(){
    local sn=$1
    local rip=$2
    local remote_file="${buss_dir}/${type}/${type}-${time}.log"
    local source_file="${base_path}/tmp_file/${sn}_${type}-${time}.log"

    rsync -avz -e "ssh -p 53306" root@${rip}:${remote_file} ${source_file}
    [ ! -f ${source_file} ] \
        && {
            Log ERROR " File Non Existent !!!"
            exit 4
            }
}

File_generate(){
    local sn=$1
    local download="/home/ftpuser/Download"

    cd ${base_path}/tmp_file/
    sed -nr "/${start_time}:[0-9]{1,2}:[0-9]{1,2}/,/${end_time}:[0-9]{1,2}:[0-9]{1,2}/p"  ${sn}_${type}-${time}.log \
    |awk -F "\t" '{if($31==0) print $0}' > ./download/${sn}_${type}-${time}.log
    [ $? -ne 0 ] && exit 4
    rsync -avz -e "ssh -p 53306" ${base_path}/tmp_file/download/${sn}_${type}-${time}.log \
    root@:${ftp_ip}:${download}/${type}/
    [ $? -eq 0 ] && Log INFO "File Generate Done." || exit 4
}


End(){
    cd ${base_path}/tmp_file/ && find ./ -type f -name "*log" -exec rm -fr {} \;
    Log INFO "Success, Succes, Allow Download ."
}


Main(){
    Arg $@
    Op_thread init $base_path/tmp.pipe 6
        for srv in $project;do
        Op_thread delete
        {

            srv_name=$(echo $pro_info|awk -F"|" '{print $1}')
            ip=$(echo $pro_info|awk -F"|" '{print $2}')
            Begin "$srv_name" "$ip"
            File_generate "$srv_name"
            End

            Op_thread insert
        }&
        done
        wait
        Op_thread close
}

Main $@
