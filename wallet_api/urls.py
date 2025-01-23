from django.contrib import admin
from django.urls import path
from wallet_api.apicore.views import ping

urlpatterns = [
    path('ping/', ping),
    path('admin/', admin.site.urls),
]
