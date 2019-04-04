from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('sqlite:///site.db', echo=True)



class Users(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True)
    password = db.Column(db.String(15))

    def __init__(self, username, password):
        self.username = username
        self.password = password


