# Order Control System

## Order Control System — это веб-приложение для управления заказами в кафе, реализованное с использованием Django. Приложение позволяет создавать, редактировать, удалять заказы, а также отслеживать выручку по статусу заказов. Также реализован REST API для взаимодействия с заказами.

### Функции:

1. Создание нового заказа.

2. Редактирование существующего заказа.

3. Удаление заказа.

4. Поиск по номеру стола и статусу.

5. Отображение выручки за смену (по заказам с статусом "оплачено").

6. REST API для работы с заказами.

### Использованные технологии: 

1. Python 3.9.10

2. Django 4.2.20

3. SQLite

4. Django REST Framework

### Установка:

Клонируйте репозиторий:

git clone https://github.com/yourusername/order_control_system.git 

cd order_control_system

Создайте и активируйте виртуальное окружение:

python3 -m venv venv

source venv/bin/activate # для macOS/Linux 
source venv/Scripts/activate # для Windows

Установите зависимости:

pip install -r requirements.txt

Примените миграции базы данных:

python manage.py migrate

Создайте суперпользователя для административного интерфейса:

python manage.py createsuperuser

Запустите сервер:

python manage.py runserver

Откройте браузер и перейдите по адресу http://127.0.0.1:8000/orders/, чтобы увидеть приложение в действии.

### Использование

Работа с заказами через веб-интерфейс

Создание заказа: Перейдите на страницу создания нового заказа и выберите стол, статус и блюда для заказа.

Редактирование заказа: На странице деталей заказа выберите кнопку для редактирования заказа.

Удаление заказа: На странице деталей заказа выберите кнопку для удаления заказа.

### Работа с заказами через REST API

Приложение предоставляет API для работы с заказами. Пример использования:

Получение списка заказов: GET /api/orders/

Создание нового заказа: POST /api/orders/ Content-Type: application/json { "table_number": 1, "status": "pending", "items": [1, 2] # Список ID выбранных блюд }

Получение подробностей заказа: GET /api/orders/{order_id}/

Обновление заказа: PUT /api/orders/{order_id}/ Content-Type: application/json { "table_number": 2, "status": "ready", "items": [3] }

Удаление заказа: DELETE /api/orders/{order_id}/

Для доступа к API используйте инструменты, такие как Postman или cURL.

### Отчеты

Выручка за смену: Перейдите на страницу "Выручка за смену", чтобы увидеть общую выручку, рассчитанную по заказам со статусом "оплачено".

### Тестирование

Для запуска тестов используйте следующую команду:

python manage.py test

Тесты находятся в директории core/tests/.

### Автор

Локотков Никита

https://github.com/lokotkovnv
