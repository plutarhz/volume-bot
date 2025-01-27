# import os
# import json

# def write_to_json(data, filepath):
#     # Проверка, существует ли файл
#     if os.path.exists(filepath):
#         print(f"Файл {filepath} уже существует.")
#     else:
#         # Если файл не существует, создаем его
#         with open(filepath, "w") as json_file:
#             json.dump(data, json_file, indent=4)
#         print(f"Файл {filepath} был успешно создан и данные сохранены.")

# def load_from_json(filepath):
#     """Загружает данные из JSON файла."""
#     try:
#         with open(filepath, 'r') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         print(f"Файл {filepath} не найден.")
#         return None
#     except json.JSONDecodeError:
#         print(f"Ошибка декодирования JSON файла {filepath}.")
#         return None   
    
# import json
# from pybit.unified_trading import HTTP
# import os
# from api.bybit_api import get_client


# def get_futures_data(client):
#     """Получает данные о фьючерсах из Bybit API."""
#     print("Запрос данных о фьючерсах с Bybit API...")
#     try:
#         response = client.get_tickers(category="linear")
#         if response.get('retCode') == 0:
#             print("Данные успешно получены.")
#             return response['result'].get('list', [])
#         else:
#             print(f"Ошибка API: {response.get('retMsg', 'Неизвестная ошибка')}")
#             return []
#     except Exception as e:
#         print(f"Произошла ошибка при запросе к API: {e}")
#         return []
  
# def filter_futures_by_turnover(futures_data, threshold):
#     """Фильтрует фьючерсы по значению turnover24h, превышающему заданный порог."""
#     print(f"Фильтрация фьючерсов с turnover24h > {threshold} USDT...")
#     filtered_data = [
#         future for future in futures_data
#         if float(future.get('turnover24h', 0)) > threshold
#     ]
#     print(f"Количество отфильтрованных фьючерсов: {len(filtered_data)}")
#     return filtered_data

# def save_to_json(data, filepath):
#     """Сохраняет данные в JSON файл."""
#     try:
#         with open(filepath, 'w') as file:
#             json.dump(data, file, indent=4)
#         print(f"Данные успешно сохранены в файл {filepath}.")
#     except Exception as e:
#         print(f"Ошибка при сохранении данных в файл {filepath}: {e}")

# def load_from_json(filepath):
#     """Загружает конфигурацию из JSON файла."""
#     try:
#         with open(filepath, 'r') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         print(f"Файл конфигурации {filepath} не найден.")
#         return None
#     except json.JSONDecodeError:
#         print(f"Ошибка чтения конфигурации из {filepath}. Проверьте формат JSON.")
#         return None  
    
# def create_futures_data_file(api_key, api_secret, filepath, threshold=100000000):
#     """Создает файл с фьючерсами, чей turnover за 24 часа превышает threshold."""
#     print(f"Получение данных с API и проверка фьючерсов с turnover > {threshold} USDT за 24 часа...")
    
#     # Получаем клиент для API с помощью конфигурации
#     client = get_client(api_key, api_secret)
    
#     # Получаем все данные о фьючерсах
#     futures_data = get_futures_data(client)
    
#     # Фильтруем фьючерсы по threshold turnover
#     filtered_futures = filter_futures_by_turnover(futures_data, threshold)
    
#     # Проверяем, есть ли отфильтрованные данные
#     if filtered_futures:
#         save_to_json(filtered_futures, filepath)  # Сохраняем только отфильтрованные данные
#     else:
#         print("Нет фьючерсов с turnover > 100,000,000 USDT за 24 часа.") 

import json
import os
from pybit.unified_trading import HTTP
from api.bybit_api import get_client

def get_futures_data(client):
    """Получает данные о фьючерсах из Bybit API."""
    print("Запрос данных о фьючерсах с Bybit API...")
    try:
        response = client.get_tickers(category="linear")
        if response.get('retCode') == 0:
            print("Данные успешно получены.")
            return response['result'].get('list', [])
        else:
            print(f"Ошибка API: {response.get('retMsg', 'Неизвестная ошибка')}")
            return []
    except Exception as e:
        print(f"Произошла ошибка при запросе к API: {e}")
        return []

def filter_futures_by_turnover(futures_data, threshold):
    """Фильтрует фьючерсы по значению turnover24h, превышающему заданный порог."""
    print(f"Фильтрация фьючерсов с turnover24h > {threshold} USDT...")
    filtered_data = [
        future for future in futures_data
        if float(future.get('turnover24h', 0)) > threshold
    ]
    print(f"Количество отфильтрованных фьючерсов: {len(filtered_data)}")
    return filtered_data

def save_to_json(data, filepath):
    """Сохраняет данные в JSON файл."""
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Данные успешно сохранены в файл {filepath}.")
    except Exception as e:
        print(f"Ошибка при сохранении данных в файл {filepath}: {e}")

def clear_json_file(filepath):
    """Очищает содержимое JSON файла перед записью."""
    try:
        with open(filepath, 'w') as file:
            file.write('[]')  # Очищаем файл, записывая пустой массив
        print(f"Файл {filepath} успешно очищен.")
    except Exception as e:
        print(f"Ошибка при очистке файла {filepath}: {e}")

def create_futures_data_file(api_key, api_secret, filepath, threshold=100000000):
    """
    Создает файл с фьючерсами, чей turnover за 24 часа превышает threshold.
    Файл очищается перед созданием данных.
    """
    print(f"Создание файла с фьючерсами, turnover > {threshold} USDT за 24 часа...")
    
    # Удаляем содержимое файла перед записью
    clear_json_file(filepath)

    # Получаем клиент для API
    client = get_client(api_key, api_secret)

    # Получаем все данные о фьючерсах
    futures_data = get_futures_data(client)

    # Фильтруем фьючерсы по threshold turnover
    filtered_futures = filter_futures_by_turnover(futures_data, threshold)

    # Проверяем, есть ли отфильтрованные данные
    if filtered_futures:
        save_to_json(filtered_futures, filepath)  # Сохраняем только отфильтрованные данные
    else:
        print("Нет фьючерсов с turnover > 100,000,000 USDT за 24 часа.")

def load_from_json(filepath):
    """Загружает данные из JSON файла."""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filepath} не найден.")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка чтения JSON из {filepath}. Проверьте формат.")
        return None



    
