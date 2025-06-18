import logging
import time

# Создаем логгер для текущего модуля
logger = logging.getLogger(__name__)
# Создание обработчика вывода логов в консоль 
handler = logging.StreamHandler()
# Форматируем сообщения логов с указанием времени, уровня и сообщения
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s; %(message)s', )
handler.formatter = formatter
# Добавляем обработчик в логгер
logger.addHandler(handler)
# Устанавливаем уровень логирования — информационные сообщения
logger.setLevel(logging.INFO)


class LoggingProductsMiddleware(object):
    # Инициализация middleware, принимается функция обработки запроса 
    def __init__(self, get_response):
        self.get_response = get_response
        # Одноразовая настройка при старте middleware

    # вызывается при каждом HTTP-запросе
    def __call__(self, request):
        # время начала обработки запроса
        start_time = time.time()
        # Формируем словарь с данными о запросе
        request_data = {
            'request': request.method,
            'ip_adress': request.META.get('REMOTE_ADDR'),
            'path': request.path,
            'user': request.user if request.user.is_authenticated else 'Anonymous',

        }
        # Логируем информацию о входящем запросе
        logger.info(request_data)
        # Сохраняем данные запроса для повторного логирования после обработки
        method = request.method
        ip_address = request.META.get('REMOTE_ADDR')
        path = request.path

        # Вызываем следующий обработчик
        response = self.get_response(request)
        # длительность обработки запроса
        duration = time.time() - start_time
        user = request.user if request.user.is_authenticated else 'Anonymous'

        #словарь после обработки
        request_data = {
            'request': method,
            'ip_adress': ip_address,
            'path': path,
            'user': user,
        }
        # инфа об ответте
        response_dict = {
            'status_code': response.status_code,
            'duration': duration,
        }
        logger.info(request_data)
        logger.info(response_dict)

        return response
