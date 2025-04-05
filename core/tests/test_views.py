from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import MenuItem, Order


class OrderViewsTestCase(TestCase):

    def setUp(self):
        """Создание пользователя и элементов меню"""
        self.user = User.objects.create_user(
            username='testuser', password='password'
        )
        self.client.login(username='testuser', password='password')
        self.menu_item = MenuItem.objects.create(name='Pizza', price=10.0)

    def test_order_create_view(self):
        """Тестирование создания заказа"""
        url = reverse('order_create')
        data = {
            'table_number': 1,
            'status': 'pending',
            'items': [self.menu_item.id],
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(id=1)

        self.assertIsNotNone(order)
        self.assertEqual(order.table_number, 1)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.total_price, 10.0)

    def test_order_detail_view(self):
        """Тестирование отображения деталей заказа"""
        order = Order.objects.create(
            table_number=1, status='pending', total_price=10.0
        )
        order.items.add(self.menu_item)
        order.save()
        url = reverse('order_detail', args=[order.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Стол: {order.table_number}')
        self.assertContains(response, f'Заказ #{order.id}')

    def test_order_update_view(self):
        """Тестирование обновления заказа"""
        order = Order.objects.create(table_number=1, status='pending')
        order.items.add(self.menu_item)
        order.total_price = order.items.first().price
        order.save()
        url = reverse('order_update', args=[order.id])
        data = {
            'table_number': 2,
            'status': 'ready',
            'items': [self.menu_item.id],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()

        self.assertEqual(order.table_number, 2)
        self.assertEqual(order.status, 'ready')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.total_price, 10.0)

    def test_order_list_view(self):
        """Тестирование отображения списка заказов"""
        order1 = Order.objects.create(
            table_number=1, status='pending', total_price=10.0
        )
        order1.items.add(self.menu_item)
        order1.save()
        order2 = Order.objects.create(
            table_number=2, status='paid', total_price=20.0
        )
        order2.items.add(self.menu_item)
        order2.save()
        url = reverse('order_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Заказ #{order1.id}')
        self.assertContains(response, f'Заказ #{order2.id}')

    def test_order_delete_view(self):
        """Тестирование удаления заказа"""
        order = Order.objects.create(table_number=1, status='pending')
        order.items.add(self.menu_item)
        order.total_price = order.items.first().price
        order.save()
        url = reverse('order_delete', args=[order.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(id=order.id)

    def test_revenue_for_shift_view(self):
        """Тестирование отображения выручки за смену"""
        order1 = Order.objects.create(table_number=1, status='paid')
        order1.items.add(self.menu_item)
        order1.total_price = 10.0
        order1.save()
        order2 = Order.objects.create(table_number=2, status='paid')
        order2.items.add(self.menu_item)
        order2.total_price = 20.0
        order2.save()
        url = reverse('revenue_for_shift')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '30.00')

    def tearDown(self):
        """Удаляем тестовые данные"""
        self.user.delete()
        self.menu_item.delete()
