# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, session
from flask_pymongo import PyMongo


# -- Initialization section --
app = Flask(__name__)

events = [
        {"event":"First Day of Classes", "date":"2019-08-21"},
        {"event":"Winter Break", "date":"2019-12-20"},
        {"event":"Finals Begin", "date":"2019-12-01"},
        {"event":"Bernard's Birthday", "date":"2020-10-11"},
        {"event":"Christmas", "date": "2020-12-25"}
    ]

# name of database
app.config['MONGO_DBNAME'] = 'test'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://bernard:bulbasaur@cluster0.jxvpj.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

# This is for the session
#  If using Python 3, use a string
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})
 
    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('list_events'))
        return redirect(url_for('index'))
    return render_template('signup.html') 

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
 
        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('list_events'))
        return 'That username already exists! Try logging in.'
    return render_template('signup.html')

@app.route('/events')
def list_events():
    collection = mongo.db.events
    events = collection.find()
    username = ""
    return render_template('mainpage.html', events = events, username = session.get('username'))

@app.route('/my_events')
def list_my_events():
    collection = mongo.db.events
    events = collection.find({'user': session['username']})
    username = ""
    return render_template('userpage.html', events = events, username = session.get('username'))
    
@app.route('/events/new', methods=['GET', 'POST'])
def new_event():
    if request.method == "POST":
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        if session.get('username'):
            user_name = session['username']
        else:
            user_name = request.form['user_name']
 
        collection = mongo.db.events
        collection.insert({'event': event_name, 'date': event_date, 'user': user_name})
        return redirect(url_for('list_events'))
# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database

    # insert new data

    # return a message to the user
    return ""

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
