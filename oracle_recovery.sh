#!/bin/bash
myVar=/home/oracle/bin/rman_cmd
mysql=/home/oracle/bin/sql_cmd.sql
myora=/home/oracle/bin/ora_cmd.sql
log=/backup_rman/log/rman_full_`date +%Y%m%d%H`.log
#创建备份目录
cd /backup_rman
mkdir bak_`date +%Y%m%d%H`
chown oracle:oinstall bak_`date +%Y%m%d%H`
chmod 755 bak_`date +%Y%m%d%H`
echo "Recovery bak_`date +%Y%m%d%H` suess" >> $log
sleep 10
#创建备份程序 rman_cmd
if [ ! -f "$myVar" ]; then
 touch $myVar
 chown oracle:oinstall $myVar
 chmod 755 $myVar
 echo "create rmn_cmd uess" >> $log
fi
sleep 10
if [ ! -f "$mysql" ]; then
 touch $mysql
 chown oracle:oinstall $mysql
 chmod 755 $mysql
 echo "create sql_cmd uess" >> $log
fi
sleep 10
if [ ! -f "$myora" ]; then
 touch $myora
 chown oracle:oinstall $myora
 chmod 755 $myora
 echo "create ora_cmd uess" >> $log
fi
sleep 10
############
echo " shutdown immediate; "            >>/home/oracle/bin/sql_cmd.sql
echo " startup mount; "                 >>/home/oracle/bin/sql_cmd.sql
echo " alter database archivelog; "     >>/home/oracle/bin/sql_cmd.sql
echo " exit "                           >>/home/oracle/bin/sql_cmd.sql
############
echo " shutdown immediate; "            >>/home/oracle/bin/ora_cmd.sql
echo " startup  mount; "                >>/home/oracle/bin/ora_cmd.sql
echo " alter database noarchivelog; "   >>/home/oracle/bin/ora_cmd.sql
echo " alter database open; "           >>/home/oracle/bin/ora_cmd.sql
echo " exit "                           >>/home/oracle/bin/ora_cmd.sql
#编辑备份程序 rman_cmd
echo " crosscheck archivelog all;                          "                                                                          >>/home/oracle/bin/rman_cmd
echo " delete noprompt expired archivelog all;  "                                                                                     >>/home/oracle/bin/rman_cmd
echo " run {  "                                                                                                                       >>/home/oracle/bin/rman_cmd
echo "         configure retention policy to recovery window of 4 days; "                                                             >>/home/oracle/bin/rman_cmd
echo "         configure controlfile autobackup off; "                                                                                >>/home/oracle/bin/rman_cmd
echo "         allocate channel c1 device type disk  format '/backup_rman/bak_`date +%Y%m%d%H`/rman_full_%T_%U'  maxpiecesize=3G; " >>/home/oracle/bin/rman_cmd
echo "         allocate channel c2 device type disk  format '/backup_rman/bak_`date +%Y%m%d%H`/rman_full_%T_%U'  maxpiecesize=3G; " >>/home/oracle/bin/rman_cmd
echo "         allocate channel c3 device type disk  format '/backup_rman/bak_`date +%Y%m%d%H`/rman_full_%T_%U'  maxpiecesize=3G; " >>/home/oracle/bin/rman_cmd
echo "         backup as compressed backupset full database format '/backup_rman/bak_`date +%Y%m%d%H`/full_bk1_%u%p%s.rmn'; "       >>/home/oracle/bin/rman_cmd
echo "         backup full database format '/backup_rman/bak_`date +%Y%m%d%H`/full_bk1_%u%p%s.rmn'; "                               >>/home/oracle/bin/rman_cmd
echo "         backup current controlfile format '/backup_rman/bak_`date +%Y%m%d%H`/rman_%T_CTL_%U'; "                              >>/home/oracle/bin/rman_cmd
echo "         backup spfile format '/backup_rman/bak_`date +%Y%m%d%H`/rman_%T_SPFILE_%U'; "                                        >>/home/oracle/bin/rman_cmd
echo "         release channel c1; "                                                                                                  >>/home/oracle/bin/rman_cmd
echo "         release channel c2; "                                                                                                  >>/home/oracle/bin/rman_cmd
echo "         release channel c3; "                                                                                                  >>/home/oracle/bin/rman_cmd
echo " } "                                                                                                                            >>/home/oracle/bin/rman_cmd
echo " crosscheck backupset; "                                                                                                        >>/home/oracle/bin/rman_cmd
echo " delete noprompt expired backup; "                                                                                              >>/home/oracle/bin/rman_cmd
echo " delete noprompt obsolete; "                                                                                                    >>/home/oracle/bin/rman_cmd
echo " crosscheck archivelog all; "                                                                                                   >>/home/oracle/bin/rman_cmd
echo " delete noprompt expired archivelog all;  "                                                                                     >>/home/oracle/bin/rman_cmd
#开始执行备份程序 rman_cmd
source /home/oracle/.bash_profile
/u01/app/oracle/product/11.2.0/dbhome_1/bin/sqlplus / as sysdba @ /home/oracle/bin/sql_cmd.sql >> $log
/u01/app/oracle/product/11.2.0/dbhome_1/bin/rman target / nocatalog cmdfile=/home/oracle/bin/rman_cmd  log=/backup_rman/log/rman_full_`date +%Y%m%d%H`.log
/u01/app/oracle/product/11.2.0/dbhome_1/bin/sqlplus / as sysdba @ /home/oracle/bin/ora_cmd.sql >> $log

#rm -rf /home/oracle/bin/rman_cmd
#删除备份程序 rman_cmd 下次备份重新创建
rm -rf $myVar
rm -rf $mysql
rm -rf $myora
