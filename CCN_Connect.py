# -*- coding: utf-8 -*-
"""
    CCN Connect
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

import flask.ext.login as flask_login

login_manager = flask_login.LoginManager()



# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'CCN_Connect.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    

@app.cli.command('initdb')
def initdb_command():
    print "hi"
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db



@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

'''
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)
'''

def make_suggestions_weighted(person_id):
    db = get_db()
    cur = db.execute('select city, state, gender, diagnosis_type, years_without_treatment from people' +
                     'where person_id = ?', person_id)
    person_data = cur.fetchall()[0]
    city = person_data[0]
    state = person_data[1]
    gender_code = person_data[2]
    diagnosis_type = person_data[3] 
    years_without_treatment = person_data[4]

    cur = db.execute('select interest_id from person_interests' + 
                     'where person_id =?', person_id)
    interest_codes = cur.fetchall()

    cur = db.execute('select person_id from people ' + 
                     'where city = ? and state = ?', (city,state))
    close_people = cur.fetchall()

    cur = db.execute('select community_id from community_members ' + 
                     'where community_member_id= ?', person_id)
    # finish this

@app.route('/')
def show_welcome():
#    if current_user.is_authenticated():
#        print "hi"
    return render_template('index.html')
    
        
@app.route('/<username>/friends')  # formatted as firstname.lastname
def show_user_friends(username):
    name_list = username.split('.')
    if len(name_list) == 1:
        return "Invalid Page"
    firstname = name_list[0]
    lastname = name_list[1]
    db = get_db()
    cur = db.execute('select description, id from people ' +
                     'where first_name = ' + "'" + firstname + "'" +
                     'and last_name = ' + "'" + lastname + "'")
    entries = cur.fetchall()
    if len(entries) == 0:
        return "Invalid Page"
    else:
        db = get_db()
        cur = db.execute('select person2_id from friendships ' +
                         'where person1_id = ?', str(entries[0][1]))
        entries1 = cur.fetchall()

        cur = db.execute('select person1_id from friendships ' +
                         'where person2_id = ?', str(entries[0][1]))
        entries2 = cur.fetchall()
        entries = entries1 + entries2
        return render_template('friends.html', friends=entries)
    
@app.route('/<username>/profile')  # formatted as firstname.lastname
def show_user_prof(username):
    name_list = username.split('.')
    if len(name_list) == 1:
        return "Invalid Page"
    firstname = name_list[0]
    lastname = name_list[1]
    db = get_db()
    cur = db.execute('select description, id from people ' +
                     'where first_name = ' + "'" + firstname + "'" +
                     'and last_name = ' + "'" + lastname + "'")
    entries = cur.fetchall()
    if len(entries) == 0:
        return "Invalid Page"
    else:
        db = get_db()
        cur = db.execute('select person2_id from friendships ' +
                         'where person1_id = ?', str(entries[0][1]))
        entries1 = cur.fetchall()

        cur = db.execute('select person1_id from friendships ' +
                         'where person2_id = ?', str(entries[0][1]))
        entries2 = cur.fetchall()
        entries = entries1 + entries2
        return render_template('profile.html', friends=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into people (first_name,'+ 
                                    'last_name' +
                                    'gender,' +
                                    'city,' +
                                    'state,' +
                                    'diagnosis_type,' +
                                    'description) values (?, ?, ?, ?,' +
                                                          '?, ?, ?)',
               [request.form['first_name'], 
               request.form['last_name'], 
               request.form['gender'], 
               request.form['city'],
               request.form['state'],
               request.form['diagnosis_type'],
               request.form['description']])
    db.commit()
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_welcome'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_welcome'))

app.run()