# Test app.py 
import os
import sys
import json
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from forms import LoginForm, RegisterForm, CarToDatabase, FilterCars, CsrfProtect, EditCar
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, request, url_for, flash, session, jsonify
from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy import func
from werkzeug.utils import secure_filename
from models import *

UPLOAD_FOLDER = './static/images/vehicles'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# DB_URI = 'mysqldb://bd6203f445759d:3f8eca2f@eu-cdbr-west-02.cleardb.net/heroku_1146a0b312400c5?reconnect=true'

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager(app)
login_manager.login_view = 'login'
CsrfProtect(app)
db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(username):
    return Users.query.get(int(username))

@app.route('/')
@app.route('/login')
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return render_template('login.html', form=form)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')
       

@app.route('/register')
def index():
    form = LoginForm()
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    form = LoginForm()
    
    # Checks that a session is active and if so sets it to False
    # If there's no session and a user tries to log out it'll
    # take you to the login screen with a message.
    
    if current_user.is_authenticated == False:
        flash("You're not logged in.")
        return render_template('login.html', form=form)
    else:
        user = current_user
        user.is_authenticated = False
        logout_user()
    return redirect(url_for('login'))
    #return render_template('login.html', form=form)
    

@app.route('/check-user-credentials', methods=['GET','POST'])
def checkuser():
    form = LoginForm()
    
    if request.method == "GET":
        return render_template('login.html', form=form)
        
    # Checks the users credentials against the 'Users' table.
    # If none match then flashes a message and asks to try again.
    
    if request.method == "POST":
        user = Users.query.filter_by(username = form.username.data).first()
        credentials = Users.query.filter_by(username = form.username.data, password = form.password.data).first()
        if user:
            if credentials:
                user.is_authenticated = True
                login_user(user, remember=False)
                return redirect((url_for('home')))
            else:
                flash('Wrong password.')
                return render_template('login.html', form=form)
        else:
            flash("Username doesn't exist.")
            return render_template('login.html', form=form)
        return redirect(url_for('home'))


@app.route('/register-user/', methods=['GET', 'POST'])
def register():
	
	# This attempts to create a new user in the 'Users' table.
	# If the user already exists it'll flash a message and ask to try again.
	
    form = RegisterForm()
    try:
        if request.method == 'POST':
            new_user = Users(username=form.username.data, password=form.password.data)
            if not new_user:
                flash('This user already exists.')
                return render_template('register.html', form=form)
            else:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
    except:
        flash('Error Occured, try again.')
        return render_template('register.html', form=form)
    
@app.route('/add-vehicle')
@login_required
def addVehicle():
    form = CarToDatabase()
    
    if request.method == 'POST' and form.validate_on_submit():
        file_img = form.car_img.data
        
        if file_img and allowed_file(file_img.filename):
            filename = secure_filename(file_img.filename)
            car_img_url = '/static/images/vehicles/' + filename
            try:
                file_img.save(os.path.join( UPLOAD_FOLDER, filename))
            except:
                return
        else:
            car_img_url = '/static/images/vehicles/no_img.jpg'
        
        add_car = Car(region=form.region.data,
                      make=form.make.data,
                      model=form.model.data,
                      model_year=form.year.data,
                      trans=form.trans.data,
                      hp_amount=form.hp.data,
                      torque_amount=form.torque.data,
                      drivetrain=form.drive.data,
                      chassy_desc=form.body.data,
                      car_desc=form.car_desc.data,
                      accel_time=form.accel.data,
                      img_url=car_img_url,
                      upload_by=current_user.username)
                      
        try:
            db.session.add(add_car)
            db.session.commit()
            flash('Vehicle added to database.')
            return redirect(url_for('filter'))
        except:
            flash("This vehicle couldn't be added, try again.")
            return redirect(url_for('addVehicle'))
    else:
        form = CarToDatabase()
        return render_template('add-vehicle.html', form=form)

@app.route('/filter-cars', methods=['GET', 'POST'])
#@login_required
def filter():
    cars = Car.query.all()
    form = FilterCars()
    region = form.region.data
    drive = form.drive.data
    query = form.query.data

    # If POST this then validates the form and pushes the request.
    if request.method == 'POST' and form.validate_on_submit():
    
        if region != "All" and drive != "All":
            cars=car_region_drive(region, drive, query)
            
        if region != "All" and drive == "All":
            cars = car_region(region, query)

        if region == "All" and drive != "All":
            cars = car_drive(drive, query)
            
        if region == "All" and drive == "All":
            cars= car_all(query)

        return render_template('filter-cars.html', form=form, cars=cars)

    # When the page loads it requests all cars from the database to display.
    return render_template('filter-cars.html', form=form, cars=cars)


@app.route('/vehicle/<int:car_id>', methods=['GET'])
#@login_required
def vehicleInfo(car_id):
    vehicles=Car.query.filter_by(id=car_id).first()
    return render_template("vehicle-info.html", vehicles=vehicles) 



