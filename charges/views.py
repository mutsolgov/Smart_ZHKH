import io
from datetime import date
from django.http import FeliResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Charge
from .serializers import ChargeSerializer

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

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


class ReceiptView(APIVies):
    permission_classes = [IsAuthenticated]

    def get(self, request, charge_id):
        try:
            charge = Charge.objects.get(pk=charge_id)
        except Charge.DoesNotExist:
            raise Http404("Начисление не найдено")
        
        if charge.account.user != request.user:
            raise PermissionDenied("Доступ запрешен")
        
        user = request.user
        account = charge.account
        service_name = charge.service_name
        amount = charge.amount
        period = charge.period
        created_date = date.today()

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)

        left_margin = 20 * mm
        top_margin = 280 * mm

        p.setFont("Helvetica-Bold", 16)
        p.drawString(left_margin, top_margin, "КВИТАНЦИЯ № {}".format(charge_id))

