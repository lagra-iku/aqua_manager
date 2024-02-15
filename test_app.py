# Module that tests the flask app

import unittest
from app import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        # Add teardown code here if needed
        pass

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_display_entry_route(self):
        response = self.app.get('/display/1')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_route(self):
        response = self.app.get('/dashboard')
        # Check for redirection to login page if not logged in
        self.assertEqual(response.status_code, 302)
        # Follow the redirect to login page
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register_route(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        response = self.app.get('/logout')
        # Check for redirection to login page if not logged in
        self.assertEqual(response.status_code, 302)
        # Follow the redirect to login page
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_home_route(self):
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_not_found_error_handler(self):
        response = self.app.get('/nonexistent-route')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
