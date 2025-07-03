from django.db import models
from charges.models import Charge

class Payment(models.Model):
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    