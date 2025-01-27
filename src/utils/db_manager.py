import sqlite3


# Функция для получения соединения с базой данных
def get_db_connection():
    """Получаем соединение с базой данных."""
    conn = sqlite3.connect('config.db')
    return conn

# Функция для создания таблицы конфигураций пользователей
def create_config_table():
    """Создает таблицу для хранения конфигурации пользователей."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            user_id INTEGER PRIMARY KEY,  -- Уникальный идентификатор пользователя
            multiplier INTEGER,           -- Множитель
            num_candles INTEGER           -- Количество свечей
        )
    ''')
    conn.commit()
    conn.close()

# Функция для получения параметров конфигурации пользователя по его ID
def get_config(user_id):
    """Получает конфигурацию пользователя по его уникальному ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT multiplier, num_candles
        FROM config
        WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            'multiplier': result[0],
            'num_candles': result[1]
        }
    return None  # Если данных нет, возвращаем None

# Функция для добавления или обновления конфигурации пользователя
def update_config(user_id, multiplier, num_candles):
    """Добавляет или обновляет параметры конфигурации пользователя."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO config (user_id, multiplier, num_candles)
        VALUES (?, ?, ?, ?)
    ''', (user_id, multiplier, num_candles))
    conn.commit()
    conn.close()

def add_user(user_id, default_multiplier=2, default_num_candles=10):
    """
    Добавляет нового пользователя в базу данных, если его еще нет.
    Если пользователь существует, ничего не делает.
    """
    if user_exists(user_id):
        print(f"Пользователь с user_id {user_id} уже существует в базе данных.")
        return  # Если пользователь уже есть, просто выходим

    # Если пользователя нет, добавляем его с параметрами по умолчанию
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO config (user_id, multiplier, num_candles)
        VALUES (?, ?, ?)
    ''', (user_id, default_multiplier, default_num_candles))
    conn.commit()
    conn.close()
    print(f"Пользователь с user_id {user_id} успешно добавлен с параметрами по умолчанию.")
    
def user_exists(user_id):
    """
    Проверяет, существует ли пользователь в базе данных.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM config WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None  # True, если пользователь существует, иначе False

def update_user(user_id, num_candles=None, multiplier=None):
    """Обновляет параметры пользователя в базе данных."""
    conn = sqlite3.connect('config.db')
    cursor = conn.cursor()

    if num_candles is not None:
        cursor.execute("UPDATE config SET num_candles = ? WHERE user_id = ?", (num_candles, user_id))
    if multiplier is not None:
        cursor.execute("UPDATE config SET multiplier = ? WHERE user_id = ?", (multiplier, user_id))

    conn.commit()
    conn.close()
