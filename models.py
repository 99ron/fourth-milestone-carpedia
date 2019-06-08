from app import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique = True)
    password = db.Column(db.String(15))
    liked = db.relationship('Popularity', foreign_keys='Popularity.user_id', backref='user', lazy='dynamic')
    
    
    def like_car(self, car):
        if not self.has_liked_car(car):
            vote = Popularity.query.filter(Popularity.car_id == car.id).first()
            vote =+1
            like = Popularity(user_id=self.id, car_id=car.id, likes=vote)
            db.session.add(like)
            db.session.commit()
            
    def unlike_car(self, car):
        if self.has_liked_car(car):
            Popularity.query.filter_by(
                user_id=self.id,
                car_id=car.id).delete()
            db.session.commit()
    
    def has_liked_car(self, car):
        return Popularity.query.filter(
            Popularity.user_id == self.id,
            Popularity.car_id == car.id).count() > 0

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
    likes = db.Column(db.Integer)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


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
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    likes = db.relationship('Popularity', backref='car', lazy='dynamic')
    
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
                 img_url="/static/images/vehicles/toyota-super-05.jpg",
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
                 img_url="/static/images/vehicles/no_img.jpg",
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
                 img_url="/static/images/vehicles/no_img.jpg",
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
                 img_url="/static/images/vehicles/no_img.jpg",
                 upload_by='Aaron')

car_usdm_1 = Car(region='USDM',
                 make='Corvette',
                 model='ZR1',
                 model_year='2019',
                 trans='Semi-Auto',
                 hp_amount='755',
                 torque_amount='715',
                 drivetrain='RWD',
                 chassy_desc='Coupe',
                 accel_time='2.8',
                 car_desc='Huge american muscle, so much power!',
                 img_url="/static/images/vehicles/no_img.jpg",
                 upload_by='Aaron')

car_usdm_2 = Car(region='USDM',
                 make='Chevrolet',
                 model='Camaro',
                 model_year='2012',
                 trans='Semi-Auto',
                 hp_amount='426',
                 torque_amount='400',
                 drivetrain='RWD',
                 chassy_desc='Coupe',
                 accel_time='4.4',
                 car_desc='Classic camaro power right here!',
                 img_url="/static/images/vehicles/no_img.jpg",
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
                 img_url="/static/images/vehicles/no_img.jpg",
                 upload_by='Aaron')

car_euro_1 = Car(region='Euro',
                 make='Aston',
                 model='Martin',
                 model_year='1996',
                 trans='Manual',
                 hp_amount='400',
                 torque_amount='350',
                 drivetrain='RWD',
                 chassy_desc='Coupe',
                 accel_time='5.4',
                 car_desc='Old classic that just lived up to its reputation!',
                 img_url="/static/images/vehicles/aston-martin.jpg",
                 upload_by='Aaron')

db.session.add(car_jdm_1)
db.session.add(car_jdm_2)
db.session.add(car_jdm_3)
db.session.add(car_jdm_4)
db.session.add(car_usdm_1)
db.session.add(car_usdm_2)
db.session.add(car_usdm_3)
db.session.add(car_euro_1)
db.session.commit()

#db.drop_all()
#db.create_all()    
'''