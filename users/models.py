from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    full_name = models.CharField("ФИО", max_length=150)
    address = models.CharField("Адрес", max_length=255)

    def __str__(self):
        return self.username