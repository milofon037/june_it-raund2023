from aiogram import types
from translation import translations as tr


def kb_menu(lang):
    menu = types.ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder=tr[lang]['CHOOSE'],
                                     resize_keyboard=True)
    menu.add(types.KeyboardButton(tr[lang]['CHECK']))
    menu.add(types.KeyboardButton(tr[lang]['CANCEL']))
    return menu


def kb_check(lang, callback):
    check = types.InlineKeyboardMarkup(row_width=2)
    check.insert(types.InlineKeyboardButton(tr[lang]['YEAH'], callback_data=callback))
    check.insert(types.InlineKeyboardButton(tr[lang]['NO'], callback_data='cancel'))
    return check


language = types.InlineKeyboardMarkup(row_width=2)
language.insert(types.InlineKeyboardButton('Русский🇷🇺', callback_data='l_ru'))
language.insert(types.InlineKeyboardButton('English🇬🇧', callback_data='l_en'))


cancel = types.ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder='13569189600', resize_keyboard=True)
cancel.add(types.KeyboardButton('/cancel'))
