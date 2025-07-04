from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'description')
    list_filter = ('user',)
    search_fields = ('number', 'user__username', 'description')
