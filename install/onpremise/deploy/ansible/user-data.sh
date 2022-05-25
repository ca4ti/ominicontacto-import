#!/bin/bash

RebrandValidation() {
  if [ $REPO_NAME == "ominicontacto" ];then
    Rebrand="false"
  else
    Rebrand="true"
  fi
}

UserValidation() {
  echo -e "\n"
  echo "##########################################################"
  echo "#         Welcome to OMniLeads deployment script         #"
  echo "##########################################################"
  echo ""
  WhoAamI="`whoami`"
  if [ "${WhoAamI}" == "root" ];then
  printf "$GREEN*** [OMniLeads] You have permission to run the script. Continuing. $NC\n"
  else
    printf "$RED*** [OMniLeads] You need to be root or have sudo permission to run this script. Exiting. $NC\n"
    exit 1
  fi
}

AnsibleExec() {

echo "******************** OML RELEASE = ${oml_app_release} ********************"

sleep 5

echo "******************** SELinux and firewalld disable ********************"

case ${oml_infras_stage} in
  onpremise)
    setenforce 0
    sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/sysconfig/selinux
    sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
    systemctl disable firewalld > /dev/null 2>&1
    systemctl stop firewalld > /dev/null 2>&1
    ;;
  *)
    echo " nothing "
    ;;
esac

echo "******************** yum update and install packages ********************"

case ${oml_infras_stage} in
  aws)
    yum remove -y python3 python3-pip
    yum install -y $SSM_AGENT_URL
    yum install -y patch libedit-devel libuuid-devel git podman
    amazon-linux-extras install -y epel
    amazon-linux-extras install python3 -y
    systemctl start amazon-ssm-agent
    ;;
  *)
    yum -y install git python3 python3-pip kernel-devel epel-release libselinux-python3 awscli podman
    ;;
esac

echo "******************** Ansible installation ********************"

pip3 install --upgrade pip
pip3 install boto3  'ansible==2.9.2'
export PATH="$HOME/.local/bin/:$PATH"

echo "******************** git clone omnileads repo ********************"

cd $SRC
git clone --recurse-submodules --branch ${oml_app_release} ${oml_app_repo_url}
cd ominicontacto
git submodule update --remote

echo "******************** inventory setting ********************"

sed -i "s/#localhost ansible/localhost ansible/g" $PATH_DEPLOY/inventory

# PGSQL edit inventory params **************************************************

if [[ "${oml_pgsql_cloud}"  == "true" ]];then
  sed -i "s/postgres_cloud=false/postgres_cloud=true/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_pgsql_db}"  != "NULL" ]];then
  sed -i "s/postgres_database=omnileads/postgres_database=${oml_pgsql_db}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_pgsql_user}"  != "NULL" ]];then
  sed -i "s/#postgres_user=omnileads/postgres_user=${oml_pgsql_user}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_pgsql_password}"  != "NULL" ]];then
  sed -i "s/#postgres_password=my_very_strong_pass/postgres_password=${oml_pgsql_password}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_pgsql_host}"  != "NULL" ]];then
  sed -i "s/#postgres_host=/postgres_host=${oml_pgsql_host}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_pgsql_port}"  != "NULL" ]];then
  sed -i "s/#postgres_port=/postgres_port=${oml_pgsql_port}/g" $PATH_DEPLOY/inventory
fi

# Asterisk ACD parameters *******

if [[ "${oml_ami_user}"  != "NULL" ]];then
  sed -i "s/#ami_user=omnileadsami/ami_user=${oml_ami_user}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_ami_password}"  != "NULL" ]];then
  sed -i "s/#ami_password=5_MeO_DMT/ami_password=${oml_ami_password}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_acd_host}"  != "NULL" ]];then
  sed -i "s/#asterisk_host=/asterisk_host=${oml_acd_host}/g" $PATH_DEPLOY/inventory
fi

# Wombat Dialer parameters *******

