## linux平台下的oracle自动备份案例(使用rman)

相关变量值：
ORACLE_BASE=/u01/app/oracle
ORACLE_HOME=/u01/app/oracle/product/11.2.0/dbhome_1
备份的数据库实例名：  db1
备份的目标目录：/backup_rman

实现过程如下：
第一步：准备目录
mkdir /backup_rman
chown oracle:oinstall /backup_rman
chmod -R 755 /backup_rman

第二步：备份脚本程序的编写
1、创建备份脚本
切换到oracle用户，在oracle家目录下面创建bin目录，新建文件rman_backup.sh
mkdir bin
cd bin
touch rman_backup.sh
chown oracle:oinstall rman_backup.sh
chmod 755 rman_backup.sh

2、创建rman的备份脚本文件
cd ~/bin 
touch rman_cmd
chown oracle:oinstall rman_cmd
chmod 755 rman_cmd
编辑rman_cmd文件添加如下内容(根据需要，可以进行适当的修改):
crosscheck archivelog all;
delete noprompt expired archivelog all;
run {
        configure retention policy to recovery window of 4 days;
        configure controlfile autobackup off;
        allocate channel c1 device type disk  format '/backup_rman/rman_full_%T_%U'  maxpiecesize=3G;
        allocate channel c2 device type disk  format '/backup_rman/rman_full_%T_%U'  maxpiecesize=3G;
        allocate channel c3 device type disk  format '/backup_rman/rman_full_%T_%U'  maxpiecesize=3G;
        //backup database plus archivelog delete all input;
		backup as compressed backupset full database format '/backup_rman2/full_bk1_%u%p%s.rmn';
		backup full database format '/backup_rman/full_bk1_%u%p%s.rmn';
        backup current controlfile format '/backup_rman/rman_%T_CTL_%U';
        backup spfile format '/backup_rman/rman_%T_SPFILE_%U';
        release channel c1;
        release channel c2;
        release channel c3;
}
crosscheck backupset;
delete noprompt expired backup;
delete noprompt obsolete;
crosscheck archivelog all;
delete noprompt expired archivelog all;

--------------------------------------下面为注释---------------------------------------------------
--Rman 归档文件丢失导致不能备份的，在备份前先执行以下两条命令
crosscheck archivelog all;
delete noprompt expired archivelog all;
--执行部分
run {
        configure retention policy to recovery window of 4 days;
        configure controlfile autobackup off;  --关闭自动备份控制文件
		--下面三句配置备份文件名字的格式。
		--channel 为rman与数据库建立一个连接， allocate channel 启动一个进程。
		--%T:年月日格式(YYYYMMDD);%U：是%u_%p_%c的简写形式，利用它可以为每一个备份片段(既磁盘文件)生成一个唯一的名称
		--maxpiecesize=3G;备份文件最大容量
        allocate channel c1 device type disk  format '/backup_rman/rman_full_%T_%U'  maxpiecesize=3G;
        allocate channel c2 device type disk  format '/backup_rman/rman_full_%T_%U'  maxpiecesize=3G;
        allocate channel c3 device type disk  format '/backup_rman/rman_full_%T_%U'  maxpiecesize=3G;
		--执行备份语句
        backup database plus archivelog delete all input;					--数据库
        backup current controlfile format '/backup_rman/rman_%T_CTL_%U';	--控制文件
        backup spfile format '/backup_rman/rman_%T_SPFILE_%U';				--spfile文件
		--释放连接
        release channel c1;
        release channel c2;
        release channel c3;
}
crosscheck backupset;
delete noprompt expired backup;
delete noprompt obsolete;
crosscheck archivelog all;
delete noprompt expired archivelog all;
-----------------------------------------------------------------------------------------
第三步：添加crontab计划任务
使用oracle用户添加例行任务：
crontab -e
新打开的窗口中添加一下内容：
0 24 * * * /home/oracle/bin/rman_backup.sh
(*/3 * * * * /home/oracle/bin/rman_backup.sh)
注，括号内的可以是做测试的时候用的，每三分钟执行一次备份，例为每天凌晨24点执行备份

第四步：执行验证：
1、crontab成功执行验证：
在root下执行tail -f /var/log/cron，监控cron日志来确保crontab的成功执行：
Aug 31 00:20:06 model crontab[6380]: (oracle) BEGIN EDIT (oracle)
Aug 31 00:20:48 model crontab[6380]: (oracle) REPLACE (oracle)
Aug 31 00:20:48 model crontab[6380]: (oracle) END EDIT (oracle)
Aug 31 00:21:01 model crond[26958]: (oracle) RELOAD (cron/oracle)
Aug 31 00:21:01 model crond[6412]: (oracle) CMD (/home/oracle/bin/rman_backup.sh)
Aug 31 00:24:01 model crond[6621]: (oracle) CMD (/home/oracle/bin/rman_backup.sh)
2、查看rman是否执行，并且执行成功
a.可在rman执行的时候执行ps -ef | grep rman | grep -v grep来查看rman进程是否成功启动
b.查看/backup_rman目录中是否有备份生成的文件：
$ oracle@model /backup_rman> ls
rman_20120831_CTL_0mnjvu15_1_1     rman_full_20120831_0injvtrq_1_1
rman_20120831_CTL_0vnjvu57_1_1     rman_full_20120831_0jnjvtvs_1_1
rman_20120831_SPFILE_0nnjvu18_1_1  rman_full_20120831_0knjvu0c_1_1
rman_20120831_SPFILE_10njvu5a_1_1  rman_full_20120831_0lnjvu13_1_1
rman_full_201208310021.log         rman_full_20120831_0onjvu1a_1_1
rman_full_201208310024.log         rman_full_20120831_0pnjvu1e_1_1
rman_full_20120831_0dnjvtrg_1_1    rman_full_20120831_0qnjvu1e_1_1
rman_full_20120831_0enjvtrg_1_1    rman_full_20120831_0rnjvu1i_1_1
rman_full_20120831_0fnjvtrg_1_1    rman_full_20120831_0snjvu4s_1_1
rman_full_20120831_0gnjvtrp_1_1    rman_full_20120831_0tnjvu52_1_1
rman_full_20120831_0hnjvtrp_1_1    rman_full_20120831_0unjvu55_1_1

验证结果：rman自动备份任务执行成功！ 

验证数据恢复
startup mount;
restore database;
recover database noredo;
recover database;
alter database open resetlogs;
修复控制文件损坏、丢失
restore controlfile from '/backup_rman/rman_20180116_CTL_2ksor1me_1_1';
restore spfile from '/tmp/bak/db_14_1_928703445'; 
restore controlfile from database;
