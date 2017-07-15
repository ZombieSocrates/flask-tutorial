import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

# Flask provides two contexts: the application context and  the request context
# The request variable is associated with the current request, while
# g is an all purpose variable defining the current application context


def connect_db():
	'''connects to app.config['DATABASE']'''
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row # Treats rows as dictionaries instead of tuples
	return rv

def get_db():
	''' Opens a new database connection if there isn't one in the
	current application context
	'''
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

# Functions with this decorator will execute everytime the appcontext
# tears down. This context is created before a request is made and torn
# down when the request finishes. The teardown will have an error parameter
# of None (everything is fine) or an exception happened
@app.teardown_appcontext
def close_db(error):
	'''Closes the database again at the end of a request
	'''
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()



app = Flask(__name__) # create the application instance
app.config.from_object(__name__) # get config settings from this file

# Load default config and override it from an environment variable
new_config = {'DATABASE': os.path.join(app.root_path, 'flaskr.db'),
			  'SECRET_KEY': 'development_key',
			  'USERNAME':'admin',
			  'PASSWORD':'default'
			  }
app.config.update(new_config)

# This allows you to define your own config and assign it to an
# environment variable.  The silent option implies that flask
# will ignore this if FLASKR_SETTINGS is not present
app.config.from_envvar('FLASKR_SETTINGS', silent = True)

