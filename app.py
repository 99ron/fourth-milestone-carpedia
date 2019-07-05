import os
import sys
import json
import boto3
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from forms import LoginForm, RegisterForm, CarToDatabase, FilterCars, CsrfProtect, EditCar
from flask_sqlalchemy import SQLAlchemy
from flask_s3 import FlaskS3
from flask import Flask, render_template, redirect, request, url_for, flash, session, jsonify
from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy import func
from werkzeug.utils import secure_filename
from models import *


# Settings for S3 storage. This is used for storing images.
S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

# Setting file path and file extensions for image uploads.
UPLOAD_FOLDER = S3_LOCATION
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Used to check image extension is on the allowed list. 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Setting the app details.
app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FLASKS3_ACTIVE'] = True
app.config['FLASKS3_BUCKET_NAME'] = os.environ.get('S3_BUCKET_NAME')
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')



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
    
    '''
    This is the primary route when the page is loaded. Also checks to see if a user 
    is currently logged in and if so forwards/redirects them to the homepage.
    '''
    
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
    form = RegisterForm()
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():

    '''
     Checks that a session is active and if so sets it to False.
     If there's no session and a user tries to log out it'll
     take you to the login screen with a message.
    '''
    
    form = LoginForm()
    if current_user.is_authenticated == False:
        flash("Why you trying? You're not logged in.")
        return render_template('login.html', form=form)
    else:
        user = current_user
        user.is_authenticated = False
        logout_user()
    return redirect(url_for('login'))


@app.route('/check-user-credentials', methods=['GET','POST'])
def checkuser():
    form = LoginForm()
    
    if request.method == "GET":
        return render_template('login.html', form=form)
    
    '''    
     Checks the users credentials against the 'Users' table.
     If none match then flashes a message and asks the user to try again.
    '''
    
    if request.method == "POST":
        # I've got it to check if the username exists in the table first.
        user = Users.query.filter_by(username = form.username.data).first()
        
        if user:
            # Then if the user is found, to confirm the user and password match in the database.
            credentials = Users.query.filter_by(username = form.username.data, password = form.password.data).first()
            
            if credentials:
                # Once confirmed user then confirms it's authenticated and redirected to the homepage.
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
	
    '''
    This attempts to create a new user in the 'Users' table.
    If the user already exists it'll flash a message and ask to try again.
    '''
    form = RegisterForm()
    
    if request.method == 'POST':
        # Posts the users preferred username and password.
        new_user = Users(username=form.username.data, password=form.password.data)
        
        try:
            
            if not new_user:
                # If the username is taken then flash a message to try another.
                flash('This user already exists.')
                return render_template('register.html', form=form)
            else:
                # If username isn't taken then add to the Users table.
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
        except:
            flash('Error Occured, try again.')
            return render_template('register.html', form=form)
    
