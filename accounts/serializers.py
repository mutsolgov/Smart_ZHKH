from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'number', 'address', 'owner_full_name',]
        read_only_fields = ['owner_full_name']
    
    def validate_number(self, value):
        # RegexValidator на уровне модели уже проверяет формат
        return value
    
    def validate(self, data):
        # Дополнительно: можно проверять, если is_active в False/True
        return data
    
    def ceate(self, validated_data):
        # owner_full_name подтягиваем из user
        user = self.context['request'].user
        validated_data['owner_full_name'] = user.full_name
        # Если нет ни одного активного, можно сделать новый активным или оставить False
        account = Account.objects.create(user=user, **validated_data)
        return account
    
    def update(self, instance, validated_data):
        # Если пытаются сменить owner_full_name на фронте, игнорируем (поле read_only)
        # Если меняется is_active, логика в save() снимает флаги
        return super().update(instance, validated_data)