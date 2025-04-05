from django.contrib import admin

from .models import MenuItem, Order

admin.site.register(Order)
admin.site.register(MenuItem)
