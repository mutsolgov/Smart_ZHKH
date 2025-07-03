from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Charge
from .serializers import ChargeSerializer

class ChargeViewSet(viewsets.ModelViewSet):
    serializer_class = ChargeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Charge.objects.filter(account_user=self.request.user)
    
    def perform_create(self, serializer):
        account = serializer.validated_data['account']
        if account.user != self.request.user:
            raise PermissionDenied("Нельзя создать начисление на чужой счет")
        serializer.save()