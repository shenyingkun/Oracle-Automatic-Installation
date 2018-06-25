#!/usr/bin/env python
#coding:utf-8
import time
import sys
import os
import shutil
import io
import commands
from optparse import OptionParser


print ("[INFO] --------------------- 挂载光盘 -----------------------")
time.sleep(2)
print ("[INFO] ------------------------------------------------------")
time.sleep(2)
path = '/mnt/cdrom'
def handleVersionFile():

    path = '/mnt/cdrom'
    str  = '/dev/sr0 /mnt/cdrom' #--------------------要查询的字符串
    str1 = 'mount /dev/cdrom /mnt/cdrom' #------------挂载语句
    str2 = 'umount /dev/cdrom' #----------------------卸载语句
    str3 = 'cat /proc/mounts' #-----------------------查询语句
    if  os.path.exists(path):# 判断目录是否存在
        time.sleep(2)
        if not os.listdir(path):
            print("[INFO] 挂载目录 /MNT/CDROM 可以直接挂载")
            time.sleep(2)
            val = commands.getoutput(str1)
            file = commands.getoutput(str3)
            if str in file:
                 print ("[INFO] 挂载成功")
            else:
                 print ("[ERROR] 挂载失败，程序退出")
                 os._exit(0)

        else:
            print("[INFO] 挂载目录 /MNT/CDROM 存在内容，卸载后重新挂载")
            time.sleep(2)
            val = commands.getoutput(str2)
            if not os.listdir(path):
                val = commands.getoutput(str1)
                file = commands.getoutput(str3)
                if str in file:
                     print ("[INFO] 挂载成功")
                else:
                     print ("[ERROR] 挂载失败，程序退出")
                     os._exit(0)
            else:
                print("[INFO] 挂载目录 /MNT/CDROM 存在无法卸载内容，必须手工检查目录")
                time.sleep(2)
                allfile=[]
                def getallfile(path):
                    allfilelist=os.listdir(path)
                    for file in allfilelist:
                        filepath=os.path.join(path,file)
                        #判断是不是文件夹
                        if os.path.isdir(filepath):
                            getallfile(filepath)
                        allfile.append(filepath)
                    return allfile

                if __name__ == '__main__':

                   allfiles=getallfile(path)
                   for item in allfiles:
                       print ("[ERROR]"+"挂载目录存在 "+item)
                os._exit(0)
    else: # 没有就创建
        print ("[INFO] 挂载目录 /MNT/CDROM 不存在，自动新建目录")
        os.mkdir(path)
        time.sleep(2)
        val = commands.getoutput(str1)
        file = commands.getoutput(str3)
        if str in file:
             print ("[INFO] 挂载成功")
        else:
             print ("[ERROR] 挂载失败，程序退出")
             os._exit(0)

if __name__ == "__main__":
    handleVersionFile()
time.sleep(2)
print ("[INFO] ------------------ 配置 YUM 安装源 -------------------")
time.sleep(2)
print ("[INFO] ------------------------------------------------------")
time.sleep(2)
os.chdir('/etc/yum.repos.d') #--------------------切换目录
def handleVersionFile():

    srcVersionFilePath = os.getcwd()+os.sep+"CentOS-Base.repo"
    dstVersionFilePath = os.getcwd()+os.sep+"CentOS-Base.repo.bak"

    srcProjectFilePath = os.getcwd()+os.sep+"CentOS-Base.repo"
    dstProjectFilePath = os.getcwd()+os.sep+"CentOS-Base.repo.bak"
    if not os.path.isfile(srcProjectFilePath):
        print("[ERROR] CENTOS-BASE.REPO 源文件不存在，程序退出")
        os._exit(0)
    else:
        time.sleep(2)
        if not os.path.isfile(dstProjectFilePath):
            print ('[INFO] CENTOS-BASE.REPO 开始拷贝')
            if os.path.exists(srcVersionFilePath):
                shutil.copyfile(srcVersionFilePath,dstVersionFilePath)
            if os.path.exists(srcProjectFilePath):
                shutil.copyfile(srcProjectFilePath,dstProjectFilePath)
                time.sleep(2)
            print ('[INFO] CENTOS-BASE.REPO 备份结束')
            os.remove(srcProjectFilePath)
            if os.path.isfile(srcProjectFilePath):
                os._exit(0)
        else:
            print("[ERROR] CENTOS-BASE.REPO.BAK 文件已存在，需要手工检查，程序退出")
            os._exit(0)
if __name__ == "__main__":
    handleVersionFile()


def handleVersionFile():

    srcVersionFilePath = os.getcwd()+os.sep+"CentOS-Media.repo"
    dstVersionFilePath = os.getcwd()+os.sep+"CentOS-Media.repo.bak"

    srcProjectFilePath = os.getcwd()+os.sep+"CentOS-Media.repo"
    dstProjectFilePath = os.getcwd()+os.sep+"CentOS-Media.repo.bak"
    if not os.path.isfile(srcProjectFilePath):
        print("[ERROR] CENTOS-MEDIA.REPO 源文件不存在，程序退出")
        #os._exit(0)
    else:
        time.sleep(2)
        if not os.path.isfile(dstProjectFilePath):
            print ('[INFO] CENTOS-MEDIA.REPO 开始拷贝')
            if os.path.exists(srcVersionFilePath):
                shutil.copyfile(srcVersionFilePath,dstVersionFilePath)
            if os.path.exists(srcProjectFilePath):
                shutil.copyfile(srcProjectFilePath,dstProjectFilePath)
                time.sleep(2)
            print ('[INFO] CENTOS-MEDIA.REPO 备份结束')
        else:
            print("[ERROR] CENTOS-MEDIA.REPO.BAK 文件已存在，需要手工检查，程序退出")
            os._exit(0)
