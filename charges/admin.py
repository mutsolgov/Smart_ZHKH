from django.contrib import admin
from .models import Charge

@admin.register(Charge)
class ChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'service_name', 'period', 'amount', 'status')
    list_filter = ('service_name', 'status', 'period')
    search_fields = ('account__number', 'service_name')