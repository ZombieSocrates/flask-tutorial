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

	def login(self, username, password):
		return self.app.post('/login', 
							data = dict(username = username,
										password = password),
							follow_redirects = True
							)

	def logout(self):
		return self.app.get('/logout', follow_redirects = True)

	def test_login_logout(self):
		'''Uses the above two methods to see whether you can log in
		and out with valid credentials and get banhammered with 
		invalid ones
		'''
		rv = self.login('admin','default')
		assert b'You were logged in' in rv.data
		rv = self.logout()
		assert b'You were logged out' in rv.data
		rv = self.login('adminx','default')
		assert b'Invalid username' in rv.data
		rv = self.login('admin','defaultx')

	def test_messages(self):
		'''Checks that we can add a message, where html is allowed in the
		text but not in the title
		'''
		self.login('admin','default')
		rv = self.app.post('/add',
						   data = dict(title='<Hello>',
						   			   text = '<strong>HTML</strong> allowed here'),
						   follow_redirects = True
						   )
		assert b'No entries so far' not in rv.data
		assert b'&lt;Hello&gt;' in rv.data
		assert b'<strong>HTML</strong> allowed here' in rv.data




if __name__ == '__main__':
	unittest.main()