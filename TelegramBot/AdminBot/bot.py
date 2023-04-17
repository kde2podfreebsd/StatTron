import configparser
import os

import markups as mk
import telebot

basedir = os.path.abspath(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read(f"{basedir}/../../config.ini")

bot = telebot.TeleBot(config["TELEGRAM"]["adminbotapitoken"])


@bot.message_handler(commands=["start"])
def start(message) -> None:
    try:
        bot.send_message(
            message.chat.id,
            "Проверка пароля для админки",
            reply_markup=mk.check_password_mk,
            parse_mode="MARKDOWN",
        )
    except Exception:
        pass


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    try:
        pass
    except Exception:
        pass


@bot.callback_query_handler(func=lambda call: True)
def language(call):
    print(call.data)
    try:

        if call.data == "check_password":
            print("введите пароль")
            print(call.data.message.text)

    except Exception:
        pass


if __name__ == "__main__":
    bot.infinity_polling()
