from django.test import TestCase, Client
from accounts.models import CustomUser

class TestViews(TestCase):
    def setUp(self) -> None:
        self.username = "test"
        self.email = "test@test.com"
        self.password = "test123456"

        self.user = CustomUser.objects.create(
            username = self.username,
            email = self.email,
            password = self.password
        )
        self.user.save()

    def test_home(self) -> None:
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_login(self) -> None:
        client = Client()
        response = client.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_register(self) -> None:
        client = Client()
        response = client.get("/register")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_without_is_logged(self) -> None:
        client = Client()
        response = client.get("/dashboard")

        self.assertRedirects(response, "/login?next=/dashboard")
        self.assertEqual(response.status_code, 302)

    def test_dashboard_logged(self) -> None:
        client = Client()
        client.force_login(self.user)
        response = client.get("/dashboard")
        self.assertEqual(response.status_code, 200)