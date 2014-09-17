#!/usr/bin/env python
from fabric.api import *


APP_REPO_URL = "https://mydemo@github.org/mydemo/integration_webapp"
DB_REPO_URL= "https://mydemo@github.org/mydemo/integration_database"
DATABASE_HOST = "database.mydemo.com"
STAG_DATABASE_HOST = "database.mydemo.com"
PROD_DATABASE_HOST = "database.mydemo.com"
PROD_APP_REPO_URL = "https://mydemo@github.org/mydemo/production_webapp"
STAG_APP_REPO_URL = "https://mydemo@github.org/mydemo/staging_webapp"
PROD_DB_REPO_URL= "https://mydemo@github.org/mydemo/production_database"
STAG_DB_REPO_URL= "https://mydemo@github.org/mydemo/staging_database"
REPO_URL_MAP = { 
		 "integration": APP_REPO_URL,
		 "staging":STAG_APP_REPO_URL,
		 "production":PROD_APP_REPO_URL
		 }
	 
DB_REPO_URL_MAP = { 
		 "integration": DB_REPO_URL,
		 "staging":STAG_DB_REPO_URL,
		 "production":PROD_DB_REPO_URL
		 }
DB_HOST_MAP = { 
		 "integration": DATABASE_HOST,
		 "staging":STAG_DATABASE_HOST,
		 "production":PROD_DATABASE_HOST
		 }
PRE_DEP_VER= 0
