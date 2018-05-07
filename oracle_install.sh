#!/bin/sh
MOUNTDIR=/dev/cdrom #光盘路径/
MOUNTPOINT=/mnt/cdrom/ #光盘挂载路径#
RPM=/mnt/cdrom/Packages/
#ERRORLOG=/tmp/ERROR_$(date +"%Y-%m-%d").log
log="/tmp/install_software_$(date +"%Y-%m-%d").log"  #操作日志存放路径
fsize=2000000
exec 1>>$log  #操作日志信息均输出到日志文件
loglevel=0 #debug:0; INFO:1; WARNINGINGINGING:2; ERROR:3 #日志级别
log=$0".log"
function log {
#localtext;locallogtype
# logfile="/tmp/install_software_$(date +"%Y-%m-%d").log"
  logtype=$1
  text=$2
  now_time='['$(date +"%Y-%m-%d %H:%M:%S")']'
  case $logtype in
    ERROR)
      echo -e "\033[31m$now_time [$1]$2\033[0m" | tee -a $logfile;;
    INFO)
      echo -e "\033[37m$now_time [$1]$2\033[0m" | tee -a $logfile;;
    WARNING)
      echo -e "\033[37m$now_time [$1]$2\033[0m" | tee -a $logfile;;
  esac
}

sleep 1
INFO() {
    log INFO " Start trying to mount a CD-ROM ..."
}
INFO
sleep 1
#检测光盘挂载路径是否存在
if [ -d $MOUNTPOINT ]; then
     INFO() {
     log INFO " Folder $MOUNTPOINT already exists!"
     }
     INFO
else
     WARNING() {
     log WARNING " Folder $MOUNTPOINT does not exist!"
     }
     WARNING
     mkdir $MOUNTPOINT #创建路径
     sleep 2
     INFO() {
        log INFO " Folder $MOUNTPOINT creation completed!"
     }
     INFO
fi
sleep 2
#yum源设置
file=/etc/yum.repos.d/CentOS-Base.repo

if [ ! -f "$file" ]; then
     WARNING() {
        log WARNING " File $file does not exist! Continue"
     }
     WARNING
else
  mv $file /etc/yum.repos.d/CentOS-Base.repo.bak
     WARNING() {
        log WARNING " File $file move completed!"
     }
     WARNING

fi

file1=/etc/yum.repos.d/CentOS-Media.repo

if [ ! -f "$file1" ]; then
     WARNING() {
        log WARNING " File $file1 does not exist! Quit!"
     }
     WARNING
else
     sed -i -e 's|enabled=0|enabled=1|' $file1
     sed -i -e "s|baseurl=file:///media/CentOS/|baseurl=file://$MOUNTPOINT|" $file1

fi

if  grep -q enabled=1 $file1 ; then
     INFO() {
        log INFO " Repo [enabled] set up completed!"
     }
     INFO
else
     ERROR() {
        log ERROR " Repo [enabled] setting failure,Now exit procedure!"
     }
     ERROR
    exit
fi
sleep 2
if  grep -q baseurl=file:///mnt/cdrom $file1 ; then
     INFO() {
        log INFO " Repo [baseurl] set up completed!"
     }
     INFO
else
     ERROR() {
        log ERROR " Repo [baseurl] setting failure,Now exit procedure!"
     }
     ERROR
    exit
fi
INFO() {
        log INFO " Repo set completed! Continue!"
     }
INFO
sleep 2
#挂载光盘镜像
mount -o loop $MOUNTDIR  $MOUNTPOINT &>  /dev/null

if [ -d $RPM ]; then
     INFO() {
        log INFO " CD-ROM mount completed!"
     }
     INFO
else
     ERROR() {
        log ERROR " time:`date` ERR: CD-ROM Mount Fail"
     }
     ERROR
     exit
fi

sleep 2

service iptables stop
chkconfig iptables off

INFO() {
        log INFO " Closing the Linux firewall successfully"
     }
