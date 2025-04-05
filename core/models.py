from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название блюда')
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name='Цена'
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField(verbose_name='Номер стола')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES,
        default='pending', verbose_name='Статус'
    )
    items = models.ManyToManyField(
        MenuItem, related_name='orders',
        verbose_name='Блюда'
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name='Общая стоимость', default=0
    )

    def __str__(self):
        return (
            f'Заказ {self.id} (Стол {self.table_number}) - '
            f'{self.get_status_display()}'
        )
