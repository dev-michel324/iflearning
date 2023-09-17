from django.test import TestCase, Client
from accounts.models import CustomUser

class TestRegister(TestCase):
    def setup(self) -> None:
        pass

    def test_register_view(self) -> None:
        client = Client()
        response = client.post("/register", data={
            "username": "test",
            "email": "test@test.com",
            "firstname": "test",
            "lastname": "test",
            "password": "test123456.",
            "password_2": "test123456."
        })

        user_exists = CustomUser.objects.filter(email="test@test.com").exists()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(user_exists, True)
        self.assertRedirects(response, "/login")

    def test_register_view_wrong_password_match(self) -> None:
        client = Client()
        password1 = "test123456."
        password2 = "test123"
        
        response = client.post("/register", data={
            "username": "test",
            "email": "test@test.com",
            "firstname": "test",
            "lastname": "test",
            "password": password1,
            "password_2": password2
        })

        user_exists = CustomUser.objects.filter(email="test@test.com").exists()

        self.assertEqual(user_exists, False)
        self.assertEqual(response.status_code, 200)