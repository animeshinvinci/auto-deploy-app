#!/usr/bin/env python
from fabric.api import *
import os
import string
from config import *


def clone_repo(repo_url,repo_dir=""):
	run("hg clone %s  %s"%(repo_url,repo_dir))


def getrevision(repo_dir):
	
	version = -1
	try:
		with cd(repo_dir):

			ret = run("hg head")
			versionlist = ret.split("\n")
			if len(versionlist) > 0:
				version_list = versionlist[0].split(":  ")[1].split(":")
				version = version_list[0].strip()

	except :
		 try:
		 	versionfileList = get(repo_dir + ".hg/tags.cache")
			if len(versionfileList) > 0:
				f= open(versionfileList[0])
				ver_str = f.read()
				version = ver_str.split()[0].strip()
		 except :
			try:
		 		versionfileList = get(repo_dir + ".hg/cache/tags")
				if len(versionfileList) > 0:
					f = open(versionfileList[0])
					ver_str = f.read()
					version = ver_str.split()[0].strip()
			except:
				pass
	return version

def pull_repo():
	pass

	






