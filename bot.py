import telebot  # библиотека telebot
from config import token  # импорт токена

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
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
        else:
            bot.ban_chat_member(chat_id, user_id)  # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(func=lambda message: True)
def check_links(message):
    """Проверка сообщений на наличие ссылок и бан пользователя, если ссылка найдена."""
    if "https://" in message.text or "http://" in message.text:
        chat_id = message.chat.id  # сохранение id чата
        user_id = message.from_user.id  # сохранение id пользователя
        user_status = bot.get_chat_member(chat_id, user_id).status  # получение статуса пользователя

        # проверка пользователя
        if user_status != 'administrator' and user_status != 'creator':
            bot.ban_chat_member(chat_id, user_id)  # Бан пользователя
            bot.reply_to(message, f"Пользователь @{message.from_user.username} был забанен за отправку ссылки.")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, "Привет, новичок!")
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

bot.infinity_polling(none_stop=True)

