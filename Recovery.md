#### 查看备份文件 scn 信息    
    RMAN> list backup;
#### 启动数据库到mount状态
    RMAN> shutdown immediate;
    RMAN> startup mount;
#### 恢复数据库到需要的备份文件  
    RMAN> restore database until scn 1023411;
#### 恢复出错 RMAN-20208
    RMAN-20208: UNTIL CHANGE is before RESETLOGS change  
#### 根据我们想恢复到SCN，明确我们应该使用incarnation 2
    RMAN> list incarnation;
#### 恢复到incarnation 2
    RMAN> reset database to incarnation 2;
#### 恢复数据库到需要的备份文件   
    RMAN> restore database until scn 1023411;
#### 启动数据库  
    RMAN> alter database open resetlogs;

#### 到此备份恢复完成
