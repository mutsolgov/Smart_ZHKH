from django.db import models
from django.conf import settings

class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    number = models.CharField("Номер лицевого счета", max_length=20, unique=True)
    description = models.CharField("Описание/Название", max_length=100, blank=True)

    def __str__(self):
        return f"{self.number} ({self.user.username})"
