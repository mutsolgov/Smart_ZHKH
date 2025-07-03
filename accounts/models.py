from django.db import models
from users.models import User

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100)
