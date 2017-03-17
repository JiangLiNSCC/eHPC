#import urllib2 , urllib
import json
import time
import random , string
import re
from client6 import newtAPIClient as Client
import six
import logging
import logging.config
import os
logging.config.fileConfig("logger.conf")
logger = logging.getLogger("test")

if six.PY2 :
    import ConfigParser
elif six.PY3 :
    import configparser as ConfigParser
cf = ConfigParser.ConfigParser() 
cf.read("../../config/test.conf")


base_url = cf.get("test","url")
login_data = {"username": cf.get("test","username") , "password" :  cf.get("test","password")}
#mc = Client( base_url = base_url  ,headers ={} , login_cookie = None , login_data = login_data)
machine_name = cf.get("test","machine")
if os.environ.get("DEBUG" , None):
    logger.setLevel(logging.DEBUG)

import unittest
class BaseTest(unittest.TestCase ):
    
    def setUp(self):
        self.mc = Client( base_url = base_url  ,headers ={} , login_cookie = None , login_data = login_data)
        self.logger = logger
        self.login_data = login_data
        self.username = login_data["username"]
        self.machine = machine_name
        pass
    
    def tearDown(self):
        pass
  

