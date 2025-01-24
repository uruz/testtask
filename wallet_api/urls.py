from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_json_api.schemas.openapi import SchemaGenerator

from wallet_api.apicore.views import ping, WalletViewSet, TransactionViewSet
from rest_framework import routers
router = routers.DefaultRouter()
router.register('wallets', WalletViewSet)
router.register('transactions', TransactionViewSet)

openapi_schema = get_schema_view(
    title='Wallet API',
    version='1.0',
    generator_class=SchemaGenerator,
)

urlpatterns = [
    path('ping/', ping),
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('openapi/', openapi_schema),
]
