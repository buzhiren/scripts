#!/bin/bash


time=$(date +%F-%H:%M)
base_path=$(cd $(dirname $0);pwd)


Debug(){
    local info=$1
    [[ $info == "true" ]] && set -x
    [[ $info == "false" ]] && return
}


Log(){
  local log_type=$1
  local log_info=$2
  local times=$(date +%F-%H:%M:%S)
  echo -e "[$times] [$log_type] [$log_info]"
}

Arg(){
    while getopts a:v:j:p:h:e: opt;do
        case "$opt" in
            a)
                action="$OPTARG"
                ;;
            v)
                version="$OPTARG"
                ;;
            j)
                job_base_name="$OPTARG"
                ;;
            p)
                project="$OPTARG"
                ;;
            h)
                hostname="$OPTARG"
                ;;
            e)
                env="$OPTARG"
                ;;
            ?)
                echo "Usage: args [-a] [-v] [-j] [-p] [-h] [-e]"
                exit 1
        esac
    done

}

Arg_comm(){
    [[ ! "$action" =~ deploy|rollback ]] \
        && {
            Log ERROR "-a Parameter error ! ! !"
            exit
        }
    [[ ! "$env" =~ beta|prod ]] \
        && {
            Log ERROR "-e Parameter error ! ! !"
            exit
        }
    [[ "$env" == "beta" ]] && return
    [ ! -n "$srv_ip" ] \
        && {
                Log ERROR "srv_ip problem ! ! !"
                exit
        }
    [ ! -n "$ngx_ip" ] \
        && {
                Log ERROR "ngx_ip problem ! ! !"
                exit
        }
}

End(){


}


Main(){

        Arg $@
        Arg_comm
        case "$action" in
                pass)
                        pass
                        ;;
                pass)
                        pass
                        ;;
                *)
                        Log ERROR "unknown error ! ! !"
                esac
        End

}

Main
