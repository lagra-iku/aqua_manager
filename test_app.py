import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'dashboard', response.data)

    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_invalid_route(self):
        response = self.app.get('/invalid_route')
        self.assertEqual(response.status_code, 404)
    
    def test_service_unavailable_route(self):  # Add @ before unittest
        response = self.app.get('/service_unavailable_error')
        self.assertEqual(response.status_code, 503)
        
    def test_register_route(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'register', response.data)
    
    def test_profile_route(self):
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user_profile/profile', response.data)
        
    def test_admin_route(self):
        response = self.app.get('/admin')
        self.assertEqual(response.status_code, 200)  # Change 302 to 200 if needed
        self.assertIn(b'admin', response.data)

    def test_logout_route(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'logout', response.data)
        
    def test_production_content_route(self):
        response = self.app.get('/production_content')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'admin/production_content', response.data)

if __name__ == '__main__':
    unittest.main()
