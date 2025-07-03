from django.db import models
from accounts.models import Account

class Charge(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
        ('partially_paid', 'Частично оплачено'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='charges')
    service_name = models.CharField("Услуга", max_length=100)
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    period = models.DateField("Период начисления")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.service_name} для {self.account.number} ({self.period})"
