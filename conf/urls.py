from django.contrib import admin
from django.urls import path

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]

if not settings.DEBUG:
    from django_otp.admin import OTPAdminSite

    admin.site.__class__ = OTPAdminSite
