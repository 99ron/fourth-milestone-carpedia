# Trying to sort what I will need.

import os
import pymysql
from flask import session

# Local Database Details
user = os.getenv('C9-USER')
password = ''

# Set Login Name
def setLogin(value):
    session['user'] = value

# Local Database connection details for testing environment.

def local():
    connection = pymysql.connect(
        host='localhost',
        user=user,
        password=password,
        db='testDB')
    return connection