from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChargeViewSet, ReceiptView

router = DefaultRouter()
router.register(r'', ChargeViewSet, basename='charges')

urlpatterns = [
    path('', include(router.urls)),
    path('receipts/<int:charge_id>/', ReceiptView.as_view(), name='receipt'),
]