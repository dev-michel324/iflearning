from django.test import TestCase
from accounts.models import CustomUser

from django.db.utils import IntegrityError

class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create(
            username = "test",
            email = "test@test.com",
            password = "test123456"
        )
        self.user.save()

    def test_if_email_equal(self) -> None:
        email : str = "test@test.com"

        self.assertEqual(self.user.email, email)

    def test_expect_username_unique_error(self) -> None: 
        with self.assertRaises(IntegrityError):
            user = CustomUser.objects.create(
                username = "test",
                email = "test1test.com",
                password = "test123456"
            ).save()

    def test_expect_email_unique_error(self) -> None:
        with self.assertRaises(IntegrityError):
            user = CustomUser.objects.create(
                username = "test1",
                email = "test@test.com",
                password = "test123456"
            ).save()