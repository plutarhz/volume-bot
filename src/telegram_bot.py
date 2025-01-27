import telebot
from telebot import types
from utils.db_manager import create_config_table, add_user, get_config,update_user
from utils.config import load_config

# Инициализация базы данных
create_config_table()
config = load_config()

bot = telebot.TeleBot(config['telegram_token'])

# Состояния пользователей
user_states = {}

def set_user_state(user_id, state):
    """Устанавливает состояние пользователя."""
    user_states[user_id] = state

def get_user_state(user_id):
    """Получает текущее состояние пользователя."""
    return user_states.get(user_id)

def reset_user_state(user_id):
    """Сбрасывает состояние пользователя."""
    if user_id in user_states:
        del user_states[user_id]

@bot.message_handler(commands=['start'])
def handle_start(message):
    """Команда /start. Регистрирует нового пользователя или выводит его текущие параметры с кнопками."""
    user_id = message.chat.id

    # Проверяем, есть ли у пользователя запись в базе данных
    user_config = get_config(user_id)

    if user_config is None:
        # Добавляем нового пользователя с параметрами по умолчанию
        add_user(user_id, config['num_candles'], config['multiplier'])
        bot.send_message(message.chat.id, "Здравствуйте! Ваши параметры бота были установлены по умолчанию.")
    else:
        # Если пользователь уже есть в базе, отправляем текущие параметры
        bot.send_message(message.chat.id, f"Здравствуйте! Ваши текущие параметры бота: \n"
                                          f"Количество свечей: {user_config['num_candles']}\n"
                                          f"Множитель: {user_config['multiplier']}")
    show_main_menu(message.chat.id)

def show_main_menu(user_id):
    """Отображает главное меню с кнопками."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Изменить количество свечей"),
        types.KeyboardButton("Изменить множитель"),
        types.KeyboardButton("Показать текущие настройки")
    )
    bot.send_message(user_id, "Выберите действие:", reply_markup=markup)


def handle_parameter_update(message, param_name, param_type):
    """Обработка обновления параметров пользователя."""
    user_id = message.chat.id
    try:
        value = param_type(message.text)
        if value <= 0:
            raise ValueError("Значение должно быть больше нуля.")

        # Обновляем параметр в базе данных
        if param_name == 'num_candles':
            update_user(user_id, num_candles=value)
        elif param_name == 'multiplier':
            update_user(user_id, multiplier=value)

        bot.reply_to(message, f"{param_name} успешно обновлен: {value}")
        reset_user_state(user_id)
        show_main_menu(user_id)
    except (ValueError, TypeError):
        bot.reply_to(message, "Ошибка! Введите корректное число больше нуля.")

def show_user_config(user_id):
    """Отображает текущие настройки пользователя."""
    user_config = get_config(user_id)
    if user_config:
        bot.send_message(user_id, f"Ваши текущие параметры: \n"
                                  f"Количество свечей: {user_config['num_candles']}\n"
                                  f"Множитель: {user_config['multiplier']}")
    else:
        bot.send_message(user_id, "Настройки не найдены. Пожалуйста, используйте /start для инициализации.")

        

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    """Обрабатывает выбор действия с кнопок и ввод параметров."""
    user_id = message.chat.id
    text = message.text
    state = get_user_state(user_id)

    if state == 'awaiting_num_candles':
        handle_parameter_update(message, 'num_candles', int)
    elif state == 'awaiting_multiplier':
        handle_parameter_update(message, 'multiplier', float)
    elif text == "Изменить количество свечей":
        set_user_state(user_id, 'awaiting_num_candles')
        bot.reply_to(message, "Введите количество свечей (например, 10):")
    elif text == "Изменить множитель":
        set_user_state(user_id, 'awaiting_multiplier')
        bot.reply_to(message, "Введите множитель (например, 2):")
    elif text == "Показать текущие настройки":
        show_user_config(user_id)
    else:
        bot.reply_to(message, "Неизвестная команда. Используйте кнопки для выбора действия.")

def main():
    print("Бот запущен, начинаю прослушку сообщений...")
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()


