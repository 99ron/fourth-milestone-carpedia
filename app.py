# Test app.py 
import os
import sys
from flask_login import current_user, login_user, LoginManager, login_required, logout_user
from forms import LoginForm, RegisterForm, CarToDatabase
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, request, url_for, flash, session
from sqlalchemy.orm import sessionmaker
from models import *

# DB_URI = 'mysqldb://bd6203f445759d:3f8eca2f@eu-cdbr-west-02.cleardb.net/heroku_1146a0b312400c5?reconnect=true'

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))



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
    user.authenticated = False
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
        return render_template('add-vehicle.html', form=form)

@app.route('/add-vehicle-to-db', methods=['GET', 'POST'])
@login_required
def addVehicleToDB():
    form = CarToDatabase()
    if request.method == 'POST':
        
        add_car = Car(region=form.region.data,
                      make=form.make.data,
                      model=form.model.data,
                      model_year=form.year.data,
                      trans=form.trans.data,
                      hp_amount=form.hp.data,
                      torque_amount=form.torque.data,
                      drivetrain=form.drive.data,
                      chassy_desc=form.body.data,
                      accel_time=form.accel.data,
                      img_url=form.car_img.data,
                      upload_by=user_id)
                      
    try:
        db.session.add(add_car)
        db.session.commit()
        flash('Vehicle added to database.')
        return redirect(url_for('addVehicle'))
    except:
        flash("This vehicle couldn't be added. Try another")
        return redirect(url_for('addVehicle'))




if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
debug=True)