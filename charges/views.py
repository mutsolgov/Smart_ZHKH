import io
from datetime import date
from django.http import FileResponse, Http404
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


class ReceiptView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, charge_id):
        # 1. Получаем объект Charge, проверяем, что он существует
        try:
            charge = Charge.objects.get(pk=charge_id)
        except Charge.DoesNotExist:
            raise Http404("Начисление не найдено")
        
        # 2. Проверяем, что начисление принадлежит текущему пользователю
        if charge.account.user != request.user:
            raise PermissionDenied("Доступ запрешен")
        
        # 3. Подготавливаем данные для квитанции
        user = request.user
        account = charge.account
        service_name = charge.service_name
        amount = charge.amount
        period = charge.period
        created_date = date.today()

        # 4. Генерация PDF
        buffer = io.BytesIO()
        # A4, портрет
        p = canvas.Canvas(buffer, pagesize=A4)
        
        # Отступы
        left_margin = 20 * mm
        top_margin = 280 * mm

        # 4.1. Шапка квитанции
        p.setFont("Helvetica-Bold", 16)
        p.drawString(left_margin, top_margin, "КВИТАНЦИЯ № {}".format(charge_id))

        p.setFont("Helvetica", 10)
        p.drawString(left_margin, top_margin - 20, f"Дата формирования: {created_date.strftime('%d.%m.%Y')}")
        p.drawString(left_margin, top_margin - 35, f"ФИО: {user.full_name}")
        p.drawString(left_margin, top_margin - 50, f"Адрес: {user.adress}")
        p.drawString(left_margin, top_margin - 65, f"Лицевой счет: {account.number}")
        p.drawString(left_margin, top_margin - 80, f"Период: {period.strftime('%m.%Y')}")

        # 4.2. Таблица услуг (заголовки)
        table_top = top_margin - 110
        p.setFont("Helvetica-Bold", 12)
        p.drawString(left_margin, table_top, "Услуга")
        p.drawString(left_margin + 100 * mm, table_top, "Сумма (₽)")
        
        # 4.3. Строка с нашей услугой
        p.setFont("Helvetica", 10)
        p.drawString(left_margin, table_top - 20, service_name)
        p.drawString(left_margin + 100 * mm, table_top - 20, f"{amount:.2f}")

        # 4.4. Итоговая сумма (выравнивание справа)
        total_y = table_top - 50
        p.setFont("Helvetica-Bold", 12)
        p.drawString(left_margin, total_y, "Итого к оплате:")
        # Вычисляем ширину текста для выравнивания по правому краю
        total_text = f"{amount:.2f} ₽"
        text_width = p.stringWidth(total_text, "Helvetica-Bold", 12)
        p.drawString(A4[0] - left_margin - text_width, total_y, total_text)

        # 4.5. Подпись(место для подписиб необязательно)
        p.setFont("helvetica", 10)
        p.drawString(left_margin, total_y - 40, "Подпись плательщика: _______________")

        # Завершаем страницу
        p.showPage()
        p.save()

        buffer.seek(0)
        filename = f"receipt_{charge_id}.pdf"
        # 5. Возвращаем как FileResponse с attachment
        return FileResponse(buffer, as_attachment=True, filename=filename)
