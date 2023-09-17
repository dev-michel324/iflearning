from django.db import models
from django.contrib.auth.models import AbstractUser

SCHOOL_GRADE = (
    ("Ensino Fundamental", "Ensino Fundamental"),
    ("Ensino Médio", "Ensino Médio"),
    ("Ensino Superior", "Ensino Superior")
)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True)
    birth = models.DateField(null=True)
    school_grade = models.CharField(
        choices=SCHOOL_GRADE, max_length=19, default="Ensino Médio")

    def __str__(self):
        return self.username
