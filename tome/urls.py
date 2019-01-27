from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

# Project URLconf
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('tome-administration/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('db/', include('db.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Debug Toolbar enabled while in debug mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
