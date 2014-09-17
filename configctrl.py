import os
import time
from config import *

class ConfigCtrl(object):

	def __init__(self,user,host,server_key):
		self.user = user
		self.host = host
		self.server_key = server_key
	
	def getAppTempDIR(self):
		return self.getBaseDir() + "webapp_%s/"
	
	
	def getAppSymLinkDIR(self):
		return self.getBaseDir() + "%s"%self.host

	def getAppReporUrl(self):
		return REPO_URL_MAP.get(self.server_key,"")
		 

	def getDBTempDIR(self):
		return self.getBaseDir() + "database_%s/"
	

	def getDBSymLinkDIR(self):
		return self.getBaseDir() + "database"

	def getDBReporUrl(self):
		return DB_REPO_URL_MAP.get(self.server_key,"")

	def getDBBackupDir(self):
		return self.getBaseDir() + "database_backup"


	def getDBHost(self):
		return DB_HOST_MAP.get(self.server_key,"")

	
	def getBaseDir(self):
		return "/home/%s/"%self.user
	
	
	
	
	
	
	
	
	