if __name__ == "__main__":
    handleVersionFile()
time.sleep(2)
def handleVersionFile():
 f = io.open('/etc/yum.repos.d/CentOS-Media.repo.bak','r',encoding='utf-8')
 f_new = io.open('/etc/yum.repos.d/CentOS-Media.repo','w',encoding='utf-8')

 for line in f:
    # 进行判断
    if "enabled=0" in line:
        line = line.replace('enabled=0','enabled=1')
        print("[INFO] CENTOS-MEDIA.REPO 文件修改成功")
        time.sleep(2)
    if "baseurl=file:///media/CentOS/" in line:
        line = line.replace('baseurl=file:///media/CentOS/','baseurl=file:///mnt/cdrom/')
        print("[INFO] CENTOS-MEDIA.REPO 文件修改成功")
    # 如果不符合就正常的将文件中的内容读取并且输出到新文件中
    f_new.write(line)

 f.close()
 f_new.close()


if __name__ == "__main__":
    handleVersionFile()

time.sleep(2)
#import psutil
print ("[INFO] --------- 关闭防火墙和SELINUX，配置HOST文件 ----------")
time.sleep(2)
print ("[INFO] ------------------------------------------------------")
time.sleep(2)
##################################################
# HOSTS文件配置 ##
##################################################
def handleVersionFile():
 a = commands.getoutput("sed -n '/HOSTNAME/p' /etc/sysconfig/network| sed -s 's/=/ /g'|gawk '{print $2}'")
 b = commands.getoutput("sed -n '/IPADDR/p' /etc/sysconfig/network-scripts/ifcfg-eth0| sed -s 's/=/ /g'|gawk '{print $2}'")
 val = commands.getoutput("cat /etc/hosts")
 str = b+" "+a
    # 进行判断
 if str in val:
        print("[INFO] 网络文件 /etc/hosts 已配置，可以跳过")
        time.sleep(2)
 else:
        fp = open('/etc/hosts')
        lines = []
        for line in fp:
            lines.append(line)
        fp.close()

        lines.insert(3, str) # 在第二行插入
        s = ''.join(lines)
        fp = open('/etc/hosts', 'w')
        fp.write(s)
        fp.close()
        val1 = commands.getoutput("cat /etc/hosts")
        if str in val1:
            print("[INFO] 网络文件 /etc/hosts 配置成功")
        else:
            print("[ERROR] 网络文件 /etc/hosts 配置失败，程序退出")
            os._exit(0)

if __name__ == "__main__":
    handleVersionFile()

##################################################
# 关闭防火墙 SELINUX ##
##################################################

def handleVersionFile():
 val = commands.getoutput("service iptables stop")
 a = commands.getoutput('/etc/init.d/iptables status')
 b = commands.getoutput('setenforce 0')
 c = commands.getoutput('getenforce')
    # 进行判断
 if "iptables: Firewall is not running." in a:
        print("[INFO] IPTABLES 防火墙关闭成功")
        time.sleep(2)
 else:
        print("[ERROR] IPTABLES 防火墙关闭失败，程序退出")
        time.sleep(2)
        os._exit(0)
    # 进行判断
 if "Permissive" in c:
        print("[INFO] SELINUX 关闭成功")
        time.sleep(2)
 else:
        print("[ERROR] SELINUX 关闭失败，程序退出")
        time.sleep(2)
        os._exit(0)

if __name__ == "__main__":
    handleVersionFile()


time.sleep(2)

print ("[INFO] --------- 开始安装 RPM 依赖包，请勿退出程序 ----------")
time.sleep(2)
print ("[INFO] ------------------------------------------------------")
time.sleep(2)

def handleVersionFile():
 #val = os.system("yum -y install binutils compat-libstdc++-33 elfutils-libelf elfutils-libelf-devel glibc glibc-common glibc-devel gcc gcc-c++ libaio libaio-devel libgcc libstdc++ libstdc++-devel make sysstat unixODBC unixODBC-devel pdksh compat-db control-center libstdc++ libstdc++-devel xscreensaver openmotif21 ksh* compat-libcap* zip unzip")
 val = commands.getoutput("yum -y install binutils compat-libstdc++-33 elfutils-libelf elfutils-libelf-devel glibc glibc-common glibc-devel gcc gcc-c++ libaio libaio-devel libgcc libstdc++ libstdc++-devel make sysstat unixODBC unixODBC-devel pdksh compat-db control-center libstdc++ libstdc++-devel xscreensaver openmotif21 ksh* compat-libcap* zip unzip")

 a ='binutils compat-libstdc++-33 elfutils-libelf elfutils-libelf-devel glibc glibc-common glibc-devel gcc gcc-c++ libaio libaio-devel libgcc libstdc++ libstdc++-devel make sysstat unixODBC unixODBC-devel pdksh compat-db control-center libstdc++ libstdc++-devel xscreensaver openmotif21 ksh compat-libcap zip unzip'

 for package in a.split():
    # 进行判断
   str = 'rpm -qa|grep'+ ' ' +package
   a = commands.getoutput(str)
   if package in a:
        print("[INFO]"+" "+"RPM包 "+package+" "+"安装成功")
   else:
        print("[WARR]"+" "+"RPM包 "+package+" "+"安装失败")

