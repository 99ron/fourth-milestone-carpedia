from app import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True)
    password = db.Column(db.String(15))
    cars = db.relationship('Car', backref='users_car', lazy=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
        
       
class Popularity(db.Model):
    __tablename__ = 'popularity'
    id = db.Column(db.Integer, primary_key = True)
    pop_num = db.Column(db.Integer)
    pops = db.relationship('Car', backref='car_pop')


class Car(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key = True)
    region = db.Column(db.String(60), nullable=False)
    make = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(30), nullable=False)
    model_year = db.Column(db.Integer, nullable=False)
    trans = db.Column(db.String(60), nullable=False)
    hp_amount = db.Column(db.Integer, nullable=False)
    torque_amount = db.Column(db.Integer, nullable=False)
    drivetrain = db.Column(db.String(30), nullable=False)
    chassy_desc = db.Column(db.String(30), nullable=False)
    accel_time = db.Column(db.Integer, nullable=False)
    car_desc = db.Column(db.String(255), nullable=True)
    img_url = db.Column(db.String(250))
    upload_by = db.Column(db.String(30), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pop_id = db.Column(db.Integer, db.ForeignKey('popularity.id'))
    
# Prep populating data into the database # 
'''
# Add a user #
new_user = Users(username='Aaron', password='Aaron')
db.session.add(new_user)
db.session.commit()

# Add a few cars #
car_jdm_1 = Car(region='JDM',
                 make='Toyota',
                 model='Supra',
                 model_year='1996',
                 trans='Auto',
                 hp_amount='320',
                 torque_amount='320',
                 drivetrain='RWD',
                 chassy_desc='Coupe',
                 accel_time='4.8',
                 car_desc='Beast from the East with the 2jz!',
                 upload_by='Aaron')

car_jdm_2 = Car(region='JDM',
                 make='Nissan',
                 model='Skyline',
                 model_year='1994',
                 trans='Manual',
                 hp_amount='320',
                 torque_amount='320',
                 drivetrain='AWD',
                 chassy_desc='Coupe',
                 accel_time='4.2',
                 car_desc='Known for its iconic RB26.',
                 upload_by='Aaron')

car_jdm_3 = Car(region='JDM',
                 make='Nissan',
                 model='300ZX',
                 model_year='1992',
                 trans='Manual',
                 hp_amount='320',
                 torque_amount='320',
                 drivetrain='RWD',
                 chassy_desc='Coupe',
                 accel_time='4.9',
                 car_desc='Wedgelike shape like a lambo at its time.',
                 upload_by='Aaron')   

car_jdm_4 = Car(region='JDM',
                 make='Honda',
                 model='Civic Type R',
                 model_year='2004',
                 trans='Manual',
                 hp_amount='220',
                 torque_amount='140',
                 drivetrain='FWD',
                 chassy_desc='Hatchback',
                 accel_time='6.2',
                 car_desc='Loves to hit the limiter.',
                 upload_by='Aaron')

car_usdm_1 = Car(region='USDM',
                 make='Corvette',
                 model='ZR1',
                 model_year='2019',
                 trans='SemiA',
                 hp_amount='755',
                 torque_amount='715',
                 drivetrain='RWD',
                 chassy_desc='Coupe',
                 accel_time='2.8',
                 car_desc='Huge american muscle, so much power!',
                 upload_by='Aaron')

car_usdm_2 = Car(region='USDM',
                 make='Chevrolet',
                 model='Camaro',
                 model_year='2012',
                 trans='SemiA',
                 hp_amount='426',
                 torque_amount='400',
                 drivetrain='RWD',
                 chassy_desc='Coupe',
                 accel_time='4.4',
                 car_desc='Classic camaro power right here!',
                 upload_by='Aaron')

car_usdm_3 = Car(region='USDM',
                 make='Ford',
                 model='Focus',
                 model_year='2012',
                 trans='Manual',
                 hp_amount='300',
                 torque_amount='270',
                 drivetrain='FWD',
                 chassy_desc='Hatchback',
                 accel_time='6.4',
                 car_desc='Hatchback fun right here!',
                 upload_by='Aaron')

db.session.add(car_jdm_1)
db.session.add(car_jdm_2)
db.session.add(car_jdm_3)
db.session.add(car_jdm_4)
db.session.add(car_usdm_1)
db.session.add(car_usdm_2)
db.session.add(car_usdm_3)
db.session.commit()
'''
#db.drop_all()
#db.create_all()    
