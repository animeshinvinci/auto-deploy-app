#!/usr/bin/env python
########################################################################
#
# This file will perform all automation steps to deploy a project.
#
#
#
#########################################################################



import time
from fabric.api import *
import os
from sshconnectionmgr import *
from hgutil import *
import sys

class deployCtrl(object):
	
	def __init__(self,base_dir,symlink_dir,repo_url,previous_version=''):
		self.base_dir = base_dir
		self.repo_url = repo_url
		self.symlink_dir = symlink_dir
		self.temp_dir = ""
		self.previous_version=previous_version
		self.currentversion = ''
		
	def clone_repo(self):
		"""this function will create a temp dir and clone repo
			"""
		try:
			self.temp_dir = self.base_dir%str(int(time.time()))
			mkdir(self.temp_dir)
			clone_repo(self.repo_url,self.temp_dir)
		except Exception,msg:
			print "Exception in clone_repo"
			print msg
			
	def getCurrentRevno(self):
		"""this function will get latest revision no.
			"""
		try:
			if self.currentversion:
				return self.currentversion
			version = getrevision(self.temp_dir)
		    	self.currentversion = version
			return version
		except Exception,msg:
			print "Exception in getCurrentRevno"
			print msg
		return -1
			
	def renamedirWithLatestRev(self):
		"""This function will responsile for renaming dir
			"""
		try:
			
			revision = self.getCurrentRevno()
			if revision == -1:
				print "Repository do not have any files so exiting from execution."
				sys.exit()
			elif revision != -1:
				dir_with_rev = self.base_dir%(str(revision))
				old_dir = self.temp_dir
			
			else:
				old_dir = self.symlink_dir
			removesymlink(old_dir,dir_with_rev)
			renamedir(old_dir,dir_with_rev)
		except Exception,msg:
			print "Exception in renamedir"
			print msg
	
	def makesymlink(self):
		try:
			revision = self.getCurrentRevno()
			if revision == -1:
				print "Repository do not have any files so exiting from execution."
				sys.exit()			
			elif revision != -1:
				if not self.previous_version:
					pre_rev = int(revision) - 1
					dir_with_pre_rev = self.base_dir%(str(pre_rev))
				else:
					dir_with_pre_rev = self.base_dir%(str(previous_version))

				dir_with_rev = self.base_dir%(str(revision))
				symlinkdir = self.symlink_dir	
			
				removesymlink(dir_with_pre_rev,symlinkdir)
				makesymlink(dir_with_rev,symlinkdir)
			else:
				print "Revision no is %s"%str(revision)
				print "Symlink not created."
		except Exception,msg:
			print "Exception in makesymlink"
			print msg
			
	def getListOfFiles(self):
		
		try:
			revision = self.getCurrentRevno()
			dir_with_rev = self.base_dir%(str(revision))
			dirList = run("ls %s"%dir_with_rev)
			sql_files = filter(lambda a:a.strip(),dirList.split(" "))
			return sql_files
		except Exception,msg:
			print "Exception in makesymlink"
			print msg
		
	
		
		
	
	


	