if __name__ == "__main__":
    handleVersionFile()

time.sleep(2)
print ("[INFO] YUM 依赖包已安装，部分失败选项需手工检查")
time.sleep(2)
print ("[INFO] ------------- 创建 ORACLE 目录、用户和组 -------------")
time.sleep(2)
print ("[INFO] ------------------------------------------------------")
time.sleep(2)

def handleVersionFile():
 str  = 'cat /etc/group'
 str1 = 'cat /etc/shadow'
 a = commands.getoutput(str)
 a1 = commands.getoutput(str1)

    # 进行判断
 if "oinstall:x:501:" in a:
        print("[INFO] Oracle Group oinstall 已存在，可以跳过")
        time.sleep(2)
 else:
        val = os.system('/usr/sbin/groupadd -g 501 oinstall')
        b = commands.getoutput(str)
        if "oinstall:x:501:" in b:
               print("[INFO] Oracle Group oinstall 设置成功")
        else:
               print("[ERROR] Oracle Group oinstall 设置失败，程序退出")
               os._exit(0)
     # 进行判断
 if "dba:x:502:" in a:
        print("[INFO] Oracle Group dba 已存在，可以跳过")
        time.sleep(2)
 else:
        val = os.system('/usr/sbin/groupadd -g 502 dba')
        b = commands.getoutput(str)
        if "dba:x:502:" in b:
               print("[INFO] Oracle Group dba 设置成功")
        else:
               print("[ERROR] Oracle Group dba 设置失败，程序退出")
               os._exit(0)
      # 进行判断
 if "oracle" in a1:
        print("[INFO] Oracle Group oracle 已存在，可以跳过")
        time.sleep(3)
 else:
        val = os.system('/usr/sbin/useradd -g oinstall -G dba oracle')
        b = commands.getoutput(str1)
        if "oracle" in b:
               print("[INFO] Oracle Group oracle 设置成功")
        else:
               print("[ERROR] Oracle Group oracle 设置失败，程序退出")
               os._exit(0)
############# DBHOME DBHOME1 DBHOME2 #################
 DBHOME='/u01/app/oracle'
 DBHOME1='/u01/app/oradata'
 DBHOME2='/u01/app/oraInventory'
#################### DBHOME ##########################
 if  os.path.exists(DBHOME):# 判断目录是否存在
    if not os.listdir(DBHOME):
        print("[INFO] Oracle 目录 /u01/app/oracle 已存在，可以跳过 ")
        time.sleep(3)
    else:
        print("[ERROR] Oracle 目录 /u01/app/oracle 已存在内容，程序退出")
        os._exit(0)
 else: # 没有就创建
    os.makedirs(DBHOME)
    if  os.path.exists(DBHOME):# 再次判断目录是否存在
        print ("[INFO] Oracle 目录 /u01/app/oracle 创建成功")
    else:
        print("[ERROR] Oracle 目录 /u01/app/oracle 创建失败，程序退出")
        os._exit(0)
#DBHOME1 ####
 if  os.path.exists(DBHOME1):# 判断目录是否存在
    if not os.listdir(DBHOME1):
        print("[INFO] Oracle 目录 /u01/app/oradata 已存在，可以跳过 ")
        time.sleep(3)
    else:
        print("[ERROR] Oracle 目录 /u01/app/oradata 已存在内容，程序退出")
        os._exit(0)
 else: # 没有就创建
    os.makedirs(DBHOME1)
    if  os.path.exists(DBHOME1):# 再次判断目录是否存在
        print ("[INFO] Oracle 目录 /u01/app/oradata 创建成功")
    else:
        print("[ERROR] Oracle 目录 /u01/app/oradata 已存在内容，程序退出")
        os._exit(0)
#################### DBHOME2 ############################
 if  os.path.exists(DBHOME2):# 判断目录是否存在
    if not os.listdir(DBHOME2):
        print("[INFO] Oracle 目录 /u01/app/oraInventory 已存在，可以跳过")
        time.sleep(3)
    else:
        print("[ERROR] Oracle 目录 /u01/app/oraInventory 已存在内容，程序退出")
        #os._exit(0)
 else: # 没有就创建
    os.makedirs(DBHOME2)
    if  os.path.exists(DBHOME2):# 再次判断目录是否存在
        print ("[INFO] Oracle 目录 /u01/app/oraInventory 创建成功")
    else:
        print("[ERROR] Oracle 目录 /u01/app/oraInventory 已存在内容，程序退出")
        #os._exit(0)
