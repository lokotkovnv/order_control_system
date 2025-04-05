from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .forms import OrderForm
from .models import MenuItem, Order
from .serializers import OrderSerializer


def order_list(request: HttpRequest) -> HttpResponse:
    """Список всех заказов с поиском по номеру стола или статусу"""
    search_query = request.GET.get('search', '').strip()

    if search_query:
        status_choices = dict(Order.STATUS_CHOICES)
        status_search = None

        for key, value in status_choices.items():
            if value.lower() and search_query.lower() in value.lower():
                status_search = key
                break

        orders = Order.objects.filter(
            Q(table_number__icontains=search_query) |
            Q(status=status_search)
        )
    else:
        orders = Order.objects.all()

    return render(request, 'core/order_list.html', {
        'orders': orders,
        'search_query': search_query,
    })


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    """Детали конкретного заказа"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'core/order_detail.html', {'order': order})


def order_create(request: HttpRequest) -> HttpResponse:
    """Создание нового заказа"""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                order = form.save()
                order.items.set(form.cleaned_data['items'])
                total_price = sum(item.price for item in order.items.all())
                order.total_price = total_price
                order.save()

                messages.success(request, f'Заказ #{order.id} успешно создан.')
                return redirect('order_detail', order.id)
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            messages.error(
                request, 'Форма содержит ошибки. Пожалуйста, исправьте их.'
            )
    else:
        form = OrderForm()

    menu_items_with_price = MenuItem.objects.all()

    return render(request, 'core/order_form.html', {
        'form': form,
        'menu_items_with_price': menu_items_with_price
    })


def order_update(request: HttpRequest, order_id: int) -> HttpResponse:
    """Редактирование существующего заказа"""
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            order.items.set(form.cleaned_data['items'])
            total_price = sum(item.price for item in order.items.all())
            order.total_price = total_price
            order.save()
            return redirect('order_detail', order.id)
    else:
        form = OrderForm(instance=order)

    menu_items_with_price = MenuItem.objects.all()

    return render(request, 'core/order_form.html', {
        'form': form,
        'menu_items_with_price': menu_items_with_price
    })


def order_delete(request: HttpRequest, order_id: int) -> HttpResponse:
    """Удаление заказа"""
    try:
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        messages.success(request, 'Заказ был успешно удален.')
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден.')
    return redirect('order_list')


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с заказами через REST API."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'table_number']
    search_fields = ['status', 'table_number']


def revenue_for_shift(request: HttpRequest) -> HttpResponse:
    """Выручка за смену (по заказам со статусом 'оплачено')"""
    paid_orders = Order.objects.filter(status='paid')
    total_revenue = sum(order.total_price for order in paid_orders)
    return render(request, 'core/revenue_for_shift.html', {
        'total_revenue': total_revenue,
        'paid_orders': paid_orders,
    })
