#!/usr/bin/env python

from fabric.api import *
import string
import os,time
import deployctrl
import sys
from sshconnectionmgr import *
import getpass
import configctrl

class deploy(object):
	
	def __init__(self,host,user,server_key):
		self.host= host
		self.user = user
		self.server_key = server_key
		self.makeConfObj = configctrl.ConfigCtrl(self.user,self.host,self.server_key)
	
	
	
	def deploy_integration_app(self):
		"""this is for integration_app	
			"""
		try:
			
			APP_TEMP_DIR = self.makeConfObj.getAppTempDIR()
			APP_SYMLINK_DIR = self.makeConfObj.getAppSymLinkDIR()
			APP_REPO_URL = self.makeConfObj.getAppReporUrl()
			dep_ctrl = deployctrl.deployCtrl(APP_TEMP_DIR,APP_SYMLINK_DIR,APP_REPO_URL)

			dep_ctrl.clone_repo()
			print "Repo Cloning Done."

			dep_ctrl.renamedirWithLatestRev()

			dep_ctrl.makesymlink()

		except Exception,msg:
			print "Exception in deploy_integration_app"
			print msg

	def deploy_integration_db(self):
		"""Integration DataBase Server  deployment"""

		try:
			
			DB_TEMP_DIR = self.makeConfObj.getDBTempDIR()
			DB_SYMLINK_DIR = self.makeConfObj.getDBSymLinkDIR()
			DB_REPO_URL = self.makeConfObj.getDBReporUrl()
			DB_BACKUP_DIR = self.makeConfObj.getDBBackupDir()
			DATABASE_HOST = self.makeConfObj.getDBHost()
			
			dep_ctrl = deployctrl.deployCtrl(DB_TEMP_DIR,DB_SYMLINK_DIR,DB_REPO_URL)
			dep_ctrl.clone_repo()
			print "Repo Cloning Done."

			dep_ctrl.renamedirWithLatestRev()
			dep_ctrl.makesymlink()
			answer = prompt("Do you want to execute Database scripts: Answer as yes or no ")
			if answer.strip().lower() == "no":
				sys.exit()
			elif answer.strip().lower().find("yes") == -1:
				sys.exit()
			sql_fileList = dep_ctrl.getListOfFiles()

			for file in sql_fileList:
				answer = prompt("Going to execute  %s: Answer as yes or no "%file)
				if answer.strip().lower() == "no":
					continue
				elif answer.strip().lower().find("yes") == -1:
					continue
				elif answer.strip() not in ["yes","no"]:
					print "Wrong answer"
					continue
				db_name = prompt("Enter Database Name:  ")
				password = ""
				dbuser = ""

				dbuser = prompt("Enter Database Username:  ")
				password = getpass.getpass("Enter Database password: ")

				if len(dbuser.strip()) <= 0:
					print "	Please Enter Username of Database."
					dbuser = prompt("Enter Database Username:  ")

				if len(password.strip()) <= 0:
					print "	Please Enter password of Database."
					password = getpass.getpass("Enter Database password: ")
				rev = dep_ctrl.getCurrentRevno()
				ext = "sql"
				file_name = file.strip(".sql")
				time_Str = str(time.ctime()).replace(" ","_").replace(":","_")
				temp_bakup_dir = DB_BACKUP_DIR + os.sep + "%s__%s__%s"%(file_name,str(rev),time_Str)
				mkdir(temp_bakup_dir)

				sql_file = temp_bakup_dir + os.sep + file_name + "__%s__%s"%(str(rev),time_Str) + "." + ext
				#print db_name,"sql_filesql_file",file
				#print sql_file
				dump_database(DATABASE_HOST,db_name,sql_file,dbuser,password)
				print "Backup of  Database ( %s )  has completed sucessfully. File saved in location  %s"%(db_name,sql_file)
				script_file = dep_ctrl.base_dir%(str(rev)) + "%s"%file
				#print "script_filescript_file"
				#print script_file
				execute_database_script(DATABASE_HOST,db_name,script_file,dbuser,password)
				print "Database %s Updated   sucessfully ."%db_name
		except Exception,msg:
			print "Exception in deploy_integration_db"
			print msg

	
	
	
	
	def getDatabaseExecution(self):
		"""
			"""
		try:
			db_sqlfiles = dep_ctrl.getListOfFiles()
			sql_str  = "Please select no to execute sql file"
			no = 1
			sql_file = ""
			database_name = ""
			for sql_fl in db_sqlfiles:
				sql_str = sql_str + "\n" + str(no) + " : %s"%sql_fl
			
			sql_file_no = prompt(" %s : "%sql_str)
			sql_file_no = int(sql_file_no)
			if sql_file_no > len(db_sqlfiles)  or sql_file_no >= 0 :
				print "	Please select proper number"
				sql_file_no = prompt(" %s : "%sql_str)
				sql_file_no = int(sql_file_no)
			try:
				sql_file = db_sqlfiles[sql_file_no]	
			except:
				print "You have not selected proper sql file"
				return
				
			database_name = prompt("Enter Database Name:  ")
			
			password = ""
			dbuser = ""
			dbuser = prompt("Enter Database Username:  ")
			password = getpass.getpass("Enter Database password: ")

			if len(dbuser.strip()) <= 0:
				print "	Please Enter Username of Database."
				dbuser = prompt("Enter Database Username:  ")

			if len(password.strip()) <= 0:
				print "	Please Enter password of Database."
				password = getpass.getpass("Enter Database password: ")
		
			return sql_file,database_name,dbuser,password
		except Exception,msg:
			print "Exception in getDatabaseExecution"
			print msg

	
	
def deployIntegration(host,user,server_key):
	
	deployObj = deploy(host,user,server_key)
	deployObj.deploy_integration_app()
	deployObj.deploy_integration_db()



if __name__=="__main__":
	
	
	if len(sys.argv) != 4:
		print """
			Please use deploy.py  serverkey host  user
		      	For Example .  deploy.py integration xyz.com root    or
		      		       deploy.py staging xyz.com root
		      		       deploy.py production xyz.com root
		      		       
		             Serverkey integration  for Devlopment Server
				       staging  for Staing Server
				       production  for Production Server
		      """
		sys.exit()
	serverKey = sys.argv[1]
	if serverKey not in ["integration","production","staging"]:
		print """
			Please use Serverkey as integration  for Development Server
				       staging  for Staing Server
				       production  for Production Server

	      	     """
	env.hosts= [sys.argv[2]]
	env.host_string = sys.argv[2]
	env.user = sys.argv[3]
	deployIntegration(env.host_string,env.user,serverKey)
	
		
	
	
	


	
			
