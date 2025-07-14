from django.db import models
from accounts.models import Account


class ServiceType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Charge(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
        ('partial', 'Частично оплачено'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='charges')
    service = models.CharField(ServiceType, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('account', 'service', 'period')

    def __str__(self):
        return f"{self.service.name} для {self.account.number} ({self.period.strftime('%m.%Y')})"
