from telebot import types

hideMenu = types.ReplyKeyboardRemove()


check_password_mk = types.InlineKeyboardMarkup(row_width=1)
check_password = types.InlineKeyboardButton(
    "Check password", callback_data="check_password"
)
check_password_mk.add(check_password)


admin_menu_mk = types.InlineKeyboardMarkup(row_width=1)
servers_list = types.InlineKeyboardButton("Server list", callback_data="servers_list")
quit_admin = types.InlineKeyboardButton("Quit admin", callback_data="quit_admin")
admin_menu_mk.add(check_password, quit_admin)
