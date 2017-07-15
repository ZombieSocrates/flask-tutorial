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

# This allows you to define your own config and assign it to an
# environment variable.  The silent option implies that flask
# will ignore this if FLASKR_SETTINGS is not present
app.config.from_envvar('FLASKR_SETTINGS', silent = True)