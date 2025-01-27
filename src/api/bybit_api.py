from pybit.unified_trading import HTTP
import time
from datetime import datetime, timezone

# Инициализация клиента Bybit API с использованием pybit.unified_trading
def get_client(api_key, api_secret):
    client = HTTP(api_key=api_key, api_secret=api_secret)
    return client

# Получаем данные по фьючерсам с Bybit API
def get_futures_data(client):
    print("Отправка запроса к API Bybit...")

    try:
        # Используем метод get_tickers с категорией "linear" для получения данных о линейных фьючерсах
        response = client.get_tickers(category="linear")

        # Проверяем, что структура ответа корректна
        if response.get('retCode') == 0:
            print("Данные успешно получены с Bybit API.")
            # Извлекаем массив фьючерсов из response['result']['list']
            return response['result'].get('list', [])
        else:
            print(f"Ошибка при запросе к API: {response.get('retMsg', 'Неизвестная ошибка')}")
            return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None

def filter_futures_by_volume(futures_data):
    print("Фильтрация фьючерсов по объему (больше 80 млн USDT)...")
    filtered_data = []
    
    for future in futures_data:
        # Извлекаем необходимые данные: volume_24h и lastPrice
        try:
            volume_24h = float(future.get('volume24h', 0))
            last_price = float(future.get('lastPrice', 0))
            
            # Проверим, что значения корректны
            if volume_24h <= 0 or last_price <= 0:
                print(f"Невалидные данные для фьючерса {future['symbol']}: volume_24h={volume_24h}, lastPrice={last_price}")
                continue

            # Вычисляем объем за 24 часа в долларах
            volume_in_usd = volume_24h * last_price

            # Фильтруем фьючерсы с объемом >= 80 000 000 USDT
            if volume_in_usd >= 80000000:
                filtered_data.append(future)
        except Exception as e:
            print(f"Ошибка при обработке фьючерса {future.get('symbol', 'Unknown')}: {e}")

    print(f"Отфильтровано {len(filtered_data)} фьючерсов.")
    
    # Выводим информацию о каждом отфильтрованном фьючерсе
    # for future in filtered_data:
    #     symbol = future.get('symbol', 'Unknown')
    #     last_price = future.get('lastPrice', 'Unknown')
    #     turnover_24h = future.get('turnover24h', 'Unknown') 
    #     print(f"  - Symbol: {symbol}, Last: {last_price}, Turnover 24h: {turnover_24h}")

    
    return filtered_data

def update_data_everyday(api_key, api_secret, update_function):
    client = get_client(api_key, api_secret)
    
    while True:
        now = datetime.now(timezone.utc)
        # Если текущее время 00:01 UTC, то обновляем данные
        if now.hour == 0 and now.minute == 1:
            print("Запуск обновления данных фьючерсов...")
            futures_data = get_futures_data(client)
            if futures_data:
                filtered_data = filter_futures_by_volume(futures_data)
                print("Обновление данных...")
                update_function(filtered_data)
            else:
                print("Не удалось получить данные для обновления.")
        else:
            # Если время не 00:01, просто ожидаем
            print(f"Ждем следующего обновления. Текущее время: {now.isoformat()}")
        time.sleep(600)  # Пауза на 10 минут, чтобы не перегружать API

def get_kline(client, symbol, interval="5", limit=10):
    """
    Запрашивает данные о свечах для указанного символа.
    :param client: объект клиента Bybit.
    :param symbol: название фьючерса.
    :param interval: интервал свечей в минутах (по умолчанию "5").
    :param limit: количество запрашиваемых свечей (по умолчанию 10).
    :return: словарь с данными о свечах.
    """
    try:
        response = client.get_kline(category="linear", symbol=symbol, interval=interval, limit=limit)
        return response.get("result", {})
    except Exception as e:
        print(f"Ошибка при получении свечей для {symbol}: {e}")
        return {}


