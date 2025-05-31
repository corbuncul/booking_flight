import logging
from datetime import datetime

# Настройка основного логгера
logger = logging.getLogger('booking_flight')
logger.setLevel(logging.DEBUG)

# Форматтер для логов
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Хендлер для файла
file_handler = logging.FileHandler(
    f'logs/booking_flight_{datetime.now().strftime('%Y-%m-%d')}.log',
    encoding='utf-8'
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Хендлер для консоли
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Добавляем хендлеры к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)
