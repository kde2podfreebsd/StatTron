from telebot import types

hideMenu = types.ReplyKeyboardRemove()


check_password_mk = types.InlineKeyboardMarkup(row_width=1)
check_password = types.InlineKeyboardButton(
    "Check password", callback_data="check_password"
)
check_password_mk.add(check_password)
