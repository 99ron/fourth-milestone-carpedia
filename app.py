# Test app.py 
import os
import sys
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from forms import LoginForm, RegisterForm, CarToDatabase, FilterCars, CsrfProtect
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, request, url_for, flash, session
from sqlalchemy.orm import sessionmaker, load_only
from werkzeug.utils import secure_filename
from models import *

UPLOAD_FOLDER = './static/images/vehicles'

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
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    
    # Checks to see if the user is logged in, if not send user to the login screen.
    # If the user is then sends to the homepage.
    
    return render_template('home.html')
       
@app.route('/login')
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        return render_template('login.html', form=form)


@app.route('/register')
def index():
    form = LoginForm()
    return render_template('register.html', form=form)



@app.route('/logout')
@login_required
def logout():
    
    # Checks that a session is active and if so sets it to False
    # If there's no session and a user tries to log out it'll
    # take you to the login screen with a message.
    
    form = LoginForm()
    user = current_user
    user.is_authenticated = False
    logout_user()
    return render_template('login.html', form=form)
    

@app.route('/check-user-credentials', methods=['GET','POST'])
def checkuser():
    
    # Checks the users credentials against the 'Users' table.
    # If none match then flashes a message and asks to try again.
    if request.method == "POST":
        form = LoginForm()
        user = Users.query.filter_by(username = form.username.data).first()
        credentials = Users.query.filter_by(username = form.username.data, password = form.password.data).first()
        if user:
            if credentials:
                user.is_authenticated = True
                login_user(user, remember=False)
                return redirect((url_for('home')))
            else:
                flash('Wrong username or password')
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
        flash('This user already exists.')
        return render_template('register.html', form=form)

    
@app.route('/add-vehicle')
@login_required
def addVehicle():
    form = CarToDatabase()
    
    if request.method == 'POST' and form.validate_on_submit():
        
        file_img = form.car_img.data
        filename = secure_filename(file_img.filename)
        car_img_url = '/static/images/vehicles/' + filename
        
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
            file_img.save(os.path.join( UPLOAD_FOLDER, filename))
            flash('Vehicle added to database.')
            return redirect(url_for('filter'))
        except:
            flash("This vehicle couldn't be added, try again.")
            return redirect(url_for('addVehicle'))
    else:
        form = CarToDatabase()
        return render_template('add-vehicle.html', form=form)

@app.route('/summary')
@login_required
def summary():
    vehicles = Car.query.all()
    return render_template('summary.html', vehicles=vehicles)


@app.route('/filter-cars', methods=['GET', 'POST'])
#@login_required
def filter():
    form = FilterCars()
    region = form.region.data
    drive = form.drive.data
    cars = Car.query.all()
    
    # If POST this then validates the form and pushes the request.
    if request.method == 'POST' and form.validate_on_submit():
        
        # Checks what the SelectFields data is set to and if region is left on
        # 'All' then it will filter by the drivetrain data. 
        if region == 'All' and drive != 'All': 
            _car = Car.query.filter_by(drivetrain=drive).all()
            return render_template('filter-cars.html', form=form, cars=_car)
        
        # As above, it's the reversal of what's being checked and if drive is left
        # on 'All' then it will filter by region.
        elif drive == 'All' and region != 'All':
            _car = Car.query.filter_by(region=region).all()
            return render_template('filter-cars.html', form=form, cars=_car)
        
        # If both SelectFields are left on 'All', pulls all information from the
        # database to be displayed.
        elif ( region == 'All' and drive == 'All' ):
            _car = Car.query.all()
            return render_template('filter-cars.html', form=form, cars=_car) 
            
            # If both SelectFields are set to specified data from the list it will
            # pull the filtered data as requested.
        else:
            _car = Car.query.filter_by(region=region, drivetrain=drive).all() 
            return render_template('filter-cars.html', form=form, cars=_car)
    
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
    form = CarToDatabase()
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
        
        file_img = form.car_img.data
        filename = secure_filename(file_img.filename)
        car_img_url = '/static/images/vehicles/' + filename
        
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
        file_img.save(os.path.join( UPLOAD_FOLDER, filename))
        flash('Vehicle updated sucessfully!')
        return redirect(url_for('filter'))
        
    except:
        flash('Error occured, try again.')
        return render_template("edit-vehicle.html", form=form, vehicles=vehicles) 
        
@app.route('/delete/<int:car_id>', methods=['GET'])       
def deleteVehicle(car_id):
    if request.method == 'GET':
        car_id = db.session.query(Car).filter_by(id=car_id).first()
        db.session.delete(car_id)
        db.session.commit()
        try:
            
            
            flash('Vehicle successfully deleted.')
            return redirect(url_for('filter'))
        except:
            db.session.rollback()
            flash('Error occured, try again.')
            return redirect(url_for('filter'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
debug=True)
