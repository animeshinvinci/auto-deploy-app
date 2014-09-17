#!/usr/bin/env python

from fabric.api import *
import time
import os
import string
from  config import *

def sshconnection():
	env.host_string = "%s:%s" % (HOST, PORT)
	env.user=USER
	env.hosts= [HOST]
	
def mkdir(dirpath):
	run("mkdir -p %s"%dirpath)
	
def makesymlink(curdir,symlinkdir):
	try:
		run("ln -s %s %s"%(curdir,symlinkdir))
	except:
		pass
def removesymlink(old_dir,symlinkdir):
	try:
		#run('cd %s'%symlinkdir)
		#with cd('%s'%symlinkdir):
		try:
			run("rm  -rf  %s"%symlinkdir)
		except:
			pass
		try:
			run("rm  -rf  %s/"%symlinkdir)
		except:
			pass
		#run("find %s -type l -delete"%symlinkdir)
	except:
		pass
def dump_database(db_host,dbname,sqldumpfile,dbuser,password):
    run('mysqldump -h %s -u %s -p%s %s > %s' % (db_host,dbuser,
        password,
        dbname,sqldumpfile       
    ))
    
def execute_database_script(db_host,dbname,sqldumpfile,dbuser,password):
	run('mysql -h %s -u %s -p%s %s < %s' % (db_host,dbuser,
	        password,
	        dbname,sqldumpfile       
   	 ))

def renamedir(old_dir,new_dir):
	run("mv %s  %s"%(old_dir,new_dir))

	
	

	
	
	
	
	