INFO
sleep 2


INFO() {
        log INFO " Start detecting the installation of RPM packages ..."
     }
INFO
sleep 2
yum -y install binutils compat-libstdc++-33 elfutils-libelf elfutils-libelf-devel glibc glibc-common glibc-devel gcc gcc-c++ libaio libaio-devel libgcc libstdc++ libstdc++-devel make sysstat unixODBC unixODBC-devel pdksh compat-db control-center libstdc++ libstdc++-devel xscreensaver openmotif21 ksh* compat-libcap* zip unzip &>  /dev/null

packagecheck()
{
for package in binutils compat-libcap1 compat-libstdc++ gcc gcc-c++ glibc glibc-devel ksh libgcc libstdc++ libstdc++-devel libaio libaio-devel make sysstat
do
rpm -q $package
if [ $? != 0 ];then
yum -y install $package &>  /dev/null
        INFO() {
            log INFO " RPM package installation completed"
        }
        INFO
sleep 2
else
        ERROR() {
           log ERROR " RPM package Installation failure!"
        }
        ERROR
        exit
fi
done
}

INFO() {
        log INFO " Start creating Oracle Users | Groups | Directories"
     }
INFO
sleep 2

if  grep -q oinstall:x:501: /etc/group ; then
     INFO() {
        log INFO " Oracle Group oinstall already creation completed!"
     }
     INFO
else
     /usr/sbin/groupadd -g 501 oinstall &>  /dev/null
fi
sleep 2

if  grep -q dba:x:502: /etc/group ; then
     INFO() {
        log INFO " Oracle Group dba already creation completed!"
     }
     INFO
else
     /usr/sbin/groupadd -g 502 dba &>  /dev/null
fi
sleep 2

if  grep -q oracle /etc/shadow ; then

     INFO() {
        log INFO " Oracle User oracle already creation completed!"
     }
     INFO
else
     /usr/sbin/useradd -g oinstall -G dba oracle &>  /dev/null
fi
sleep 2

if  grep -q oinstall:x:501: /etc/group && grep -q dba:x:502: /etc/group && grep -q oracle /etc/shadow ; then

sleep 2
else
      ERROR() {
        log INFO " Oracle users | groups | directories creating failure! "
     }
     ERROR
EXIT
fi
sleep 2

DBHOME=/u01/app/oracle
DBHOME1=/u01/app/oradata
DBHOME2=/u01/app/oraInventory

if [ ! -d $DBHOME ]&&[! -d $DBHOME1 ]&& [! -d $DBHOME2 ]; then
     ERROR() {
        log ERROR " ORACLE Folder Create Failed! Now exit procedure "
     }
     ERROR
     exit
else
      INFO() {
        mkdir -p $DBHOME
        mkdir -p $DBHOME1
        mkdir -p $DBHOME2
        chown -R oracle:oinstall /u01/app/oracle/ /u01/app/oradata/ /u01/app/oraInventory
        chmod -R 755 /u01/app/oracle/ /u01/app/oradata/ /u01/app/oraInventory
        log INFO " ORACLE Folder Create Completed! "
     }
     INFO

fi
sleep 2

echo "oracle" | passwd --stdin oracle &>  /dev/null
     INFO() {
        log INFO " ORACLE USER Password Create Completed!"
     }
     INFO
sed -i /::/d /etc/hosts
sleep 2
INFO() {
        log INFO " Create ORACLE user | group | directory completion"
     }
INFO

sleep 2
if  grep -q oracle /etc/security/limits.conf ; then
     WARNING() {
        log WARNING " File [/etc/security/limits.conf] already set successfully!"
     }
     WARNING
