from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class LoginTestCase(TestCase):
    def setUp(self):
        # Create a user with all required fields, including 'nombre'
        User = get_user_model()
        self.user = User.objects.create_user(
            correo_electronico='user@example.com', 
            password='testpassword', 
            nombre='Test User'  # Assuming 'nombre' is the required field you were missing
        )
    
    def test_correct_login(self):
        # Attempt to log in with correct credentials
        login_successful = self.client.login(correo_electronico='user@example.com', password='testpassword')
        self.assertTrue(login_successful)
        # Follow this with tests to access views or data as needed

    def test_wrong_login(self):
        # Attempt to log in with incorrect credentials
        login_successful = self.client.login(correo_electronico='user@example.com', password='wrongpassword')
        self.assertFalse(login_successful)
        # You can further assert response or redirection as needed
