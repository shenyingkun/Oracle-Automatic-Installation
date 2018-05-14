##       
RMAN> list backup;


RMAN> shutdown immediate;

RMAN> startup mount;

RMAN> restore database until scn 1023411;

RMAN-20208: UNTIL CHANGE is before RESETLOGS change  

####根据我们想恢复到SCN，明确我们应该使用incarnation 2

RMAN> list incarnation;

RMAN> reset database to incarnation 2;

RMAN> restore database until scn 1023411;

RMAN> alter database open resetlogs;

RMAN> list incarnation;

根据我们想恢复到SCN，明确我们应该使用incarnation 2

到此备份恢复完成
