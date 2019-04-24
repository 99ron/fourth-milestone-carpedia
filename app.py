# Test app.py 
import os
import sys
from forms import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, request, url_for, flash, session
from sqlalchemy.orm import sessionmaker
from models import *

# DB_URI = 'mysqldb://bd6203f445759d:3f8eca2f@eu-cdbr-west-02.cleardb.net/heroku_1146a0b312400c5?reconnect=true'

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    
    # Checks to see if the user is logged in, if not send user to the login screen.
    
   if not session.get('logged_in'):
        form = LoginForm()
        return render_template('login.html', form=form)
   else:
        form = LoginForm()  
        return render_template('home.html')
        
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register')
def index():
    form = LoginForm()
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    
    # Checks that a session is active and if so sets it to False
    # If there's no session and a user tries to log out it'll
    # take you to the login screen with a message.
    
    if session.get('logged_in'):
        session['logged_in'] = False
        return home()
    else:
        flash("You're not logged in..." )
        return login()
    
    
@app.route('/check-user-credentials', methods=['GET','POST'])
def checkuser():
    
    # Checks the users credentials against the 'Users' table.
    # If none match then flashes a message and asks to try again.
    if request.method == "POST":
        form = LoginForm()
        user = Users.query.filter_by(username = form.username.data, password = form.password.data).first()
        
        if user is not None:
            session['logged_in'] = True
            session['username'] = user.username
        else:
            flash('Wrong username or password, Try again.')
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
        flash('This user already exists, try another.')
        return render_template('register.html', form=form)

    
@app.route('/add-vehicle')
def addVehicle():
    regions = Region.query.all()
    makes = Make.query.all()
    trans = Trans.query.all()
    drives = Drive.query.all()
    chassy = Chassy_Type.query.all()
    return render_template('add-vehicle.html',
                            region=regions, 
                            make=makes,
                            trans=trans,
                            drives=drives,
                            chassy=chassy)


@app.route('/add-vehicle-to-db', methods=['GET', 'POST'])
def addVehicleToDB():
    
    if request.method== 'POST':
            _region = request.form.get('form_region')
            _make = request.form.get('form_make')
            _model = request.form.get('form_model')
            _image = request.form.get('form_image')
            _model_year = request.form.get('form_year')
            _trans = request.form.get('form_trans')
            _drive = request.form.get('form_drive')
            _body = request.form.get('form_body')
            _stats_hp = request.form.get('form_stats_hp')
            _stats_torque = request.form.get('form_stats_torque')
            _stats_accel = request.form.get('form_stats_accel')
    try:
        new_car = Car(region_name = _region,
        make_name = _make,
        model_name = _model,
        img_url = _image,
        model_year_num = _model_year,
        trans_id = _trans,
        drive_id = _drive,
        body_id = _body,
        hp_amount = _stats_hp,
        torque_amount = _stats_torque,
        accel_time = _stats_accel)
        db.session.add(new_car)
        db.session.commit()
        flash('Vehicle added to database.')
        return render_template('add-vehicle.html')
    except:
        flash("This vehicle couldn't be added. Try another")
        return redirect(url_for('addVehicle'))




if __name__ == '__main__':
    
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
debug=True)