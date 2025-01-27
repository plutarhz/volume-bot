import json
import os
from utils.db_manager import get_config, update_config

# Путь к конфигурационному файлу
CONFIG_FILE_PATH = "config.json"

def load_config():
    """Загружает данные из конфигурационного файла."""
    if not os.path.exists(CONFIG_FILE_PATH):
        raise FileNotFoundError(f"Конфигурационный файл {CONFIG_FILE_PATH} не найден.")
    
    with open(CONFIG_FILE_PATH, "r") as f:
        try:
            config_data = json.load(f)
            return config_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка чтения конфигурации: {e}")

# Функция для загрузки конфигурации

# def load_config():
#     # Загружаем параметры из базы данных
#     # api_key = get_config('api_key')
#     # api_secret = get_config('api_secret')
#     volume_threshold = get_config('volume_threshold')
#     num_candles = get_config('num_candles')
#     multiplier = get_config('multiplier')

#     # Если параметр не найден в базе данных, загружаем из конфигурационного файла
#     if not volume_threshold or not num_candles or not multiplier:
#         with open("config.json", "r") as f:
#             config = json.load(f)
#             volume_threshold = config['volume_threshold']
#             num_candles = config['num_candles']
#             multiplier = config['multiplier']

#     return {
#         'volume_threshold': int(volume_threshold),
#         'num_candles': int(num_candles),
#         'multiplier': int(multiplier),
#     }


# # Функция для обновления параметра конфигурации в базе данных
# def update_user_param(parameter, value):
#     update_config(parameter, value)

def get_api_key():
    """Получает API ключ из конфигурации."""
    config = load_config()
    return config.get("api_key", None)

def get_api_secret():
    """Получает API секрет из конфигурации."""
    config = load_config()
    return config.get("api_secret", None)

def get_telegram_token():
    """Получает токен Telegram бота."""
    config = load_config()
    return config.get("telegram_token", None)

def get_chat_id():
    """Получает chat_id Telegram."""
    config = load_config()
    return config.get("chat_id", None)

def get_volume_threshold():
    """Получает порог объема для фильтрации фьючерсов."""
    config = load_config()
    return config.get("volume_threshold", 100000000)  # Default threshold is 100 million

def get_num_candles():
    """Получает количество свечей для расчета среднего turnover."""
    config = load_config()
    return config.get("num_candles", 10)  # Default to 10 candles

def get_multiplier():
    """Получает множитель для сравнения turnover."""
    config = load_config()
    return config.get("multiplier", 5)  # Default multiplier is 5
