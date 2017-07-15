import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

	def setUp(self):
		'''Creates a new test_client and initializes a new database
		before each test is run.  Also activates testing config flag
		to true
		'''
		self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp() #returns a low-level handle and random file name
		flaskr.app.testing = True
		self.app = flaskr.app.test_client()
		with flaskr.app.app_context():
			flaskr.init_db()

	def tearDown(self):
		'''clean up,clean up, everybody everywhere
		'''
		os.close(self.db_fd)
		os.unlink(flaskr.app.config['DATABASE'])

	def test_empty_db(self):
		'''Checks that application has "No entries so far"
		at its root before any entries are added. The 
		app.get method sends a get request and we check the
		output'''
		rv = self.app.get('/')
		assert b'No entries so far' in rv.data

if __name__ == '__main__':
	unittest.main()