else
    echo "#ORACLE SETTING                           " >> /etc/security/limits.conf
    echo "oracle               soft    nproc   2047 " >> /etc/security/limits.conf
    echo "oracle               hard    nproc   16384" >> /etc/security/limits.conf
    echo "oracle               soft    nofile  1024 " >> /etc/security/limits.conf
    echo "oracle               hard    nofile  65536" >> /etc/security/limits.conf
     INFO() {
        log INFO " File [/etc/security/limits.conf] set completed!"
     }
     INFO


fi
sleep 2

if  grep -q  fs.aio-max-nr /etc/sysctl.conf ; then
     WARNING() {
        log WARNING " File [/etc/sysctl.conf] already set successfully!"
     }
     WARNING
else
    sed -i /kernel.shmmax/d /etc/sysctl.conf
    sed -i /kernel.shmall/d /etc/sysctl.conf
    echo "#ORACLE SETTING                          " >> /etc/sysctl.conf
    echo "fs.aio-max-nr = 1048576                  " >> /etc/sysctl.conf
    echo "fs.file-max = 6815744                    " >> /etc/sysctl.conf
    echo "kernel.shmall = 2097152                  " >> /etc/sysctl.conf
    echo "kernel.shmmax = 12884901888              " >> /etc/sysctl.conf
    echo "kernel.shmmni = 4096                     " >> /etc/sysctl.conf
    echo "kernel.sem = 250 32000 100 128           " >> /etc/sysctl.conf
    echo "net.ipv4.ip_local_port_range = 9000 65500" >> /etc/sysctl.conf
    echo "net.core.rmem_default = 262144           " >> /etc/sysctl.conf
    echo "net.core.rmem_max = 4194304              " >> /etc/sysctl.conf
    echo "net.core.wmem_default = 262144           " >> /etc/sysctl.conf
    echo "net.core.wmem_max = 1048586              " >> /etc/sysctl.conf
    sysctl -p &>  /dev/null
     INFO() {
        log INFO " File [/etc/sysctl.conf] set completed!"
     }
     INFO
fi
sleep 2

if  grep -q oracle /etc/profile; then
     WARNING() {
        log WARNING " File [/etc/profile] already set successfully!"
     }
     WARNING

else
    echo "if [ $USER = "oracle" ]; then
        if [ $SHELL = "/bin/ksh" ]; then
              ulimit -p 16384
              ulimit -n 65536
        else
              ulimit -u 16384 -n 65536
        fi
    fi
    ">> /etc/profile
     INFO() {
        log INFO " File [/etc/profile] set set completed!"
     }
     INFO
fi
sleep 2

if  grep -q oracle /home/oracle/.bash_profile; then
     WARNING() {
        log WARNING " File [/home/oracle/.bash_profile] already set successfully!"
     }
     WARNING

else
     echo "PATH=\$PATH:\$ORACLE_HOME/bin                                                       " >> /home/oracle/.bash_profile
     echo "export PATH                                                                " >> /home/oracle/.bash_profile
     echo "umask 022                                                                  " >> /home/oracle/.bash_profile
     echo "ORACLE_BASE=/u01/app/oracle                                                " >> /home/oracle/.bash_profile
     echo "ORACLE_SID=orcl                                                            " >> /home/oracle/.bash_profile
     echo "ORACLE_HOME=/u01/app/oracle/product/11.2.0/dbhome_1                        " >> /home/oracle/.bash_profile
     echo "PATH=\$ORACLE_HOME/bin/:\$PATH                                               " >> /home/oracle/.bash_profile
     echo "LANG=en_US.UTF-8                                                           " >> /home/oracle/.bash_profile
     echo "export ORACLE_BASE ORACLE_HOME ORACLE_SID                                  " >> /home/oracle/.bash_profile
     source /home/oracle/.bash_profile
     INFO() {
        log INFO " File [/home/oracle/.bash_profile] set completed!"
     }
     INFO
fi
sleep 1

INFO() {
        log INFO " The environment variable is configured,Now start unpacking the installation package"
     }
INFO
sleep 2

# unzip
# unzip
chmod 777 /tools
chown oracle:dba /tools -R

