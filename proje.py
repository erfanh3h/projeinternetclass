from flask import Flask, render_template, flash, request,session
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from sqlalchemy.orm import sessionmaker
from tabledef import *
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
engine = create_engine('sqlite:///tutorial.db', echo=True)

@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('admin.html')
    else:
        return "Hello Admin!  <a href='/adminedit'>Enter people</a> <a href='/logout'>log out</a>"

@app.route("/user/<int:sid>")
def get_user(sid):
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.sid.in_([sid]))
    result = query.first()
    data = {
        'id': result.sid,
        'username': result.name,
        'email': result.email,
        'address': result.resume
    }
    return json.dumps(data)

@app.route('/admin', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

class showform(FlaskForm):
    sid = IntegerField('SID')

@app.route("/user", methods=['GET','POST'])
def user():
    form = showform(request.form)
    if request.method == 'POST':
        sid = request.form['sid']
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.sid.in_([sid]))
        result = query.first()
        if result:
            query = s.query(User).filter(User.sid.in_([sid]))
            res = query.first()
            data = {
                'id': res.sid,
                'username': res.name,
                'email': res.email,
                'address': res.resume
            }
            flash(res.sid)
            flash(res.name)
            flash(res.phone)
            flash(res.email)
            flash(res.resume)
        else:
            flash('Wrong Password!')
    return render_template('user.html', form=form)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

class RegisterForm(FlaskForm):
    id = IntegerField('SID')
    username = StringField('Name')
    password = PasswordField('Phone')
    email = StringField('Email')
    address = StringField('Resume')
    submit = SubmitField('Sign In')
@app.route("/adminedit", methods=['GET','POST'])
def index():
    form= RegisterForm()
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        print(id + ' - ' + username + ' - ' + password + ' - ' + email + ' - ' + address)
        if id and username and password:
            Session = sessionmaker(bind=engine)
            session = Session()

            user = User(id, username, password, email, address)
            session.add(user)

            # commit the record the database
            session.commit()
            flash('ID: ' + id + ' --> Username: ' + username + ', Email: ' + email + ', Address: ' + address)
        else:
            flash('Error: Fill all feilds!! ')
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run()