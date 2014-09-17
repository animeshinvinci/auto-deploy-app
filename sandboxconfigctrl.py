#######################################################
#
#
#
#
#
#
#
#######################################################

import os
import time
from config import *
from fabric.api import *
from sshconnectionmgr import *
from hgutil import *

class SandBoxConfigCtrl(object):

	def __init__(self,user,host,issue,server_key):
		self.user = user
		self.host = host
                self.issue = issue
		self.server_key = server_key
                self.db_backupdir = ""
		
        def makeSandBoxDir(self):
                dirpath = self.getBaseDir() + "/" + self.host + "/" + self.issue 
                run("mkdir -p %s"%dirpath)
        
        def cloneRepo(self):
                repourl = self.getAppReporUrl()
                dirpath = self.getBaseDir() + "/" + self.host + "/" + self.issue 
                clone_repo(repourl,dirpath)
                
	def getAppReporUrl(self):
		return REPO_URL_MAP.get(self.server_key,"")
		 

	def getDBTempDIR(self):
		return self.getBaseDir() + "database_%s/"
	
        
        def cloneDBRepo(self):
                dirpath = self.getDBBackupDir() 
                run("mkdir -p %s"%dirpath)
                db_repo_dir = self.getDBReporUrl()
                clone_repo(db_repo_dir,dirpath)

        def getListOfFiles(self):
        
                dirList = run("ls %s"%self.db_backupdir)
                sql_files = filter(lambda a:a.strip(),dirList.split(" "))
                return sql_files
                 
                
	def getDBReporUrl(self):
		return DB_REPO_URL_MAP.get(self.server_key,"")

	
        def getDBBackupDir(self):
                self.db_backupdir = self.getBaseDir() + "database_backup" + "/"  + "database_%s/"%time.strftime("%d_%m_%Y_%H_%M_%S",time.localtime())
                return self.db_backupdir

	def getDBHost(self):
		return DB_HOST_MAP.get(self.server_key,"")

	
	def getBaseDir(self):
		return "/home/%s/"%self.user
	
        def getDBBackup(self,db_name,dbuser,password):
                try:
                        db_host = self.getDBHost()
                        sql_file = self.db_backupdir + "/" + db_name + "__" + time.strftime("%d_%m_%Y_%H_%M_%S",time.localtime()) + ".sql"
                        dump_database(db_host,db_name,sql_file,dbuser,password)        
	        except Exception,msg:
                        print "Exception in getDBBackup"
                        print msg
                        
        def executeDBFile(self,dbname,dbuser,password,file):
                try:
                       sqldumpfile = self.db_backupdir + "/" + file
                       db_host = self.getDBHost()
                       execute_database_script(db_host,dbname,sqldumpfile,dbuser,password)
	        except Exception,msg:
                        print "Exception in executeDBFile"
                        print msg       
	
	


