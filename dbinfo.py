# Trying to sort what I will need.

import os
import pymysql
from flask import session
import sqlalchemy as db




# Local Database Details
user = os.getenv('C9-USER')
password = ''

# Local Database connection details for testing environment.
'''
def local():
    connection = pymysql.connect(
        host="eu-cdbr-west-02.cleardb.net",
        user="bd6203f445759d",
        password="3f8eca2f",
        db="heroku_1146a0b312400c5")
    return connection
'''
'''
def remote():
    connection = pymysql.connect(
        host="eu-cdbr-west-02.cleardb.net",
        user="bd6203f445759d",
        password="3f8eca2f",
        db="heroku_1146a0b312400c5")
    return connection
'''
    
# Set connection to be on local database or remote

local = db






