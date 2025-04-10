from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', include('core.urls')),
    path('api/', include('core.api_urls')),
]
