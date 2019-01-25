from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('tome-administration/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('db/', include('db.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
