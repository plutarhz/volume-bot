from pybit.unified_trading import HTTP

# Инициализация клиента
client = HTTP(api_key='your_api_key', api_secret='your_api_secret')

# Выводим доступные методы объекта client
print(dir(client))