#################### 判断目录是否可用 ########################
 if  os.path.exists(DBHOME and DBHOME1 and DBHOME2):# 判断目录是否存在
    print ("[INFO] Oracle 安装目录 DBHOME DBHOME1 DBHOME2 创建完成，可以使用")
    time.sleep(2)
    val2 = os.system('chown -R oracle:oinstall /u01/app/oracle/ /u01/app/oradata/ /u01/app/oraInventory')
    val3 = os.system('chmod -R 755 /u01/app/oracle/ /u01/app/oradata/ /u01/app/oraInventory')
    print("[INFO] Oracle 安装目录 DBHOME DBHOME1 DBHOME2 授权成功")
    time.sleep(2)
 else: # 没有就退出
    print ("[ERROR] Oracle 安装目录 DBHOME DBHOME1 DBHOME2 创建不成功，需要手工重新创建，程序退出")
    #os._exit(0)

 val = commands.getoutput('echo "oracle" | passwd --stdin oracle')
 val1 = commands.getoutput("sed -i /::/d /etc/hosts")
 print ("[INFO] Oracle 用户创建成功，密码：oracle")
 time.sleep(2)

if __name__ == "__main__":
    handleVersionFile()

time.sleep(2)

print ("[INFO] --------------- 配置 Oracle 环境变量 -----------------")
time.sleep(2)
print ("[INFO] ------------------------------------------------------")
time.sleep(2)

def handleVersionFile():
  a = commands.getoutput('cat /etc/sysctl.conf')
             ##检查
  if "fs.aio-max-nr " in a:
        print ("[INFO] 配置文件 /etc/sysctl.conf 已存在需要配置的内容，可以跳过")
        time.sleep(2)
        #os._exit(0)
  else:
        cmd1  = os.system("sed -i /kernel.shmmax/d /etc/sysctl.conf")
        cmd2  = os.system("sed -i /kernel.shmall/d /etc/sysctl.conf")
        cmd3  = os.system('echo "#ORACLE SETTING                          " >> /etc/sysctl.conf')
        cmd4  = os.system('echo "fs.aio-max-nr = 1048576                  " >> /etc/sysctl.conf')
        cmd5  = os.system('echo "fs.file-max = 6815744                    " >> /etc/sysctl.conf')
        cmd6  = os.system('echo "kernel.shmall = 2097152                  " >> /etc/sysctl.conf')
        cmd7  = os.system('echo "kernel.shmmax = 12884901888              " >> /etc/sysctl.conf')
        cmd8  = os.system('echo "kernel.shmmni = 4096                     " >> /etc/sysctl.conf')
        cmd9  = os.system('echo "kernel.sem = 250 32000 100 128           " >> /etc/sysctl.conf')
        cmd10 = os.system('echo "net.ipv4.ip_local_port_range = 9000 65500" >> /etc/sysctl.conf')
        cmd11 = os.system('echo "net.core.rmem_default = 262144           " >> /etc/sysctl.conf')
        cmd12 = os.system('echo "net.core.rmem_max = 4194304              " >> /etc/sysctl.conf')
        cmd13 = os.system('echo "net.core.wmem_default = 262144           " >> /etc/sysctl.conf')
        cmd14 = os.system('echo "net.core.wmem_max = 1048586              " >> /etc/sysctl.conf')
        cmd15 = commands.getoutput("sysctl -p")
        print ("[INFO] 配置文件 /etc/sysctl.conf 环境变量配置成功")
        time.sleep(2)

  b = commands.getoutput('cat /etc/profile')

  if "oracle " in b:
        print ("[INFO] 配置文件 /etc/profile 已存在需要配置的内容，可以跳过")
        time.sleep(2)
        #os._exit(0)
  else:
        cmd1  = os.system('echo "if [ $USER = "oracle" ]; then ">> /etc/profile')
        cmd1  = os.system('echo "    if [ $SHELL = "/bin/ksh" ]; then">> /etc/profile')
        cmd1  = os.system('echo "          ulimit -p 16384 ">> /etc/profile')
        cmd1  = os.system('echo "          ulimit -n 65536 ">> /etc/profile')
        cmd1  = os.system('echo "    else ">> /etc/profile')
        cmd1  = os.system('echo "          ulimit -u 16384 -n 65536 ">> /etc/profile')
        cmd1  = os.system('echo "    fi ">> /etc/profile')
        cmd1  = os.system('echo "fi  ">> /etc/profile')
        print ("[INFO] 配置文件 /etc/profile 环境变量配置成功")
        time.sleep(2)

  c = commands.getoutput('cat /home/oracle/.bash_profile')

  if "oracle " in c:
        print ("[INFO] 配置文件 /home/oracle/.bash_profile 已存在需要配置的内容，可以跳过")
        time.sleep(2)
        #os._exit(0)
  else:
        time.sleep(2)
        cmd2 = os.system('echo "PATH=\$PATH:\$ORACLE_HOME/bin                        " >> /home/oracle/.bash_profile')
        cmd2 = os.system('echo "export PATH                                          " >> /home/oracle/.bash_profile')
        cmd2 = os.system('echo "umask 022                                            " >> /home/oracle/.bash_profile')
        cmd2 = os.system('echo "ORACLE_BASE=/u01/app/oracle                          " >> /home/oracle/.bash_profile')
        cmd2 = os.system('echo "ORACLE_SID=orcl                                      " >> /home/oracle/.bash_profile')
        cmd2 = os.system('echo "ORACLE_HOME=/u01/app/oracle/product/11.2.0/dbhome_1  " >> /home/oracle/.bash_profile')
        cmd2 = os.system('echo "PATH=\$ORACLE_HOME/bin/:\$PATH                       " >> /home/oracle/.bash_profile')
        cmd2 = os.system('echo "LANG=en_US.UTF-8                                     " >> /home/oracle/.bash_profile')
        cmd2 = os.system('echo "export ORACLE_BASE ORACLE_HOME ORACLE_SID            " >> /home/oracle/.bash_profile')
        cmd2 = os.system('source /home/oracle/.bash_profile')
        print ("[INFO] 配置文件 /home/oracle/.bash_profile 环境变量配置成功")