file1=p13390677_112040_Linux-x86-64_1of7.zip
file2=p13390677_112040_Linux-x86-64_2of7.zip

if [ -d /tools/database ]
then
rm -rf /tools/database
fi

if [ -f /tools/$file1 ]
then
  ls /tools/$file1 &>  /dev/null
  unzip /tools/$file1 -d /tools &>  /dev/null
fi

if [ -f /tools/$file2 ]
then
  ls /tools/$file2 &>  /dev/null
  unzip /tools/$file2 -d /tools &>  /dev/null
fi
INFO() {
        log INFO " The ORACLE installation package is unzip"
     }
INFO
sleep 2
##################################################
# parameter files
##################################################

# create install_db.rsp

install=`sed -n '/oracle.install.option/p' /tools/database/response/db_install.rsp` &>  /dev/null
hostname=`sed -n '/ORACLE_HOSTNAME/p' /tools/database/response/db_install.rsp` &>  /dev/null
group_name=`sed -n '/UNIX_GROUP_NAME/p' /tools/database/response/db_install.rsp` &>  /dev/null
inventory=`sed -n '/INVENTORY_LOCATION/p' /tools/database/response/db_install.rsp` &>  /dev/null
languages=`sed -n '/^SELECTED_LANGUAGES=en$/p' /tools/database/response/db_install.rsp` &>  /dev/null
oracle_home=`sed -n '/ORACLE_HOME/p' /tools/database/response/db_install.rsp` &>  /dev/null
oracle_base=`sed -n '/ORACLE_BASE/p' /tools/database/response/db_install.rsp` &>  /dev/null
InstallEdition=`sed -n '/oracle.install.db.InstallEdition/p' /tools/database/response/db_install.rsp` &>  /dev/null
dba_group=`sed -n '/oracle.install.db.DBA_GROUP/p' /tools/database/response/db_install.rsp` &>  /dev/null
oper_group=`sed -n '/oracle.install.db.OPER_GROUP/p' /tools/database/response/db_install.rsp` &>  /dev/null
updates=`sed -n '/^DECLINE_SECURITY_UPDATES=$/p' /tools/database/response/db_install.rsp` &>  /dev/null
hostname1=`sed -n '/HOSTNAME/p' /etc/sysconfig/network| sed -s "s/=/ /g"|gawk '{print $2}'` &>  /dev/null


