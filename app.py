# Test app.py 
import os
import sqlalchemy
from model import *
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker


DB_URI = 'mysqldb://bd6203f445759d:3f8eca2f@eu-cdbr-west-02.cleardb.net/heroku_1146a0b312400c5?reconnect=true'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    
    # Checks to see if the user is logged in, if not send user to the login screen.
    
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html')
        
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def index():
    return render_template('register.html')

@app.route('/logout')
def logout():
    
    # Checks that a session is active and if so sets it to False
    # If there's no session and a user tries to log out it'll
    # take you to the login screen with a message.
    
    if session.get('logged_in'):
        session['logged_in'] = False
        return login()
    else:
        flash("You're not logged in..." )
        return login()
    
    
@app.route('/check-user-credentials', methods=['GET','POST'])
def checkuser():
    
    # Checks the users credentials against the 'Users' table.
    # If none match then flashes a message and asks to try again.
    
    if request.method == "POST":
        uname = request.form['username']
        pword = request.form['password']
        login = Users.query.filter_by(username=uname, password=pword).first()
        
        if login is not None:
            session['logged_in'] = True
            session['username'] = uname
        else:
            flash('Wrong Password, try again.')
            return render_template('login.html')
        return redirect(url_for('home'))
        
        
@app.route('/register-user/', methods=['GET', 'POST'])
def register():
	
	# This attempts to create a new user in the 'Users' table.
	# If the user already exists it'll flash a message and ask to try again.
	
    try: 
        if request.method == 'POST':
	        uname = request.form['username']
	        pword = request.form['password']
	        new_user = Users(username = uname, password = pword)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    except:
        flash('This user already exists, try another.')
        return render_template('register.html')
    

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
debug=True)