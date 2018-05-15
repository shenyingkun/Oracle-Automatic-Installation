## 一 拷贝最新文件到新主机上
#### 1 rman 连接到源数据库
    [oracle@m1 ]$ rman target /
      connected to target database: CRM (DBID=1503894931)
    RMAN>
#### 2  分别列出备份文件详细信息
    RMAN> list backup of spfile;
             Piece Name: /home/oracle/bak_2018051415/full_bk1_07t2snh317.rmn
             Piece Name: /home/oracle/bak_2018051415/full_bk1_0bt2snil111.rmn
             Piece Name: /home/oracle/bak_2018051415/rman_20180514_SPFILE_0dt2snjh_1_1
             
    RMAN> list backup of controlfile;
             Piece Name: /home/oracle/bak_2018051415/full_bk1_06t2snh116.rmn
             Piece Name: /home/oracle/bak_2018051415/full_bk1_0at2snih110.rmn
             Piece Name: /home/oracle/bak_2018051415/rman_20180514_CTL_0ct2snjf_1_1
             
    RMAN> list backup of database;
             Piece Name: /home/oracle/bak_2018051415/full_bk1_05t2snh115.rmn
             Piece Name: /home/oracle/bak_2018051415/full_bk1_04t2snh114.rmn
             Piece Name: /home/oracle/bak_2018051415/full_bk1_09t2snih19.rmn
             Piece Name: /home/oracle/bak_2018051415/full_bk1_08t2snih18.rmn
             
    RMAN> list backup of archivelog all;
#### 3 copy 这些备份到新的主机并授权
    [root@m1 /]# scp -r /home/oracle/bak_2018051415/ root@192.168.190.134:/home/oracle/
    [root@m2 /]# cd home/oracle/
    [root@m2 oracle]# chown oracle:oinstall *
    [root@m2 oracle]# chmod -R 755 *

## 二 恢复参数文件及控制文件
#### 1 关闭新数据库
    SQL> shutdown immediate;
#### 2 先mv新主机上的spfile*.ora文件到别处
    [root@m2 /]# cd /u01/app/oracle/product/11.2.0/dbhome_1/dbs/
    [root@m2 dbs]# mv spfileorcl.ora spfileorcl.ora.bak
#### 3 在新主机上发起rman连接，设置dbid 并启动实例到nomount状态
    [oracle@m2 ]$ rman target /
    RMAN> set DBID=1503894931
      executing command: SET DBID
    RMAN> startup nomount
      startup failed: ORA-01078: failure in processing system parameters
 注意：在rman下即使没有参数文件，默认也会启动一个DUMMY实例，以便能够恢复参数文件。
#### 4  恢复 spfile 文件
    [oracle@m2 ]$ rman target /
    RMAN> restore spfile to '/u01/app/oracle/product/11.2.0/dbhome_1/dbs/spfileorcl.ora' from '/home/oracle/bak_2018051415/rman_20180514_SPFILE_0dt2snjh_1_1';
      Finished restore at 10-DEC-12 
#### 5 启动数据库到 nomount 状态
    RMAN> startup force nomount;
#### 6 恢复控制文件，先mv新主机的control01.ctl文件到别处
    [root@m2 /]# cd /u01/app/oracle/oradata/orcl/
    [root@m2 orcl]# mv control01.ctl control01.ctl.bak
#### 7 恢复控制文件
    RMAN> restore controlfile to '/u01/app/oracle/oradata/orcl/control01.ctl' from '/home/oracle/bak_2018051415/rman_20180514_CTL_0ct2snjf_1_1';
    Finished restore at 10-DEC-12
#### 8 拷贝 control01.ctl 覆盖 control02.ctl
    [root@m2 /]# cd /u01/app/oracle/fast_recovery_area/orcl/
    [root@m2 orcl]# mv control02.ctl control02.ctl.bak
    [root@m2 orcl]# cd /u01/app/oracle/oradata/orcl/
    [root@m2 orcl]# cp control01.ctl /u01/app/oracle/fast_recovery_area/orcl/
    给control02.ctl授权
    [root@m2 orcl]#  chown oracle:oinstall *
    [root@m2 orcl]#  chmod -R 755 *
#### 9 启动数据库到加载状态
    RMAN> alter database mount;
    
## 三  在新数据库中注册数据文件备份和归档备份
    RMAN> catalog start with '/home/oracle/bak_2018051415/';
    ...
    Do you really want to catalog the above files (enter YES or NO)? yes
    ...
    List of Cataloged Files
    ... 
## 四  恢复数据库
#### 1 
    RMAN> restore database;
    ...
    Finished restore at 10-DEC-12
#### 2
    RMAN> recover database;
    ...
    Finished recover at 10-DEC-12
    报错
    RMAN-03002: failure of recover command at 05/14/2018 16:21:36
    ORA-19698: /u01/app/oracle/oradata/orcl/redo01.log is from different database: id=1503895833, db_name=ORCL
    解决办法：
    [root@m1 /]# cd /u01/app/oracle/oradata/orcl/
    [root@m1 orcl]#scp redo0* root@192.168.190.134:/home/oracle/
    [root@m2 /]# cd home/oracle/
    [root@m2 oracle]# chown oracle:oinstall redo0*
    [root@m2 oracle]# chmod -R 755 redo0*
    重新执行 recover database
 #### 3
    alter database open resetlogs 打开数据库
    SQL> alter database open resetlogs;
    Database altered.
    恢复完成，登陆验证数据
