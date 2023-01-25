from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from conf.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', HomeView.as_view(), name='home'),
]

if not settings.DEBUG:
    from django_otp.admin import OTPAdminSite

    admin.site.__class__ = OTPAdminSite

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