if [[ "${api_dialer_user}"  != "NULL" ]];then
  sed -i "s/#dialer_user=demoadmin/dialer_user=${api_dialer_user}/g" $PATH_DEPLOY/inventory
fi
if [[ "${api_dialer_password}"  != "NULL" ]];then
  sed -i "s/#dialer_password=demo/dialer_password=${api_dialer_password}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_dialer_host}" != "NULL" ]];then
  sed -i "s/#dialer_host=/dialer_host=${oml_dialer_host}/g" $PATH_DEPLOY/inventory
fi

# WebRTC kamailio & rtpengine params *******

if [[ "${oml_kamailio_host}"  != "NULL" ]];then
  sed -i "s/#kamailio_host=/kamailio_host=${oml_kamailio_host}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_rtpengine_host}" != "NULL" ]];then
  sed -i "s/#rtpengine_host=/rtpengine_host=${oml_rtpengine_host}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_extern_ip}" != "NULL" ]];then
  sed -i "s/#extern_ip=auto/extern_ip=${oml_extern_ip}/g" $PATH_DEPLOY/inventory
fi

# Redis, Nginx and Websockets params *******

if [[ "${oml_redis_host}" != "NULL" ]];then
  sed -i "s/#redis_host=/redis_host=${oml_redis_host}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_redis_ha}" == "true" ]];then
sed -i "s/redis_ha=false/redis_ha=true/g" $PATH_DEPLOY/inventory
sed -i "s/#sentinel_host_01=/sentinel_host_01=${oml_sentinel_host_01}/g" $PATH_DEPLOY/inventory
sed -i "s/#sentinel_host_02=/sentinel_host_02=${oml_sentinel_host_02}/g" $PATH_DEPLOY/inventory
sed -i "s/#sentinel_host_03=/sentinel_host_03=${oml_sentinel_host_03}/g" $PATH_DEPLOY/inventory
fi

if [[ "$NGINX_HOST" != "NULL" ]];then
  sed -i "s/#nginx_host=/nginx_host=$NGINX_HOST/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_websocket_host}" != "NULL" ]];then
  sed -i "s/#websocket_host=/websocket_host=${oml_websocket_host}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_websocket_port}" != "NULL" ]];then
  sed -i "s/#websocket_port=/websocket_port=${oml_websocket_port}/g" $PATH_DEPLOY/inventory
fi

# Others App params *******

sed -i "s%\#TZ=%TZ=${oml_tz}%g" $PATH_DEPLOY/inventory

if [[ "$${oml_app_sca}" != "NULL" ]];then
  sed -i "s/sca=3600/sca=${oml_app_sca}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_app_ecctl}" != "NULL" ]];then
  sed -i "s/sca=28800/sca=${oml_app_ecctl}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_app_login_fail_limit}" != "NULL" ]];then
  sed -i "s/LOGIN_FAILURE_LIMIT=10/LOGIN_FAILURE_LIMIT=${oml_app_login_fail_limit}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_app_reset_admin_pass}" == "true" ]];then
  sed -i "s/reset_admin_password=false/reset_admin_password=true/g" $PATH_DEPLOY/inventory
fi

if [[ "${oml_callrec_device}" != "NULL" ]];then
sed -i "s/callrec_device=local/callrec_device=${oml_callrec_device}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_backup_filename}" != "NULL" ]];then
sed -i "s%\#backup_file_name=%backup_file_name=${oml_backup_filename}%g" $PATH_DEPLOY/inventory
fi
if [[ "${s3_access_key}" != "NULL" ]];then
sed -i "s%\#s3_access_key=%s3_access_key=${s3_access_key}%g" $PATH_DEPLOY/inventory
fi
if [[ "${s3_secret_key}" != "NULL" ]];then
sed -i "s%\#s3_secret_key=%s3_secret_key=${s3_secret_key}%g" $PATH_DEPLOY/inventory
fi
if [[ "${s3_bucket_name}" != "NULL" ]];then
sed -i "s%\#s3_bucket_name=%s3_bucket_name=${s3_bucket_name}%g" $PATH_DEPLOY/inventory
fi
if [[ "${s3_endpoint_url}" != "NULL" ]];then
sed -i "s%\#s3url=%s3url=${s3_endpoint_url}%g" $PATH_DEPLOY/inventory
fi
if [[ "${s3_region}" != "NULL" ]];then
sed -i "s%\#s3_region=%s3_region=${s3_region}%g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_auto_restore}" != "NULL" ]];then
sed -i "s/auto_restore=false/auto_restore=${oml_auto_restore}/g" $PATH_DEPLOY/inventory
fi
if [[ "${oml_high_load}" != "NULL" ]];then
sed -i "s/high_load=false/high_load=${oml_high_load}/g" $PATH_DEPLOY/inventory
fi

