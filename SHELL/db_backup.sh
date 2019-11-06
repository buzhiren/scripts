#!/bin/bash


source /etc/profile
source /etc/bashrc
ip=$1
port=$2
backup_path=$3
ncport=$4
passwd=$5
back_ip=$(ifconfig eth0 | grep "inet addr" |awk -F : '{print $2}'|awk '{print $1}')
time=$(date  +'%Y%m%d')

Log(){
	logfile=/data/tmp_trade/${0}.log
	local logtype=$1
	local loginfo=$2
	echo "[$(date +%F:%H:%M)] $logtype $loginfo" >> $logfile
}


Slave_info(){
	slave_path=$(mysql -h$ip -P${port} -utest -p123456 -e "show global variables like '%datadir%'"|awk 'NR==2 {print $2}') > /dev/null 2>&1
	master_host=$(mysql -h$ip -P${port} -utest -p123456 -e "show slave status\G"|grep -i master_host|awk -F : '{print $2}')
	master_port=$(mysql -h$ip -P${port} -utest -p123456 -e "show slave status\G"|grep -i master_port|awk -F : '{print $2}')
	Log info "$slave_path  $master_host  $master_port"
	if [ ${#slave_path} == 0 ]; then
    	echo "can't find datadir"
    	exit 1
	fi
}

Nc_init(){
	ncpid=$(netstat -tunlp|grep $ncport|awk -F "[ /]+" '{print $(NF-2)}')
	kill -9 $ncpid
}

Backup_port(){
	mkdir -p $backup_path/$time && cd $backup_path/$time && nc -d -l $ncport | tar -xif - > /dev/null 2>&1 &
	[ $? -eq 0 ] && Log info " backup $ncport port start ! "
}

Innobackupex_start(){
	Log info "Innobackupex db backup start . "
	ssh  $ip "innobackupex --defaults-file=$slave_path/my$port.cnf --user=root --password=${passwd} --host=127.0.0.1 --stream=tar --slave-info $backup_path/$time| nc $back_ip $ncport" 
	[ $? -eq 0 ] && \
		{
			Log info "Innobackupex db backup success . "
		} || \
		{
			Log info "Innobackupex db backup fail . "
			exit 1
		}
}

App_log(){
	Log info "app_log backup start . "
	innobackupex --user=root --password=${passwd} --apply-log $backup_path/$time --ibbackup=/usr/bin/xtrabackup_56 --use-memory=1G
	[ $? -eq 0 ] && \
		{
			Log info " app_log  success . "
		} || \
		{
			Log info "app_log fail . "
			exit 2
		}
}


Connection_point(){
	if [ ${#master_host} == 0 ];then
    	master_log_file=''
    	master_log_pos=0
	else
    	master_log_file=$(cd $backup_path/$time && cat xtrabackup_slave_info|awk -F = '{print $2}'|awk -F , '{print $1}'|sed s/\'//g)
    	master_log_pos=$(cd $backup_path/$time && cat xtrabackup_slave_info|awk -F = '{print $3}')
		log_file=$(cd $backup_path/$time && cat xtrabackup_binlog_pos_innodb|awk '{print $1}'|awk -F / '{print $2}')
		log_pos=$(cd $backup_path/$time && cat xtrabackup_binlog_pos_innodb|awk '{print $2}')
		cd $backup_path && echo "echo \"change master to master_host='${master_host}',master_user='dvdrep',master_password='Dvd@17xtuxTSaIpo',master_log_file='${master_log_file}',master_log_pos=${master_log_pos},master_port=${master_port}\"|mysql -h127.0.0.1 -uroot -p -P${master_port}" > start_master.sh && \
		Log info "日志文件连接点生成 ."
	fi
}


Main(){
	Slave_info
	Nc_init
	Backup_port
	Innobackupex_start
	App_log
	Connection_point
}

Main