@app.route('/add-vehicle', methods=['POST', 'GET'])
@login_required
def addVehicle():
    form = CarToDatabase()
    
    if request.method == 'POST':
       
        # Collects the image filename from the form
        file_img = form.car_img.data
        
        if file_img and allowed_file(file_img.filename):
            # This processes the image wanting to be uploaded that it is an image format
            # and saves the filepath to the image location in the db while also physically
            # storing the image in the bucket.

            filename = secure_filename(file_img.filename)
            car_img_url = UPLOAD_FOLDER + "images/" + filename
            try:
                # This tries to places the physical image in to my bucket on S3.
                # If the file already exists then sets the url to it but doesn't upload the file.
                
                s3 = boto3.resource('s3')
                s3.Bucket('vinpedia').put_object(Key="images/" + filename, Body=file_img)
            except:
                flash('Couldn\'t upload that file. Please try again on the edit page.')
                car_img_url = UPLOAD_FOLDER + 'images/no_img.jpg'
        else:
            car_img_url = UPLOAD_FOLDER + 'images/no_img.jpg'
        
        # Collects all the information from the form to compile it into a new vehicle in the database.
        add_car = Car(region=form.region.data,
                      make=form.make.data,
                      model=form.model.data,
                      model_year=form.year.data,
                      trans=form.trans.data,
                      hp_amount=form.hp.data,
                      torque_amount=form.torque.data,
                      drivetrain=form.drive.data,
                      chassy_desc=form.body.data,
                      car_desc=request.form["car-description"],
                      accel_time=form.accel.data,
                      img_url=car_img_url,
                      upload_by=current_user.username)
                      
        try:
            # Uploads the newly added vehicle to the db as long as there's no issues.
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
@login_required
def filter():
    '''
    This section processes the filter of which I've chosen by Region and Drive type
    to filter by, it's then sorted by Manufacturer A-Z or only cars that have likes on them.
    '''
    cars = Car.query.all()
    form = FilterCars()
    region = form.region.data
    drive = form.drive.data
    query = form.query.data
    
    # If POST this then validates the form and pushes the request.
    if request.method == 'POST' and form.validate_on_submit():
        
        # If region and drive have values they'll be processed here.
        if region != "All" and drive != "All":
            cars=car_region_drive(region, drive, query)
         
        # If region has a value but drive does not then it'll be processed here.    
        if region != "All" and drive == "All":
            cars = car_region(region, query)
        
        # If drive has a value but region doesn't then it'll be processed here.
        if region == "All" and drive != "All":
            cars = car_drive(drive, query)
        
        # If neither has values then it'll be processed here.  
        if region == "All" and drive == "All":
            cars = car_all(query)
        
        return render_template('filter-cars.html', form=form, cars=cars)

    # When the page loads it requests all cars from the database to display.
    return render_template('filter-cars.html', form=form, cars=cars, query=query)


@app.route('/filter-cars/mine', methods=['GET', 'POST'])
@login_required
def myUploads():
    form = FilterCars()
    user = current_user.username
    try:
        # Searches for the current logged in user's cars by comparing the user by the upload_by field.
        cars = Car.query.filter(user==Car.upload_by).order_by(Car.make)
        return render_template('filter-cars.html', cars=cars, form=form)
    except:
        flash("Something went wrong, please try again.")
        return render_template('filter-cars.html', cars=cars, form=form)
    
@app.route('/vehicle/<int:car_id>', methods=['GET'])
@login_required
def vehicleInfo(car_id):
    # When the user presses the more info button this gets the vehicles ID and displays all the information for that vehicle.
    vehicles=Car.query.filter_by(id=car_id).first()
    return render_template("vehicle-info.html", vehicles=vehicles) 


@app.route('/vehicle/edit/<int:car_id>/<vehicleName>', methods=['POST', 'GET'])
@login_required
def editVehicle(car_id, vehicleName):
    '''
    This section is for editing the vehicle in the database, which can only be done by
    the user who uploaded the vehicle. 
    '''
    form = EditCar()
    user = current_user.username
    vehicles=Car.query.filter_by(id=car_id).one()
    
    if request.method == 'GET':
        
        # Confirms the current logged in user is who uploaded the vehicle.
        user_match = user_uploaded_car(user)
        
        if user_match is True:
        
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
        else:
            flash('You can\'t do that request. You didn\'t upload this vehicle.')
            return redirect(url_for('filter'))

    if request.method == 'POST':
        
        # Confirms the current logged in user is who uploaded the vehicle that's trying to be edited.
        user_match = user_uploaded_car(user)
        
        if user_match is True:
            
            # If true then proceeds with processing the data
            vehicleImage = vehicles.img_url 
            file_img = form.car_img.data
            
            # Confirms there's a file to upload, if not it'll keep the stored image to be used.
            if file_img and allowed_file(file_img.filename):
                filename = secure_filename(file_img.filename)
                car_img_url = UPLOAD_FOLDER + "images/" + filename
                try:
                    # This tries to places the physical image in to my bucket on S3. If it already exists 
                    # or fails it'll just use the previous image. 
                    s3 = boto3.resource('s3')
                    s3.Bucket('vinpedia').put_object(Key="images/" + filename, Body=file_img)
                except Exception as e:
                    print(e)
                    flash('Couldn\'t upload that file. Have put the previous image back on.')
                    car_img_url = vehicleImage
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
        return redirect(url_for('vehicleInfo', car_id=vehicles.id, vehicleName=vehicles.model))
        
    except:
        flash('Invalid Input.')
        return render_template("edit-vehicle.html", form=form, vehicles=vehicles) 
        