if __name__ == "__main__":
    handleVersionFile()

time.sleep(2)

print ("[INFO] ------------------- 解压安装文件 ---------------------")
time.sleep(2)
print ("[INFO] ------------------------------------------------------")
time.sleep(2)

def handleVersionFile():
    path1 = '/tools'
    path2 = '/tools/database'
    file1 = '/p13390677_112040_Linux-x86-64_1of7.zip'
    file2 = '/p13390677_112040_Linux-x86-64_2of7.zip'
    str  = 'unzip /p13390677_112040_Linux-x86-64_1of7.zip -d /tools'
    str1 = 'unzip /p13390677_112040_Linux-x86-64_2of7.zip -d /tools'

    if  os.path.exists(path1):# 判断目录是否存在
        val = os.system('chmod 777 /tools')
        val = os.system('chown oracle:dba /tools -R')
        if os.path.exists(path2):
            print("[INFO] 安装目录 /tools 存在 database 目录，删除以后再操作")
            time.sleep(2)
            shutil.rmtree(path2)
            if os.path.exists(path2):
                print("[ERROR] 安装目录 /tools/database 无法删除,请手工删除，程序退出")
                os.exit(0)
            else:
                print("[INFO] 安装目录 /tools/database 已删除，开始解压安装文件")
                if os.path.exists(file1 and file2):
                      print("[INFO] 开始解压 FILE1，请勿退出程序")
                      #val = os.system(str)
                      val = commands.getoutput(str)
                      print("[INFO] 开始解压 FILE2，请勿退出程序")
                      #val = os.system(str1)
                      val = commands.getoutput(str1)
                      if os.path.exists(path2):
                            print("[INFO] 解压完成")
                            time.sleep(3)
                      else:
                            print("[ERROR] 解压失败，程序退出")
                            os._exit(0)
                      time.sleep(3)
                else:
                      print("[ERROR] 安装文件不存在，请重新上传安装文件，程序退出")
                      os.exit(0)
        else:
                print("[INFO] 开始解压安装文件")
                if os.path.exists(file1 and file2):
                      print("[INFO] 开始解压 FILE1，请勿退出程序")
                      #val = os.system(str)
                      val = commands.getoutput(str)
                      print("[INFO] 开始解压 FILE2，请勿退出程序")
                      #val = os.system(str1)
                      val = commands.getoutput(str1)
                      if os.path.exists(path2):
                            print("[INFO] 解压完成")
                            time.sleep(3)
                      else:
                            print("[ERROR] 解压失败，程序退出")
                            os._exit(0)
                      time.sleep(2)
                else:
                      print("[ERROR] 安装文件不存在，请重新上传安装文件，程序退出")
                      os.exit(0)
    else:
        os.mkdir(path1)
        val = os.system('chmod 777 /tools')
        val = os.system('chown oracle:dba /tools -R')
        if  os.path.exists(path1):# 判断目录是否存在
            print ("[INFO] 安装目录 /tools,已自动创建，开始解压安装文件")
            time.sleep(2)
            if os.path.exists(file1 and file2):
                   print("[INFO] 开始解压 FILE1，请勿退出程序")
                   #val = os.system(str)
                   val = commands.getoutput(str)
                   print("[INFO] 开始解压 FILE2，请勿退出程序")
                   #val = os.system(str1)
                   val = commands.getoutput(str1)
                   if os.path.exists(path2):
                         print("[INFO] 解压完成")
                         time.sleep(3)
                   else:
                         print("[ERROR] 解压失败，程序退出")
                         os._exit(0)
                   time.sleep(3)
            else:
                   print("[ERROR] 安装文件不存在，请重新上传安装文件，程序退出")
                   os.exit(0)
        else:
            print ("[ERROR] 安装目录 /tools 创建失败，程序退出")
            os.exit(0)
if __name__ == "__main__":
    handleVersionFile()
time.sleep(3)

print ("[INFO] ------------------- 配置安装文件 ---------------------")
time.sleep(2)
print ("[INFO] ------------------------------------------------------")
time.sleep(2)

