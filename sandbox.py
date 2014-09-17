#!/usr/bin/env python
#
##########################################################

from fabric.api import *
import string
import os,time
import deployctrl
import sys
from sshconnectionmgr import *
import getpass
import sandboxconfigctrl
from hgutil import *


class SandBoxDeploy(object):
        
        def __init__(self,host,user,issue_no,server_key):
                self.host= host
                self.user = user
                self.issue_no = issue_no
                self.server_key = server_key
                self.makeConfObj = sandboxconfigctrl.SandBoxConfigCtrl(self.user,self.host,self.issue_no,self.server_key)
        
        
        
        def deploy_sandbox_app(self):
                """this is for integration_app  
                        """
                try:
                        self.makeConfObj.makeSandBoxDir()
                        self.makeConfObj.cloneRepo()
                except Exception,msg:
                        print "Exception in deploy_sandbox_app"
                        print msg

        def deploy_sandbox_db(self):
                """Integration DataBase Server  deployment"""

                try:
                        
                        
                        answer = prompt("Do you want to execute Database scripts: Answer as yes or no ")
                        if answer.strip().lower() == "no":
                                sys.exit()
                        elif answer.strip().lower().find("yes") == -1:
                                sys.exit()
                        
                        self.makeConfObj.cloneDBRepo()
                        sql_fileList = self.makeConfObj.getListOfFiles()

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
                                        print " Please Enter Username of Database."
                                        dbuser = prompt("Enter Database Username:  ")

                                if len(password.strip()) <= 0:
                                        print " Please Enter password of Database."
                                        password = getpass.getpass("Enter Database password: ")
                                ext = "sql"
                                file_name = file.strip(".sql")
                                self.makeConfObj.getDBBackup(db_name,dbuser,password)
                                self.makeConfObj.executeDBFile(db_name,dbuser,password,file)
                except Exception,msg:
                        print "Exception in deploy_integration_db"
                        print msg

def deploySandbox(host,user,issue_no,server_key):
        
        deployObj = SandBoxDeploy(host,user,issue_no,server_key)
        deployObj.deploy_sandbox_app()
        deployObj.deploy_sandbox_db()



if __name__=="__main__":
        
        
        if len(sys.argv) < 3:
                print """
                        Please use sandbox.py  serverkey host  user
                        For Example .  sandbox.py integration issue78 dev.mydemo.com mydemo_development    or
                                       sandbox.py staging issue78 dev.mydemo.com mydemo_development
                                       sandbox.py production issue78 dev.mydemo.com mydemo_development
                                       
                             Serverkey integration  for Devlopment Server
                                       staging  for Staing Server
                                       production  for Production Server
                                       
                             Default Host : dev.mydemo.com
                             Default User : mydemo_development
                      """
                sys.exit()
        serverKey = sys.argv[1]
        if serverKey not in ["integration","production","staging"]:
                print """
                        Please use Serverkey as integration  for Development Server
                                       staging  for Staing Server
                                       production  for Production Server

                     """
        issue_no = sys.argv[2]
        try:
                env.hosts= [sys.argv[3]]
                env.host_string = sys.argv[3]
        except:
                env.host_string  = "dev.mydemo.com"
        try:
                env.user = sys.argv[4]
        except:
                env.user = "mydemo_development"
        deploySandbox(env.host_string,env.user,issue_no,serverKey)
        
                
        
        
        


        
                        
