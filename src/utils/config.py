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
