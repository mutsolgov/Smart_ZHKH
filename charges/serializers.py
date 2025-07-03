from rest_framework import serializers
from .models import Charge

class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = ['id', 'account', 'service_name', 'amount', 'period', 'status']
        read_only_fields = ['status']