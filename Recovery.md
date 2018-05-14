## 查看备份文件 scn 信息    
    RMAN> list backup;
## 查看备份文件 scn 信息
    RMAN> shutdown immediate;
## 查看备份文件 scn 信息   
    RMAN> startup mount;
## 查看备份文件 scn 信息   
    RMAN> restore database until scn 1023411;
## 查看备份文件 scn 信息   
    RMAN-20208: UNTIL CHANGE is before RESETLOGS change  
## 查看备份文件 scn 信息   
## 根据我们想恢复到SCN，明确我们应该使用incarnation 2
    RMAN> list incarnation;
## 查看备份文件 scn 信息   
    RMAN> reset database to incarnation 2;
## 查看备份文件 scn 信息   
    RMAN> restore database until scn 1023411;
## 查看备份文件 scn 信息   
    RMAN> alter database open resetlogs;
## 查看备份文件 scn 信息   
    RMAN> list incarnation;

## 根据我们想恢复到SCN，明确我们应该使用incarnation 2

## 到此备份恢复完成
