import telebot 
from config import token 

bot = telebot.TeleBot(token)
USERS_FILE = 'users_info.txt'


def load_users():
    """Загрузить существующих пользователей из файла в словарь по user_id."""
    users = {}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    user_data = line.split('|')  # Разделяем данные по символу '|'
                    user_info = {
                        'id': int(user_data[0]),
                        'first_name': user_data[1],
                        'last_name': user_data[2],
                        'username': user_data[3],
                        'language_code': user_data[4],
                        'is_bot': user_data[5] == 'True'
                    }
                    users[user_info['id']] = user_info
    except FileNotFoundError:
        # файл не найден - возвращаем пустой словарь
        pass
    return users


def save_user(user_data):
    """Сохранить информацию о пользователе в текстовом формате, только если это новый user_id."""
    users = load_users()
    if user_data['id'] in users:
        # пользователь уже сохранен
        return False
    with open(USERS_FILE, 'a', encoding='utf-8') as f:
        # Сохраняем данные в формате: id|first_name|last_name|username|language_code|is_bot
        f.write(f"{user_data['id']}|{user_data['first_name']}|{user_data['last_name']}|{user_data['username']}|{user_data['language_code']}|{user_data['is_bot']}\n")
    return True


def user_info_from_message(message):
    """Извлечь информацию о пользователе из сообщения."""
    user = message.from_user
    user_info = {
        'id': user.id,
        'first_name': user.first_name or '',
        'last_name': user.last_name or '',
        'username': user.username or '',   
        'language_code': user.language_code or '',
        'is_bot': user.is_bot,
    }
    return user_info


@bot.message_handler(commands=['start'])
def start(message):
    user_info = user_info_from_message(message)
    save_user(user_info)  # Сохраняем информацию о пользователе
    bot.reply_to(message, "Привет! Я бот для управления чатом.")


@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:  # проверка на то, что эта команда была вызвана в ответ на сообщение
        chat_id = message.chat.id  # сохранение id чата
        user_id = message.reply_to_message.from_user.id  # сохранение id пользователя
        user_status = bot.get_chat_member(chat_id, user_id).status  # получение статуса пользователя
        # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        elif "https://" in message.text or "http://" in message.text:
            bot.ban_chat_member(chat_id, user_id)  # Бан пользователя
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен за отправку ссылки.")
        else:
            bot.ban_chat_member(chat_id, user_id)  # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")


bot.infinity_polling(none_stop=True)

