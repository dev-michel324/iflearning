from django.test import TestCase, Client
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password

class TestLogin(TestCase):
    def setUp(self) -> None:
        self.username = "test"
        self.email = "test@test.com"
        self.password = "test123456"
        encrypted_password = make_password(self.password, None, "default")

        self.user = CustomUser.objects.create(
            username = self.username,
            email = self.email,
            password = encrypted_password
        )
        self.user.save()

    def test_login_view(self) -> None:
        client = Client()
        response = client.post("/login", data={"email": self.email, "password": self.password})

        self.assertRedirects(response, '/dashboard')
        self.assertEqual(response.status_code, 302)

    def test_login_with_wrong_password_view(self) -> None:
        wrong_password : str = "123456"
        client = Client()
        response = client.post("/login", data={"email": self.email, "password": wrong_password})
        
        self.assertEqual(response.status_code, 200)