# utils/keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


# Главное меню

create_deal = InlineKeyboardButton(
    "💼 Создать сделку",
    callback_data="create_deal"
)

my_requisites = InlineKeyboardButton(
    "💳 Мои реквизиты",
    callback_data="my_requisites"
)

profile = InlineKeyboardButton(
    "👤 Мой профиль",
    callback_data="button16"
)

settings = InlineKeyboardButton(
    "⚙️ Настройки",
    callback_data="settings"
)

support = InlineKeyboardButton(
    "☎️ Поддержка",
    callback_data="button5"
)

about = InlineKeyboardButton(
    "👥 О нас",
    callback_data="button15"
)

faq = InlineKeyboardButton(
    "📃 FAQ",
    callback_data="button14"
)

history = InlineKeyboardButton(
    "💾 История сделок",
    callback_data="history"
)


# Клавиатура как в примере FunPay

main_keyboard = InlineKeyboardMarkup(row_width=2)

main_keyboard.add(create_deal)
main_keyboard.add(my_requisites)
main_keyboard.row(profile, settings)
main_keyboard.add(history)
main_keyboard.add(support)
main_keyboard.add(about, faq)



# Назад

back_main_menu = InlineKeyboardMarkup()

back_main_menu.add(
    InlineKeyboardButton(
        "⬅️ Назад",
        callback_data="button19"
    )
)


# Поддержка

inline_kb9 = InlineKeyboardMarkup()

inline_kb9.add(
    InlineKeyboardButton(
        "⬅️ Назад",
        callback_data="button19"
    )
)


# Личный кабинет

back_to_personal_account = InlineKeyboardMarkup()

back_to_personal_account.add(
    InlineKeyboardButton(
        "⬅️ Назад",
        callback_data="cancel_to_personal_account"
    )
)



# Обычная кнопка Меню

keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True
)

keyboard.add(
    "Меню"
)
