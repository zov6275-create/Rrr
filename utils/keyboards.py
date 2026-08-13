# utils/keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

inline_button = InlineKeyboardButton('Получить 🆔', callback_data='button1')
inline_button_2 = InlineKeyboardButton('Отзывы🥇', callback_data='button2')
inline_button_3 = InlineKeyboardButton('Оставить отзыв🗣', callback_data='button3')
inline_button_4 = InlineKeyboardButton('Сделок проведено🔄', callback_data='button4')
inline_button_5 = InlineKeyboardButton('Поддержка🧑‍💻', callback_data='button5')
inline_button_6 = InlineKeyboardButton('Да', callback_data='btn6')
inline_button_7 = InlineKeyboardButton('Нет', callback_data='btn7')
inline_button_8 = InlineKeyboardButton('Я оплатил✅', callback_data='btn8')
inline_button_9 = InlineKeyboardButton('Передал', callback_data='btn9')
inline_button_10 = InlineKeyboardButton('Подтвердить сделку', callback_data='btn10')
inline_button_12 = InlineKeyboardButton('Оставить отзыв🗣', callback_data='button12')
inline_button_13 = InlineKeyboardButton('<<Назад', callback_data='button13')
inline_button_14 = InlineKeyboardButton('Да', callback_data='yes')
inline_button_15 = InlineKeyboardButton('Нет', callback_data='no')
inline_button_16 = InlineKeyboardButton('FAQ📃', callback_data='button14')
inline_button_17 = InlineKeyboardButton('О нас👨‍👩‍👦', callback_data='button15')
inline_button_18 = InlineKeyboardButton('Личный кабинет👤', callback_data='button16')
inline_button_19 = InlineKeyboardButton('Я продавец🙋‍♂️', callback_data='button17')
inline_button_20 = InlineKeyboardButton('Я покупатель💁‍♂', callback_data='button18')
inline_button_21 = InlineKeyboardButton('<<Назад', callback_data='button19')
inline_button_22 = InlineKeyboardButton('Отменить', callback_data='cancel')
inline_button_23 = InlineKeyboardButton('Просмотреть историю💾', callback_data='history')
inline_button_24 = InlineKeyboardButton('<<Назад', callback_data='cancel_to_personal_account')

# Добавление инлайе клавиатуры
inline_kb1 = InlineKeyboardMarkup().add(inline_button).add(inline_button_21)
inline_kb2 = InlineKeyboardMarkup().add(inline_button_2, inline_button_3).add(inline_button_4).add(inline_button_5, inline_button_16).add(inline_button_21)
inline_kb3 = InlineKeyboardMarkup().insert(inline_button_6).insert(inline_button_7)
inline_kb4 = InlineKeyboardMarkup().add(inline_button_8)
inline_kb5 = InlineKeyboardMarkup().add(inline_button_9)
inline_kb6 = InlineKeyboardMarkup().add(inline_button_10)
inline_kb8 = InlineKeyboardMarkup().add(inline_button_12)
inline_kb9 = InlineKeyboardMarkup().add(inline_button_13)
yes_or_no = InlineKeyboardMarkup().add(inline_button_14, inline_button_15)
yes_or_no_2 = InlineKeyboardMarkup().add(inline_button_19, inline_button_20).add(inline_button_18).add(inline_button_17)
back_main_menu = InlineKeyboardMarkup().add(inline_button_23).add(inline_button_21)
cancel_button = InlineKeyboardMarkup().add(inline_button_22)
back_to_personal_account = InlineKeyboardMarkup().add(inline_button_24)
# Добавление обычной клавиатуры
keyboard_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['Меню']

keyboard.add(*buttons)
