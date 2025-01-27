import time
import os
import json
from data.json_creator import load_from_json, create_futures_data_file
from api.bybit_api import get_client, get_kline
from utils.config import load_config
from time import sleep
from datetime import datetime, timezone


def fetch_turnover_avg_and_check(client, symbols, multiplier, num_candles):
    """Получает средний turnover за последние N свечей и проверяет превышение за последние 5 минут."""
    print(f"Получение данных turnover за последние {num_candles} свечей...")
    for symbol in symbols:
        try:
            response = get_kline(client, symbol, interval="5", limit=num_candles + 1)
            if response and "list" in response:
                candles = response["list"]
                
                if len(candles) <= num_candles:
                    print(f"Недостаточно данных для фьючерса {symbol}. Требуется {num_candles + 1} свечей.")
                    continue

                last_candle = candles[1]  # Вторая свеча — это завершенная свеча перед текущей
                previous_candles = candles[2:num_candles + 2]  # Индексы с 2 по num_candles+2
                turnovers = [float(candle[6]) for candle in previous_candles]
                avg_turnover = sum(turnovers) / len(turnovers)
                last_turnover = float(last_candle[6])
                
                if last_turnover > avg_turnover * multiplier:
                    print(
                        f"Фьючерс: {symbol}, Последний turnover: {last_turnover:.2f} USDT "
                        f"превышает средний turnover ({avg_turnover:.2f} USDT) в {multiplier} раз!"
                    )
                else:
                    print(
                        f"Фьючерс: {symbol}, Последний turnover: {last_turnover:.2f} USDT, "
                        f"Средний turnover: {avg_turnover:.2f} USDT."
                    )
            else:
                print(f"Нет данных для фьючерса {symbol}")
        except Exception as e:
            print(f"Ошибка при обработке фьючерса {symbol}: {e}")


def is_time_divisible_by_five():
    """Проверяет, кратно ли текущее время по UTC 5 минутам."""
    current_time = datetime.now(timezone.utc)
    return current_time.minute % 5 == 0


def wait_until_next_five_minute():
    """Ожидает начала ближайшего пятиминутного интервала."""
    current_time = datetime.now(timezone.utc)
    seconds_to_wait = (5 - current_time.minute % 5) * 60 - current_time.second
    print(f"Ожидание до следующего пятиминутного интервала: {seconds_to_wait} секунд.")
    time.sleep(seconds_to_wait)


def load_symbols_from_file(filepath):
    """Загружает список символов фьючерсов из JSON файла."""
    data = load_from_json(filepath)
    if not data:
        print("Файл пуст или не существует.")
        return []
    return [item["symbol"] for item in data]


def main():
    try:
        print("Загрузка конфигурации...")
        config = load_config()  # Загружаем конфигурацию
        api_key = config['api_key']
        api_secret = config['api_secret']
        volume_threshold = config['volume_threshold']
        multiplier = config['multiplier']
        num_candles = config['num_candles']
        
        client = get_client(api_key, api_secret)
        filepath = "output/futures_data.json"

        print(f"Создание или обновление файла {filepath}...")
        create_futures_data_file(api_key, api_secret, filepath, volume_threshold)

        print("Загрузка символов из файла...")
        symbols = load_symbols_from_file(filepath)
        if not symbols:
            print("Не удалось загрузить символы. Проверьте файл.")
            return

        print("Запуск циклического мониторинга turnover...")
        while True:
            if not is_time_divisible_by_five():
                wait_until_next_five_minute()

            print(f"Текущее время: {datetime.now(timezone.utc)}")
            fetch_turnover_avg_and_check(client, symbols, multiplier, num_candles)
            print("Ожидание следующего обновления...")
            sleep(300)  # Пауза 5 минут

    except KeyboardInterrupt:
        print("Программа завершена пользователем.")


if __name__ == "__main__":
    main()