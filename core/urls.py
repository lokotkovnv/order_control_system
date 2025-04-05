from django.urls import path

from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/edit/', views.order_update, name='order_update'),
    path('<int:order_id>/delete/', views.order_delete, name='order_delete'),
    path('revenue/', views.revenue_for_shift, name='revenue_for_shift'),
]