@app.route('/vehicle/edit/<int:car_id>/<vehicleName>', methods=['POST', 'GET'])
#@login_required
def editVehicle(car_id, vehicleName):
    form = EditCar()
    vehicles=Car.query.filter_by(id=car_id).one()
    
    if request.method == 'GET':
        
        form.region.data = vehicles.region
        form.make.data = vehicles.make
        form.model.data = vehicles.model
        form.hp.data = vehicles.hp_amount
        form.torque.data = vehicles.torque_amount
        form.year.data = vehicles.model_year
        form.trans.data = vehicles.trans
        form.drive.data = vehicles.drivetrain
        form.body.data = vehicles.chassy_desc
        form.accel.data = vehicles.accel_time
        form.car_desc.data = vehicles.car_desc
        
        
        return render_template("edit-vehicle.html", form=form, vehicles=vehicles)

    if request.method == 'POST':
        
        vehicleImage = vehicles.img_url 
        file_img = form.car_img.data
        
        if file_img and allowed_file(file_img.filename):
            filename = secure_filename(file_img.filename)
            car_img_url = '/static/images/vehicles/' + filename
            try:
                file_img.save(os.path.join( UPLOAD_FOLDER, filename))
            except:
                return
        else:
            car_img_url = vehicleImage
           
        vehicles.region = form.region.data
        vehicles.make = form.make.data
        vehicles.model = form.model.data
        vehicles.hp_amount = form.hp.data
        vehicles.torque_amount = form.torque.data
        vehicles.model_year = form.year.data
        vehicles.trans = form.trans.data
        vehicles.drivetrain = form.drive.data
        vehicles.chassy_desc = form.body.data
        vehicles.accel_time = form.accel.data
        vehicles.car_desc = form.car_desc.data
        vehicles.img_url = car_img_url
    
    try:
        form.populate_obj(vehicles)
        db.session.merge(vehicles)
        db.session.commit()
        flash('Vehicle updated sucessfully!')
        return redirect(url_for('filter'))
        
    except:
        flash('Invalid Input.')
        return render_template("edit-vehicle.html", form=form, vehicles=vehicles) 
        
@app.route('/delete/<int:car_id>', methods=['GET']) 
@login_required
def deleteVehicle(car_id):
    if request.method == 'GET':
        
        try:
            car_id = db.session.query(Car).filter_by(id=car_id).first()
            db.session.delete(car_id)
            db.session.commit()
            flash('Vehicle successfully deleted.')
            return redirect(url_for('filter'))
        except:
            db.session.rollback()
            flash('Error occured, try again.')
            return redirect(url_for('filter'))

@app.route('/summary')
#@login_required
def summary():
    return render_template('summary.html')

@app.route('/summary/data')
def summaryData():
    cars = Car.query.all()
    
    USDM = 0
    USDMN = []
    JDM = 0
    JDMN = []
    Euro = 0
    EuroN = []
    Manual = 0
    ManualN = []
    SemiAuto = 0
    SemiAutoN = []
    Auto = 0
    AutoN = [] 
    Sequential = 0
    SequentialN = []
    LT4 = 0
    LT4N = []
    LT7 = 0
    LT7N = []
    MT7 = 0
    MT7N = []
    

    for car in cars:
        
        if car.region == 'USDM':
            USDM +=1
            USDMN.append([' ' + car.make + ' ' + car.model])
        elif car.region == 'JDM':
            JDM +=1
            JDMN.append([' ' + car.make + ' ' + car.model])
        else:
            Euro +=1
            EuroN.append([' ' + car.make + ' ' + car.model])
            
        if car.trans  == 'Manual':
            Manual +=1
            ManualN.append([' ' + car.make + ' ' + car.model])
        elif car.trans == 'Semi-Auto':
            SemiAuto +=1
            SemiAutoN.append([' ' + car.make + ' ' + car.model])
        elif car.trans == 'Auto':
            Auto +=1
            AutoN.append([' ' + car.make + ' ' + car.model])
        else:
            Sequential +=1
            SequentialN.append([' ' + car.make + ' ' + car.model])
    
        if car.accel_time <= 4:
            LT4 +=1
            LT4N.append([' ' + car.make + ' ' + car.model])
        elif car.accel_time <= 7:
            LT7 +=1
            LT7N.append([' ' + car.make + ' ' + car.model])
        else:
            MT7 +=1
            MT7N.append([' ' + car.make + ' ' + car.model])
    
    jsonData = [{'USDM' : USDM , 'JDM' : JDM, 'Euro' : Euro, 'USDMN' : USDMN, 'JDMN' : JDMN, 'EuroN' : EuroN }, {'Manual': Manual, 'SemiAuto': SemiAuto, 'Auto': Auto, 'Sequential': Sequential, 'ManualN' : ManualN, 'SemiAutoN' : SemiAutoN, 'AutoN' : AutoN, 'SequentialN' : SequentialN}, {'LT4' : LT4, 'LT7': LT7, 'MT7': MT7, 'LT4N' : LT4N, 'LT7N' : LT7N, 'MT7N' : MT7N }]
    return jsonify(jsonData)
    

@app.route('/like/<int:car_id>/<action>')
@login_required
def like(car_id, action):
    car = Car.query.filter_by(id=car_id).first_or_404()
    if action == 'like':
        current_user.like_car(car)
        
        flash('Like Added')
    if action == 'unlike':
        current_user.unlike_car(car)
        
        flash('Like Removed')
    return redirect(url_for('vehicleInfo', car_id=car_id))
    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
debug=True)