if [ "$install" = "oracle.install.option=" ]
 then
   sed -i "s/oracle.install.option=/oracle.install.option=INSTALL_DB_SWONLY/g" /tools/database/response/db_install.rsp &>  /dev/null
   INFO() {
        log INFO " INSTALL $install  update succeeful!"
     }
   INFO
 else
   ERROR() {
        log ERROR " INSTALL $install parameter don't update!"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$hostname" = "ORACLE_HOSTNAME=" ]
 then
 sed -i "s/ORACLE_HOSTNAME=/ORACLE_HOSTNAME=$hostname1/g" /tools/database/response/db_install.rsp &>  /dev/null
     INFO() {
        log INFO " HOSTNAME $hostname update succeeful!"
     }
   INFO
 else
   ERROR() {
        log ERROR " HOSTNAME $hostname parameter don't update!"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$group_name" = "UNIX_GROUP_NAME=" ]
 then
  sed -i "s/UNIX_GROUP_NAME=/UNIX_GROUP_NAME=dba/g" /tools/database/response/db_install.rsp &>  /dev/null
   INFO() {
        log INFO " GROUP_NAME $group_name update succeeful!"
     }
   INFO
 else
   ERROR() {
        log ERROR " GROUP_NAME $group_name parameter don't update!"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$inventory" = "INVENTORY_LOCATION=" ]
 then
  sed -i "s/INVENTORY_LOCATION=/INVENTORY_LOCATION=\/u01\/app\/oraInventory/g" /tools/database/response/db_install.rsp &>  /dev/null
    INFO() {
        log INFO " INVENTORY $inventory update succeeful!"
     }
   INFO
 else
      ERROR() {
        log ERROR " INVENTORY $inventory parameter don't update!"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$languages" = "SELECTED_LANGUAGES=en" ]
 then
  sed -i "s/SELECTED_LANGUAGES=en/SELECTED_LANGUAGES=en,zh_CN/g" /tools/database/response/db_install.rsp &>  /dev/null
      INFO() {
        log INFO " LANGUAGES $languages update succeeful!"
     }
   INFO
 else
   ERROR() {
        log ERROR " LANGUAGES $languages parameter don't update!"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$oracle_home" = "ORACLE_HOME=" ]
 then
 sed -i "s/ORACLE_HOME=/ORACLE_HOME=\/u01\/app\/oracle\/product\/11.2.0\/dbhome_1/g" /tools/database/response/db_install.rsp &>  /dev/null
   INFO() {
        log INFO " ORACLE_HOME $oracle_home update succeeful!"
     }
   INFO
 else
   ERROR() {
        log ERROR " ORACLE_HOME $oracle_home parameter don't update!"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$oracle_base" = "ORACLE_BASE=" ]
 then
  sed -i "s/ORACLE_BASE=/ORACLE_BASE=\/u01\/app\/oracle/g" /tools/database/response/db_install.rsp &>  /dev/null
   INFO() {
        log INFO " ORACLE_BASE $oracle_base update succeeful!"
     }
   INFO
 else
   ERROR() {
        log ERROR " ORACLE_BASE $oracle_base parameter don't update!"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$InstallEdition" = "oracle.install.db.InstallEdition=" ]
 then
  sed -i "s/oracle.install.db.InstallEdition=/oracle.install.db.InstallEdition=EE/g" /tools/database/response/db_install.rsp &>  /dev/null
   INFO() {
        log INFO " InstallEdition $InstallEdition update succeeful!"
     }
   INFO
 else
   ERROR() {
        log ERROR " InstallEdition $InstallEdition parameter don't update!"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$dba_group" = "oracle.install.db.DBA_GROUP=" ]
 then
   sed -i "s/oracle.install.db.DBA_GROUP=/oracle.install.db.DBA_GROUP=dba/g" /tools/database/response/db_install.rsp &>  /dev/null
   INFO() {
        log INFO " DBA_GROUP $dba_group update succeeful!"
     }
   INFO
 else
   ERROR() {
        log ERROR " DBA_GROUP $dba_group parameter don't update!"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$oper_group" = "oracle.install.db.OPER_GROUP=" ]
 then
  sed -i "s/oracle.install.db.OPER_GROUP=/oracle.install.db.OPER_GROUP=dba/g" /tools/database/response/db_install.rsp &>  /dev/null
   INFO() {
        log INFO " OPER_GROUP $oper_group update succeeful!"
     }
   INFO
 else
   ERROR() {
        log ERROR " OPER_GROUP $oper_group parameter don't update!"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$updates" = "DECLINE_SECURITY_UPDATES=" ]
 then
  sed -i "s/DECLINE_SECURITY_UPDATES=/DECLINE_SECURITY_UPDATES=true/g" /tools/database/response/db_install.rsp &>  /dev/null
      INFO() {
        log INFO " UPDATES $updates update succeeful!"
     }
   INFO
 else
   ERROR() {
        log ERROR " UPDATES $updates parameter don't update!"
     }
   ERROR
   EXIT
fi
sleep 2
#create dbca.rsp

gdbname1=`sed -n '/GDBNAME = "orcl11g.us.oracle.com"/p' /tools/database/response/dbca.rsp` &>  /dev/null
sid1=`sed -n '/SID = "orcl11g"/p' /tools/database/response/dbca.rsp` &>  /dev/null
oradata=`sed -n '/DATAFILEDESTINATION =/p' /tools/database/response/dbca.rsp` &>  /dev/null
flash=`sed -n '/RECOVERYAREADESTINATION=/p' /tools/database/response/dbca.rsp` &>  /dev/null
charset=`sed -n '/CHARACTERSET =/p' /tools/database/response/dbca.rsp` &>  /dev/null
ncharset=`sed -n '/NATIONALCHARACTERSET=/p' /tools/database/response/dbca.rsp` &>  /dev/null


if [ "$gdbname1" = "GDBNAME = \"orcl11g.us.oracle.com\"" ]
then
sed -i "s/GDBNAME = \"orcl11g.us.oracle.com\"/GDBNAME = \"orcl\"/g" /tools/database/response/dbca.rsp &>  /dev/null
      INFO() {
        log INFO " GDBNAME1 $gdbname1 update succeeful!"
     }
   INFO
else
   ERROR() {
        log ERROR " GDBNAME1 $gdbname1 not update"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$sid1" = "SID = \"orcl11g\"" ]
then
   sed -i "s/SID = \"orcl11g\"/SID = \"orcl\"/g" /tools/database/response/dbca.rsp &>  /dev/null
         INFO() {
        log INFO " SID1 $sid1 update succeeful!"
     }
   INFO
else
   ERROR() {
        log ERROR " SID1 $sid1 not update"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$oradata" = "#DATAFILEDESTINATION =" ]
then
   sed -i "s/#DATAFILEDESTINATION =/DATAFILEDESTINATION = \"\/oradata\"/g" /tools/database/response/dbca.rsp &>  /dev/null
            INFO() {
        log INFO " ORADATA $oradata update succeeful!"
     }
   INFO
else
   ERROR() {
        log ERROR " ORADATA $oradata not update"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$flash" = "#RECOVERYAREADESTINATION=" ]
then
 sed -i "s/#RECOVERYAREADESTINATION=/RECOVERYAREADESTINATION= \"\/u01\/app\/oracle\/flash_recovery_area\"/g" /tools/database/response/dbca.rsp &>  /dev/null
 INFO() {
        log INFO " FLASH $flash update succeeful!"
     }
   INFO
else
   ERROR() {
        log ERROR "FLASH $flash not update!"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$charset" = "#CHARACTERSET = \"US7ASCII\"" ]
then
  sed -i "s/#CHARACTERSET = \"US7ASCII\"/CHARACTERSET = \"AL32UTF8\"/g" /tools/database/response/dbca.rsp &>  /dev/null
   INFO() {
        log INFO " CHARSET $charset update succeeful!"
     }
   INFO
else
   ERROR() {
        log ERROR " CHARSET $charset not update!"
     }
   ERROR
   EXIT
fi
sleep 2
if [ "$ncharset" = "#NATIONALCHARACTERSET= \"UTF8\"" ]
then
sed -i "s/#NATIONALCHARACTERSET= \"UTF8\"/NATIONALCHARACTERSET = \"UTF8\"/g" /tools/database/response/dbca.rsp &>  /dev/null
   INFO() {
        log INFO " NCHARSET $ncharset update succeeful!"
     }
   INFO
else
   ERROR() {
        log ERROR " NCHARSET $ncharset is not update!"
     }
   ERROR
   EXIT
fi
chmod 777 /tools

# netca.rsp

## 注意： 以下命令可单独执行，因为软件装完需要执行脚本 ##
#install
INFO() {
        log INFO " Starting Oracle Universal Installer... Please wait ..."
     }
INFO
sleep 2

su - oracle <<EOF
cd /tools/database/
./runInstaller -silent -responseFile /tools/database/response/db_install.rsp
sleep 300
cd /tools/database/install/
netca -silent -responsefile /tools/database/response/netca.rsp
sleep 60
cd /tools/database/install/
dbca -silent -createDatabase -templateName General_Purpose.dbc -gdbName orcl -sysPassword oracle -systemPassword oracle
EOF