if [[ "${oml_google_maps_api_key}" != "NULL" ]];then
sed -i "s%\#google_maps_api_key=%google_maps_api_key=${oml_google_maps_api_key}%g" $PATH_DEPLOY/inventory
sed -i "s%\#google_maps_center=%google_maps_center='${oml_google_maps_center}'%g" $PATH_DEPLOY/inventory
fi

echo "******************** omnileads.yml playbook execution ********************"
echo "******************** omnileads.yml playbook execution ********************"
echo "******************** omnileads.yml playbook execution ********************"

cd $PATH_DEPLOY
touch /var/tmp/oml_install

set -o allexport
source ".ansible_env"
set +o allexport

ansible-playbook omnileads.yml --extra-vars "iface=$oml_nic \
                  rebrand=$Rebrand \
                  oml_release=$(git branch | awk '{print $2}') \
                  commit=$(git rev-parse HEAD) \
                  build_date=\"$(env LC_hosts=C LC_TIME=C date)\"" -i inventory 
ResultadoAnsible=`echo $?`

if [ $ResultadoAnsible == 0 ];then
  echo "
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@////@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@/@@@@/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@/@/@////@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@/@@@/@@@/@@@@@@@/@@@@/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/@@@/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/@@@@@@@@@@@@@
  @@@@@@/@@@/@@@/@@@@@@@/@@@@/@@@@@@@//@@@@@/@@@///@@@@@&//@@@@@@@@@@@@@@@@/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@/@@@@@@@@@@@@@
  @@@@@@@@/@/@@@&/@@//@@@(@/@@@@@@@@/@@@@@@@@/@@////@@@@/@/@@@//@@@/@@@/@@@/@@@@@@@//@@@/@@@/@@@/@@@//@@@///@@/@@@/@@@@@@
  @@@@@@@@/@@/&//%//@/@//@@/@@@@@@@@/@@@@@@@@/%@//@//@@/@@/@@@/@@@@//@@/@@@/@@@@@@/@@@//@@@@@/////@/@@@@@@#/@@///@@@@@@@@
  @@@@@@@////@/@@////@@/@///@@@@@@@@//@@@@@@//@@//@@/@/@@@/@@@/@@@@//@@/@@@/@@@@@@///@@@@/@/@@@@@/@@/@@@@@//@@@@@@/@@@@@@
  @@@@@@/@@@//@//@@@@/@@/@@@@/@@@@@@@@//////@@@@//@@@/@@@@/@@@/@@@@//@@/@@@///////@@////@@@@////@/@@@/////@/@@/////@@@@@@
  @@@@@@/@@@//@@@@@@/@@@//@@/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@/@@@//@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@/@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@@&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                                          The Open Source Contact Center Solution
                                           Copyright (C) 2018 Freetech Solutions"
  echo ""
  echo "#############################################################"
  echo "#         OMniLeads installation ended successfully         #"
  echo "#############################################################"
  echo ""
  git checkout $current_directory/inventory
else
  echo ""
  echo "#######################################################################################"
  echo "#         OMniLeads installation failed. Check what happened and try it again         #"
  echo "#######################################################################################"
  echo ""
fi

}

RebrandValidation
UserValidation
AnsibleExec