@app.route('/delete/<int:car_id>', methods=['GET', 'POST']) 
@login_required
def deleteVehicle(car_id):
    '''
    This button deletes the currently viewed car but only if the user is the same 
    as who uploaded it.
    '''
    user = current_user.username
    if request.method == 'GET':
        user_match = user_uploaded_car(user)
        
        # If logged in user matches the uploaded user then it'll process the delete function below.
        if user_match is True:
            try:
                car_id = db.session.query(Car).filter_by(id=car_id).first()
                db.session.delete(car_id)
                db.session.commit()
                flash('Vehicle successfully deleted.')
                return redirect(url_for('filter'))
            except Exception as e:
                print(e)
                db.session.rollback()
                flash('Error occured, try again.')
                return redirect(url_for('filter'))
        else:
            flash('You can\'t do that request. You didn\'t upload this vehicle.')
            return redirect(url_for('filter'))
    else:
        return redirect(url_for('filter'))
            
@app.route('/summary')
@login_required
def summary():
    return render_template('summary.html')


@app.route('/summary/data')
def summaryData():
    '''
    This route compiles the information from the database, puts it as a list within an array 
    and finally converts it to a JSON URL which is retrieved on the summary.html page to display
    on a barchart and a dynamic table.
    '''
    
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
    MT500 = 0
    MT500N = []
    MT300 = 0
    MT300N = []
    LT300 = 0
    LT300N = []
    

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
            LT4N.append([' ' + car.make + ' ' + car.model + ' - ' + str(car.accel_time)])
        elif car.accel_time <= 7:
            LT7 +=1
            LT7N.append([' ' + car.make + ' ' + car.model + ' - ' + str(car.accel_time)])
        else:
            MT7 +=1
            MT7N.append([' ' + car.make + ' ' + car.model + ' - ' + str(car.accel_time)])
        
        if car.hp_amount >= 500:
            MT500 +=1
            MT500N.append([' ' + car.make + ' ' + car.model + ' - ' + str(car.hp_amount) + 'bhp'])
        elif car.hp_amount >=300:
            MT300 +=1
            MT300N.append([' ' + car.make + ' ' + car.model + ' - ' + str(car.hp_amount) + 'bhp'])
        else:
            LT300 +=1
            LT300N.append([' ' + car.make + ' ' + car.model + ' - ' + str(car.hp_amount) + 'bhp'])
            
        
        
        
    jsonData = [{'USDM' : USDM , 'JDM' : JDM, 'Euro' : Euro, 'USDMN' : USDMN, 'JDMN' : JDMN, 'EuroN' : EuroN }, {'Manual': Manual, 'SemiAuto': SemiAuto, 'Auto': Auto, 'Sequential': Sequential, 'ManualN' : ManualN, 'SemiAutoN' : SemiAutoN, 'AutoN' : AutoN, 'SequentialN' : SequentialN}, {'LT4' : LT4, 'LT7': LT7, 'MT7': MT7, 'LT4N' : LT4N, 'LT7N' : LT7N, 'MT7N' : MT7N }, {'MT500' : MT500, 'MT300' : MT300, 'LT300' : LT300, 'MT500N' : MT500N, 'MT300N' : MT300N, 'LT300N' : LT300N}]
    return jsonify(jsonData)
    


@app.route('/like/<int:car_id>/<action>')
@login_required
def like(car_id, action):
    
    '''
    Route below checks if the user has voted on the current viewed car and responds
    with either the like or unlike button while adding or removing a vote, the functions 
    are in the models.py file
    '''
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
