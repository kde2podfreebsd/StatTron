import configparser
import os

import telebot

basedir = os.path.abspath(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read(f"{basedir}/../../config.ini")

bot = telebot.TeleBot(config["TELEGRAM"]["adminbotapitoken"])


@bot.message_handler(commands=["start"])
def start(message) -> None:
    try:
        pass
    except Exception:
        pass
