#!/bin/bash
source /home/oracle/.bash_profile
/u01/app/oracle/product/11.2.0/dbhome_1/bin/rman target / nocatalog cmdfile=/u01/bin/rman_cmd  log=/backup_rman/rman_full_`date +%Y%m%d%H%M`.log
