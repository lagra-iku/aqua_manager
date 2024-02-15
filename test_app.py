import unittest
from app import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_edit_entry_route(self):
        response = self.app.get('/edit/1')
        self.assertEqual(response.status_code, 200)

    def test_display_entry_route(self):
        response = self.app.get('/display/1')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_route(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_admin_route(self):
        response = self.app.get('/admin')
        self.assertEqual(response.status_code, 200)

    def test_add_production_route(self):
        response = self.app.get('/add_production')
        self.assertEqual(response.status_code, 200)

    def test_production_content_route(self):
        response = self.app.get('/production_content')
        self.assertEqual(response.status_code, 200)

    def test_edit_production_route(self):
        response = self.app.get('/edit_production/1')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_profile_route(self):
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 200)

    def test_register_route(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 200)

    def test_home_route(self):
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 200)

    def test_not_found_error_handler(self):
        response = self.app.get('/nonexistent-route')
        self.assertEqual(response.status_code, 404)

    def test_service_unavailable_error_handler(self):
        response = self.app.get('/admin', headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 503)

if __name__ == '__main__':
    unittest.main()
