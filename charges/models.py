from django.db import models
from accounts.models import Account

class Charge(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.DateField()
    status = models.CharField(max_length=20, choices=[("pending", "Ожидает"), ("paid", "Оплачено")])
