from app import db
from flask_sqlalchemy import SQLAlchemy
    

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True)
    password = db.Column(db.String(15))
    cars = db.relationship('Car', backref='users_car', lazy=True)


class Popularity(db.Model):
    __tablename__ = 'popularity'
    pop_id = db.Column(db.Integer, primary_key = True)
    pop_num = db.Column(db.Integer)
    pops = db.relationship('Car', backref='car_pop')


class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key = True)
    region = db.Column(db.String(60), nullable=False)
    make = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False, unique=True)
    model_year = db.Column(db.Integer, nullable=False)
    trans = db.Column(db.String(60), nullable=False)
    hp_amount = db.Column(db.Integer, nullable=False)
    torque_amount = db.Column(db.Integer, nullable=False)
    drivetrain = db.Column(db.String(30), nullable=False)
    chassy_desc = db.Column(db.String(30), nullable=False)
    accel_time = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String(250))
    upload_by = db.Column(db.String(30), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    pop_id = db.Column(db.Integer, db.ForeignKey('popularity.pop_id'))
    
    
    
#db.drop_all()
#db.create_all()    