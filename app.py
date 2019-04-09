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
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def index():
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def welcome():
    return render_template('home.html')

@app.route('/check-user-credentials', methods=['GET','POST'])
def checkuser():
    if request.method == "POST":
        uname = request.form['username']
        pword = request.form['password']
        login = Users.query.filter_by(username=uname, password=pword).first()
        
        if login is not None:
            return redirect (url_for('home'))
           # flash('wrong password')
        return render_template('login.html')

@app.route('/register-user/', methods=['GET', 'POST'])
def register():
	
    if request.method == 'POST':
	    uname = request.form['username']
	    pword = request.form['password']
	    new_user = Users(username = uname, password = pword)
    db.session.add(new_user)
    db.session.commit()
		
    return redirect(url_for('login'))
    return render_template('register.html')
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
debug=True)