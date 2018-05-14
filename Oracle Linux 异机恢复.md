## 一 拷贝最新文件到新主机上
#### 1 rman 连接到源数据库
       [oracle@m1 ]$ rman target /
       connected to target database: CRM (DBID=1503894931)
       RMAN>
#### 2  分别列出备份文件详细信息
       RMAN> list backup of spfile;
            Piece Name: /oracle/app/db1/dbs/0dnsd96i_1_1
       RMAN> list backup of controlfile;
            Piece Name: /oracle/app/db1/dbs/0dnsd96i_1_1
       RMAN> list backup of database;
            Piece Name: /oracle/app/db1/dbs/0cnsd8vq_1_1
       RMAN> list backup of archivelog all;
#### 3 copy 这些备份到新的主机并授权
      [root@m1 /]# scp -r /home/oracle/bak_2018051415/ root@192.168.190.134:/home/oracle/

## 二 恢复参数文件及控制文件
#### 1 配置新主机上的ORACLE_SID
      SQL> shutdown immediate;
#### 2 在新主机上发起rman连接
      [oracle@m2 ]$ rman target /
#### 3  设置dbid 并启动实例到nomount状态
      RMAN> set DBID=1503894931
      executing command: SET DBID
      RMAN> startup nomount
      startup failed: ORA-01078: failure in processing system parameters
      注意：在rman下即使没有参数文件，默认也会启动一个DUMMY实例，以便能够恢复参数文件。
#### 4  恢复spfile文件，先mv新主机的spfile*.ora文件到别处
      cd /u01/app/oracle/product/11.2.0/dbhome_1/dbs/
      mv spfileorcl.ora spfileorcl.ora.bak
      RMAN> restore spfile to '/u01/app/oracle/product/11.2.0/dbhome_1/dbs/spfileorcl.ora' from '/home/oracle/bak_2018051415/rman_20180514_SPFILE_0dt2snjh_1_1';
      Finished restore at 10-DEC-12 
#### 5 startup force nomount
    RMAN> startup force nomount;
#### 6 恢复控制文件，先mv新主机的control01.ctl文件到别处
    cd /u01/app/oracle/oradata/orcl/
    mv control01.ctl control01.ctl.bak
    RMAN> restore controlfile to '/u01/app/oracle/oradata/orcl/control01.ctl' from '/home/oracle/bak_2018051415/rman_20180514_CTL_0ct2snjf_1_1';
    Finished restore at 10-DEC-12
    cp /u01/app/oracle/oradata/orcl/control01.ctl /u01/app/oracle/fast_recovery_area/orcl/control02.ctl
    给control02.ctl授权
    chown oracle:oinstall /u01/app/oracle/fast_recovery_area/orcl/control02.ctl
    chmod -R 755 /u01/app/oracle/fast_recovery_area/orcl/control02.ctl
#### 7 启动数据库到加载状态
    RMAN> alter database mount;
## 三  在新控制文件中注册数据文件备份和归档备份
    RMAN> catalog start with '/home/oracle/bak_2018051415/';
    ...
    Do you really want to catalog the above files (enter YES or NO)? yes
    ...
    List of Cataloged Files
    ... 
## 四  恢复整个库
    RMAN> restore database;
    ...
    Finished restore at 10-DEC-12

    RMAN> recover database;
    ...
    Finished recover at 10-DEC-12
    报错
    RMAN-03002: failure of recover command at 05/14/2018 16:21:36
    ORA-19698: /u01/app/oracle/oradata/orcl/redo01.log is from different database: id=1503895833, db_name=ORCL

    [root@m1 /]# scp /u01/app/oracle/oradata/orcl/redo0* root@192.168.190.134:/home/oracle/
    [root@m2 /]# cd home/oracle/
    [root@m2 oracle]# chown oracle:oinstall redo0*
    [root@m2 oracle]# chmod -R 755 redo0*
    alter database open resetlogs 打开数据库
    SQL> alter database open resetlogs;
    Database altered.
