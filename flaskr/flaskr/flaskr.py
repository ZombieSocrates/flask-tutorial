import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash


app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # get config settings from this file

# Load default config and override it from an environment variable
new_config = {'DATABASE': os.path.join(app.root_path, 'flaskr.db'),
			  'SECRET_KEY': 'development_key',
			  'USERNAME':'admin',
			  'PASSWORD':'default'
			  }
app.config.update(new_config)

'''This allows you to define your own config and assign it to an
environment variable.  The silent option implies that flask
will ignore this if FLASKR_SETTINGS is not present'''
app.config.from_envvar('FLASKR_SETTINGS', silent = True)

def connect_db():
	'''connects to app.config['DATABASE']'''
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row # Treats rows as dictionaries instead of tuples
	return rv

'''Flask provides two contexts: the application context and  the request context
The request variable is associated with the current request, while
g is an all purpose variable defining the current application context'''

def get_db():
	''' Opens a new database connection if there isn't one in the
	current application context
	'''
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

'''Functions with this decorator will execute everytime the appcontext
tears down. This context is created before a request is made and torn
down when the request finishes. The teardown will have an error parameter
of None (everything is fine) or an exception happened'''
@app.teardown_appcontext
def close_db(error):
	'''Closes the database again at the end of a request
	'''
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

'''open_resource is a helper function that retrieves a file from
the resource location (flaskr/flaskr)
'''
def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode = 'r') as f:
		db.cursor().executescript(f.read())
	db.commit()

'''The command line decorator creates a new command with 
the flask script.  You can now run flask initdb to execute
init_db()
'''
@app.cli.command('initdb')
def initdb_command():
	'''Initializes the database'''
	init_db()
	print('Initialized  the database')

'''This view function passes the entries in the database
to the show_entries template and renders the template
'''
@app.route('/')
def show_entries():
	db = get_db()
	cur = db.execute('select title, text from entries order by id desc')
	entries = cur.fetchall()
	return render_template('show_entries.html', entries = entries)

# @app.route('/add', methods = ['POST'])