def handleVersionFile():
    str0  = 'oracle.install.option='
    str1  = 'ORACLE_HOSTNAME='
    str2  = 'UNIX_GROUP_NAME='
    str3  = 'INVENTORY_LOCATION='
    str4  = 'SELECTED_LANGUAGES=en'
    str5  = 'ORACLE_HOME='
    str6  = 'ORACLE_BASE='
    str7  = 'oracle.install.db.InstallEdition='
    str8  = 'oracle.install.db.DBA_GROUP='
    str9  = 'oracle.install.db.OPER_GROUP='
    str10 = 'DECLINE_SECURITY_UPDATES='
    str11 = "sed -n '/HOSTNAME/p' /etc/sysconfig/network| sed -s 's/=/ /g'|gawk '{print $2}'"

    str = 'cat /tools/database/response/db_install.rsp'
    a = commands.getoutput(str)
    if str0 in a:   # 判断是否存在
        val = os.system('sed -i "s/oracle.install.option=/oracle.install.option=INSTALL_DB_SWONLY/g" /tools/database/response/db_install.rsp')
        b = commands.getoutput(str)
        if str0+"INSTALL_DB_SWONLY" in b :
            print("[INFO] 配置 ORACLE.INSTALL.OPTION=INSTALL_DB_SWONLY 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 ORACLE.INSTALL.OPTION=INSTALL_DB_SWONLY 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，退出")
        os._exit(0)

    if str1 in a:   # 判断是否存在
        hostname1 = commands.getoutput(str11)
        val = os.system('sed -i "s/ORACLE_HOSTNAME=/ORACLE_HOSTNAME=%s/g" /tools/database/response/db_install.rsp' %(hostname1))
        b = commands.getoutput(str)
        str_new = str1+hostname1
        if str_new in b :
            print("[INFO] 配置 ORACLE_HOSTNAME 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 ORACLE_HOSTNAME 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，退出")
        os._exit(0)


    if str2 in a:   # 判断是否存在
        val = os.system('sed -i "s/UNIX_GROUP_NAME=/UNIX_GROUP_NAME=dba/g" /tools/database/response/db_install.rsp')
        b = commands.getoutput(str)
        if str2+"dba" in b :
            print("[INFO] 配置 UNIX_GROUP_NAME 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 UNIX_GROUP_NAME 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)


    if str3 in a:   # 判断是否存在
        val = os.system('sed -i "s/INVENTORY_LOCATION=/INVENTORY_LOCATION=\/u01\/app\/oraInventory/g" /tools/database/response/db_install.rsp')
        b = commands.getoutput(str)
        if str3+"/u01/app/oraInventory" in b :
            print("[INFO] 配置 INVENTORY_LOCATION 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 INVENTORY_LOCATION 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，退出")
        os._exit(0)

    if str4 in a:   # 判断是否存在
        val = os.system('sed -i "s/SELECTED_LANGUAGES=en/SELECTED_LANGUAGES=en,zh_CN/g" /tools/database/response/db_install.rsp')
        b = commands.getoutput(str)
        if str4+",zh_CN" in b :
            print("[INFO] 配置 SELECTED_LANGUAGES 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 SELECTED_LANGUAGES 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，退出")
        os._exit(0)

    if str5 in a:   # 判断是否存在
        val = os.system('sed -i "s/ORACLE_HOME=/ORACLE_HOME=\/u01\/app\/oracle\/product\/11.2.0\/dbhome_1/g" /tools/database/response/db_install.rsp')
        b = commands.getoutput(str)
        if str5+"/u01/app/oracle/product/11.2.0/dbhome_1" in b :
            print("[INFO] 配置 ORACLE_HOME 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 ORACLE_HOME 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)

    if str6 in a:   # 判断是否存在
        val = os.system('sed -i "s/ORACLE_BASE=/ORACLE_BASE=\/u01\/app\/oracle/g" /tools/database/response/db_install.rsp')
        b = commands.getoutput(str)
        if str6+"/u01/app/oracle" in b :
            print("[INFO] 配置 ORACLE_BASE 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 ORACLE_BASE 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)

    if str7 in a:   # 判断是否存在
        val = os.system('sed -i "s/oracle.install.db.InstallEdition=/oracle.install.db.InstallEdition=EE/g" /tools/database/response/db_install.rsp')
        b = commands.getoutput(str)
        if str7+"EE" in b :
            print("[INFO] 配置 ORACLE.INSTALL.DB.INSTALLEDITION 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 ORACLE.INSTALL.DB.INSTALLEDITION 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)

    if str8 in a:   # 判断是否存在
        val = os.system('sed -i "s/oracle.install.db.DBA_GROUP=/oracle.install.db.DBA_GROUP=dba/g" /tools/database/response/db_install.rsp')
        b = commands.getoutput(str)
        if str8+"dba" in b :
            print("[INFO] 配置 ORACLE.INSTALL.DB.DBA_GROUP 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 ORACLE.INSTALL.DB.DBA_GROUP 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)

    if str9 in a:   # 判断是否存在
        val = os.system('sed -i "s/oracle.install.db.OPER_GROUP=/oracle.install.db.OPER_GROUP=dba/g" /tools/database/response/db_install.rsp')
        b = commands.getoutput(str)
        if str9+"dba" in b :
            print("[INFO] 配置 ORACLE.INSTALL.DB.OPER_GROUP 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 ORACLE.INSTALL.DB.OPER_GROUP 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)

    if str10 in a:   # 判断是否存在
        val = os.system('sed -i "s/DECLINE_SECURITY_UPDATES=/DECLINE_SECURITY_UPDATES=true/g" /tools/database/response/db_install.rsp')
        b = commands.getoutput(str)
        if str10+"true" in b :
            print("[INFO] 配置 DECLINE_SECURITY_UPDATES 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 DECLINE_SECURITY_UPDATES 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)

if __name__ == "__main__":
    handleVersionFile()
time.sleep(5)
##################################################
# dbca.rsp files
##################################################

def handleVersionFile():

    str = 'cat /tools/database/response/dbca.rsp'
    a = commands.getoutput(str)
    if "GDBNAME =" in a:   # 判断是否存在
        str0='sed -i "s/GDBNAME = \\"orcl11g.us.oracle.com\\"/GDBNAME = \\"orcl\\"/g" /tools/database/response/dbca.rsp'
        val = os.system(str0)
        b = commands.getoutput(str)
        if 'GDBNAME = "orcl"' in b :
            print("[INFO] 配置 GDBNAME 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 GDBNAME 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)

    if "SID =" in a:   # 判断是否存在
        val = os.system('sed -i "s/SID = \\"orcl11g\\"/SID = \\"orcl\\"/g" /tools/database/response/dbca.rsp')
        b = commands.getoutput(str)
        if 'SID = "orcl"' in b :
            print("[INFO] 配置 SID 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 SID 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)

    if "DATAFILEDESTINATION =" in a:   # 判断是否存在
        val = os.system('sed -i "s/#DATAFILEDESTINATION =/DATAFILEDESTINATION = \\"\/oradata\\"/g" /tools/database/response/dbca.rsp')
        b = commands.getoutput(str)
        if 'DATAFILEDESTINATION = "/oradata"' in b :
            print("[INFO] 配置 DATAFILEDESTINATION 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 DATAFILEDESTINATION 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)

    if "RECOVERYAREADESTINATION=" in a:   # 判断是否存在
        val = os.system('sed -i "s/#RECOVERYAREADESTINATION=/RECOVERYAREADESTINATION= \\"\/u01\/app\/oracle\/flash_recovery_area\\"/g" /tools/database/response/dbca.rsp')
        b = commands.getoutput(str)
        if 'RECOVERYAREADESTINATION= "/u01/app/oracle/flash_recovery_area"' in b :
            print("[INFO] 配置 RECOVERYAREADESTINATION 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 RECOVERYAREADESTINATION 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)

    if "CHARACTERSET = " in a:   # 判断是否存在
        val = os.system('sed -i "s/#CHARACTERSET = \\"US7ASCII\\"/CHARACTERSET = \\"AL32UTF8\\"/g" /tools/database/response/dbca.rsp')
        b = commands.getoutput(str)
        if 'CHARACTERSET = "AL32UTF8"' in b :
            print("[INFO] 配置 CHARACTERSET 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 CHARACTERSET 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)

    if "NATIONALCHARACTERSET= " in a:   # 判断是否存在
        val = os.system('sed -i "s/#NATIONALCHARACTERSET= \\"UTF8\\"/NATIONALCHARACTERSET = \\"UTF8\\"/g" /tools/database/response/dbca.rsp')
        b = commands.getoutput(str)
        if 'NATIONALCHARACTERSET = "UTF8"' in b :
            print("[INFO] 配置 NATIONALCHARACTERSET 完成")
            time.sleep(3)
        else:
            print("[ERROR] 配置 NATIONALCHARACTERSET 错误，程序退出")
            os._exit(0)
    else:
        print ("[ERROR] 配置文件内容不存在，程序退出")
        os._exit(0)

if __name__ == "__main__":
    handleVersionFile()

time.sleep(3)
print ("[INFO] ---------------- 安装 Oracle 数据库 ------------------")
time.sleep(2)
print ("[INFO] ------------------------------------------------------")
time.sleep(2)

def handleVersionFile():
  DBFILE1 = '/home/oracle/DBFILE1.py'

  if not os.path.isfile(DBFILE1):
      os.mknod(DBFILE1)
      cmd = os.system('echo \'#!/usr/bin/env python  \' >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "#coding:utf-8  " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "import time " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "import sys " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "import os " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "import shutil " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "import io " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "import commands " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "from optparse import OptionParser " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo " " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo " " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "def handleVersionFile(): " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "    str0 = \'cd /tools/database/\' " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "    str1 = \'./runInstaller -silent -responseFile /tools/database/response/db_install.rsp\' " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo \'    str11 = str0+"&&"+str1 \' >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "    val1 = commands.getoutput(str11) " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo \'    if "Successfully Setup Software." in val1: \' >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo \'        print("[INFO] 1.Successfully Setup Software.") \' >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "        time.sleep(2) " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "    else: " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo \'        print("[ERROR] 1.Failed Setup Software.") \' >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "        time.sleep(2) " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "        os._exit(0) " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "    # 进行判断 " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo " " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo \'if __name__ == "__main__": \' >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "    handleVersionFile() " >> /home/oracle/DBFILE1.py')
      cmd = os.system('echo "time.sleep(2) " >> /home/oracle/DBFILE1.py')
      if os.path.getsize(DBFILE1):
          os.system('chmod 777 /home/oracle/DBFILE1.py')
          os.system('chown oracle:dba /home/oracle/DBFILE1.py -R')
          print("[INFO] 临时脚本文件 DBFILE1.py 创建成功")
          time.sleep(2)
          DBFILE2 = '/home/oracle/DBFILE2.py'
          if not os.path.isfile(DBFILE2):
              os.mknod(DBFILE2)
              cmd = os.system('echo \'#!/usr/bin/env python  \' >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "#coding:utf-8  " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "import time " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "import sys " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "import os " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "import shutil " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "import io " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "import commands " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "from optparse import OptionParser " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo " " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo " " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "def handleVersionFile(): " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "    str0 = \'cd /tools/database/install/\' " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "    str1 = \'netca -silent -responsefile /tools/database/response/netca.rsp\' " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo \'    str11 = str0+"&&"+str1 \' >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "    val1 = commands.getoutput(str11) " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo \'    if "Oracle Net Services configuration successful" in val1: \' >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo \'        print("[INFO] 2.Successfully Setup Software.") \' >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "        time.sleep(2) " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "    else: " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo \'        print("[ERROR] 2.Failed Setup Software.") \' >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "        time.sleep(2) " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "        os._exit(0) " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "    # 进行判断 " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo " " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo \'if __name__ == "__main__": \' >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "    handleVersionFile() " >> /home/oracle/DBFILE2.py')
              cmd = os.system('echo "time.sleep(2) " >> /home/oracle/DBFILE2.py')
              if os.path.getsize(DBFILE1):
                  os.system('chmod 777 /home/oracle/DBFILE2.py')
                  os.system('chown oracle:dba /home/oracle/DBFILE2.py -R')
                  print("[INFO] 临时脚本文件 DBFILE2.py 创建成功")
                  time.sleep(2)
                  DBFILE3 = '/home/oracle/DBFILE3.py'
                  if not os.path.isfile(DBFILE3):
                      os.mknod(DBFILE3)
                      cmd = os.system('echo \'#!/usr/bin/env python  \' >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "#coding:utf-8  " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "import time " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "import sys " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "import os " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "import shutil " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "import io " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "import commands " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "from optparse import OptionParser " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo " " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo " " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "def handleVersionFile(): " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "    str0 = \'cd /tools/database/install/\' " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "    str1 = \'dbca -silent -createDatabase -templateName General_Purpose.dbc -gdbName orcl1 -sysPassword oracle -systemPassword oracle\' " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo \'    str11 = str0+"&&"+str1 \' >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "    val1 = commands.getoutput(str11) " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo \'    if "100% complete" in val1: \' >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo \'        print("[INFO] 3.Successfully Setup Software.") \' >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "        time.sleep(2) " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "    else: " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo \'        print("[ERROR] 3.Failed Setup Software.") \' >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "        time.sleep(2) " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "        os._exit(0) " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "    # 进行判断 " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo " " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo \'if __name__ == "__main__": \' >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "    handleVersionFile() " >> /home/oracle/DBFILE3.py')
                      cmd = os.system('echo "time.sleep(2) " >> /home/oracle/DBFILE3.py')
                      if os.path.getsize(DBFILE1):
                          os.system('chmod 777 /home/oracle/DBFILE3.py')
                          os.system('chown oracle:dba /home/oracle/DBFILE3.py -R')
                          print("[INFO] 临时脚本文件 DBFILE3.py 创建成功")
                          time.sleep(2)
                      else:
                          print("临时脚本文件 DBFILE3.py 创建失败")
                  else:
                      print("临时脚本文件 DBFILE3.py 已存在，请手工查看")
                      os._exit(0)
              else:
                  print("临时脚本文件 DBFILE2.py 创建失败")
          else:
              print("临时脚本文件 DBFILE2.py 已存在，请手工查看")
              os._exit(0)
      else:
          print("临时脚本文件 DBFILE1.py 创建失败")
  else:
      print("临时脚本文件 DBFILE1.py 已存在，请手工查看")
      os._exit(0)

if __name__ == "__main__":
    handleVersionFile()

#######################################################
print("[INFO] Oracle 数据库开始静默安装，请勿退出程序")
time.sleep(2)
#######################################################

def handleVersionFile():
    str = 'su - oracle -c "python /home/oracle/DBFILE1.py"'
    val = commands.getoutput(str)
    if "Successfully Setup Software." in val:
        print("[INFO] Oracle 数据库软件安装成功")
        str1 = 'su - oracle -c "python /home/oracle/DBFILE2.py"'
        val1 = commands.getoutput(str1)
        time.sleep(3)
        if "Successfully Setup Software." in val1:
            print("[INFO] Oracle 数据库监听软件配置成功")
            str2 = 'su - oracle -c "python /home/oracle/DBFILE3.py"'
            val2 = commands.getoutput(str2)
	    time.sleep(3)
            if "Successfully Setup Software." in val2:
                print("[INFO] Oracle 数据库配置成功")
		time.sleep(3)
            else:
                print("[ERROR] Oracle 数据库配置失败")
        else:
            print("[ERROR] Oracle 数据库监听软件配置失败")
    else:
        print("[ERROR] 数据库软件安装失败")
    # 执行临时脚本文件
    DBFILE1 = '/home/oracle/DBFILE1.py'
    DBFILE2 = '/home/oracle/DBFILE2.py'
    DBFILE3 = '/home/oracle/DBFILE3.py'
    if os.path.isfile(DBFILE1):
        os.remove(DBFILE1)
        if os.path.isfile(DBFILE2):
            os.remove(DBFILE2)
            if os.path.isfile(DBFILE3):
                os.remove(DBFILE3)
                print("[INFO] Oracle 数据库安装结束")




if __name__ == "__main__":
    handleVersionFile()
time.sleep(2)


time.sleep(3)
print("[INFO] 请开始下一步")
