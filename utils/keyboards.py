# utils/keyboards.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


# =====================
# ГЛАВНОЕ МЕНЮ
# =====================

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

history = InlineKeyboardButton(
    "💾 История сделок",
    callback_data="history"
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


# Главное меню

main_keyboard = InlineKeyboardMarkup(row_width=2)

main_keyboard.row(
    create_deal
)

main_keyboard.row(
    my_requisites
)

main_keyboard.row(
    profile,
    settings
)

main_keyboard.row(
    history
)

main_keyboard.row(
    support
)

main_keyboard.row(
    about,
    faq
)


# =====================
# НАЗАД В МЕНЮ
# =====================

back_main_menu = InlineKeyboardMarkup()

back_main_menu.add(
    InlineKeyboardButton(
        "⬅️ Назад",
        callback_data="button19"
    )
)


# =====================
# ПОДДЕРЖКА / НАЗАД
# =====================

inline_kb9 = InlineKeyboardMarkup()

inline_kb9.add(
    InlineKeyboardButton(
        "⬅️ Назад",
        callback_data="button19"
    )
)


# =====================
# НАЗАД В ПРОФИЛЬ
# =====================

back_to_personal_account = InlineKeyboardMarkup()

back_to_personal_account.add(
    InlineKeyboardButton(
        "⬅️ Назад",
        callback_data="cancel_to_personal_account"
    )
)


# =====================
# ОБЫЧНАЯ КНОПКА МЕНЮ
# =====================

keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True
)

keyboard.add(
    "Меню"
)
