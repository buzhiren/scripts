#!/bin/bash
# function: all swoole process management
# Usage method: $0 action module

module=$1
action=$2
module_all="srv_laowang|srv_order|srv_api|srv_config"


Log(){
	local logtype=$1
	local loginfo=$2
	echo "[$(date +%F:%H:%M)] [$logtype] $loginfo" 
}

Init_var(){
	[[ ! $module =~ $module_all ]] \
		&& {
			Log Error "Usage: $0 {$module_all}" 
			exit 1
		}
    [[ ! $action =~ start|stop|restart|reload ]] \
        && {
            Log Error "Usage: $0 $module {start|stop|restart|reload}"
            exit 1
        }
    work_dir="/home/work/$module"
    start_cmd="/home/service/php7/bin/php $work_dir/smServer.php"
    reload_cmd='kill -USR1 $master_pid'
    stop_cmd='kill -TERM $master_pid'
    force_stop_cmd='kill -9 $pid_all'
	eval $(awk -F= '{ if($1=="worker_num")  print "worker_num="$2+2; else if($1=="port") print "port="$2 }' $work_dir/mouthSwoole.ini)
}

Check_var(){
	sleep 0.5
	eval $(netstat -tunlp|awk -vP="$port" -F "[ :/]+" 'NR>2 { if($5==P) printf("master_pid=%s; process=%s",$9,$10) }')
	if [[ -z "$process" && -z "$master_pid" ]];then
		process_num=0
		return 0
	fi
	process_num=$(ps aux|grep -i "$process"|grep -v grep|wc -l)
}

Start(){
	if [ $process_num -eq 0 ];then
		eval $start_cmd && Check_var && \
		[ $process_num -eq $worker_num ] && Log Info "$module start 正常 ." || Log Error "$module start 失败 ."
	elif [ $process_num -eq 34 ];then
		Log Info "$module 进程存在 ."
		exit 0
	else
		Log Error "$module 进程不正常, 强制重启中 ."
		pid_all=$(ps aux|grep -i "$process"|grep -v grep)
		eval $($force_stop_cmd) && eval $($start_cmd) && Check_var
		[ $process_num -eq $worker_num ] && Log Info "$module 强制重启正常 ." || Log Error "$module 强制重启失败, 请人工介入 !!!"
	fi
}

Stop(){
	if [ $process_num -eq $worker_num ];then
		eval $stop_cmd && Check_var
		[ $process_num -eq 0 ] && Log Info "$module stop 正常 ." || Log Info "$module stop 失败 ."
	elif [ $process_num -eq 0 ];then
		Log Info "$module 进程不存在 ."
	else
		Log Error "$module 进程不正常, 强制关闭中 ."
		pid_all=$(ps aux|grep -i "$process"|grep -v grep)
		eval $($force_stop_cmd) && Check_var
		[ $process_num -eq 0 ] && Log Info "$module 强制关闭正常 ." || Log Error "$module 强制关闭失败, 请人工介入 !!!"
	fi
}

Restart(){
	Stop 
	Check_var
	Start
}

Reload(){
	if [ $process_num -eq 34 ];then
		old_time=$(ps aux|grep -i "$process"|grep -Eiv "Master|Manager|grep"|awk 'NR==2 {print $9}')
		eval $($reload_cmd) \
			&& Check_var \
			&& new_time=$(ps aux|grep -i "$process"|grep -Eiv "Master|Manager|grep"|awk 'NR==2 {print $9}')
		if [ $process_num -eq $worker_num -a "$pid_old_time" != "$new_time"  ] ;then 
			Log Info "$module reload 正常 ."
		elif [ "$pid_old_time" == "$new_time"  ]; then
			Log Erro "$module work进程时间未重载, 强制重启中 ."
			Restart
		else
			Log Error "$module reload 进程不正常, 强制重启中  ."
			Restart
		fi
	elif [ $process_num -eq 0 ];then
		Log Info "swoole 进程不存在, 启动中."
		Start
	else
		Log Error "swoole 进程不正常, 强制重启中  ."
		Restart
	fi
}

Main(){
	Init_var
	Check_var
	case $action in
		start)
			Start
			;;
		stop)
			Stop
			;;
		restart)
			Restart
			;;
		reload)
			Reload
			;;
		status)
			Stauts
			;;
		*)
		   Log Error "unknown error ."
			;;
	esac
}

Main
