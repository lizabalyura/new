"""
ASGI config for labs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

# Импорт маршрутов WebSocket 
import library.routing
# Стандартный способ получить ASGI-приложение для обработки HTTP-запросов
from django.core.asgi import get_asgi_application

#настройка поддержки WebSocket в Channels
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack



# Устанавливаем переменную окружения для настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labs.settings')

#главное ASGI-приложение, которое умеет различать HTTP и WebSocket
application = ProtocolTypeRouter({
    # http запросы идут через стандарт джанго-приложение
    "http": get_asgi_application(),
    # Все WebSocket-запросы будут обрабатываться ниже
    "websocket": AuthMiddlewareStack( # Добавляет поддержку аутентификации пользователей
        URLRouter(  # Подключает маршруты для WebSocket
            library.routing.websocket_urlpatterns # список юрлов для вебсокета
        )
    ),
})