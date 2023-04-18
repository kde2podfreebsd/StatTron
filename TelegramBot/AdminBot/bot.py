import configparser
import os

import markups as mk
import telebot
from redis import Redis

basedir = os.path.abspath(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read(f"{basedir}/../../config.ini")

bot = telebot.TeleBot(config["TELEGRAM"]["admin_tgbot_api_token"])
redis = Redis(host=config["REDIS"]["host"], port=config["REDIS"]["port"])


@bot.message_handler(commands=["start"])
def start(message) -> None:
    try:
        if redis.get(message.chat.id) is None:
            redis.set(str(message.chat.id), "False")
            bot.send_message(
                message.chat.id,
                "Проверка пароля для админки",
                reply_markup=mk.check_password_mk,
                parse_mode="MARKDOWN",
            )

        if redis.get(message.chat.id) == b"False":
            bot.send_message(
                message.chat.id,
                "Проверка пароля для админки",
                reply_markup=mk.check_password_mk,
                parse_mode="MARKDOWN",
            )

        if redis.get(message.chat.id) == b"True":
            bot.send_message(
                message.chat.id,
                "Admin menu",
                reply_markup=mk.admin_menu_mk,
                parse_mode="MARKDOWN",
            )

    except Exception:
        pass


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    try:
        if redis.get(message.chat.id) is None:
            redis.set(str(message.chat.id), "False")
            bot.send_message(
                message.chat.id,
                "Проверка пароля для админки",
                reply_markup=mk.check_password_mk,
                parse_mode="MARKDOWN",
            )

        if redis.get(message.chat.id) == b"False":
            bot.send_message(
                message.chat.id,
                "Проверка пароля для админки",
                reply_markup=mk.check_password_mk,
                parse_mode="MARKDOWN",
            )

        if redis.get(message.chat.id) == b"True":
            bot.send_message(
                message.chat.id,
                "Admin menu",
                reply_markup=mk.admin_menu_mk,
                parse_mode="MARKDOWN",
            )
    except Exception:
        pass


def check_admin_password(message):
    try:
        if message.text == config["TELEGRAM"]["admin_password"]:
            redis.set(str(message.chat.id), "True")
            bot.send_message(
                message.chat.id,
                "Admin menu",
                reply_markup=mk.admin_menu_mk,
                parse_mode="MARKDOWN",
            )
        else:
            bot.send_message(
                message.chat.id,
                "Пароль неверный, необходима проверка пароля для админки",
                reply_markup=mk.check_password_mk,
                parse_mode="MARKDOWN",
            )

    except Exception:
        pass


@bot.callback_query_handler(func=lambda call: True)
def call_backs(call):
    try:
        if call.data == "check_password":
            msg = bot.send_message(
                call.message.chat.id,
                "Введите пароль",
                reply_markup=mk.hideMenu,
                parse_mode="MARKDOWN",
            )
            bot.register_next_step_handler(msg, check_admin_password)

        if call.data == "quit_admin":
            redis.set(str(call.message.chat.id), "False")
            bot.send_message(
                call.message.chat.id,
                "Проверка пароля для админки",
                reply_markup=mk.check_password_mk,
                parse_mode="MARKDOWN",
            )

        if call.data == "servers_list":
            pass

    except Exception:
        pass


if __name__ == "__main__":
    bot.infinity_polling()
