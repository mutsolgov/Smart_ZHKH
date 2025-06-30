from django.db import models
from users.models import CustomUser

class Account(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100)
