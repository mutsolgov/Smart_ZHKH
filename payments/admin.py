from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'charge', 'amount', 'date')
    list_filter = ('date',)
    search_fields = ('charge__account__number',)