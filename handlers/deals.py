from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import random


class DealState(StatesGroup):
    description = State()
    price = State()


async def create_deal(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "💼 Создание сделки\n\n"
        "Введите описание сделки:"
    )
    await DealState.description.set()


async def get_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)

    await message.answer(
        "Введите цену сделки:"
    )

    await DealState.price.set()


async def get_price(message: types.Message, state: FSMContext):
    data = await state.get_data()

    deal_id = random.randint(10000, 99999)

    link = f"https://t.me/{(await message.bot.get_me()).username}?start=deal_{deal_id}"

    await message.answer(
        f"✅ Сделка создана!\n\n"
        f"📄 Описание:\n{data['description']}\n\n"
        f"💰 Цена:\n{message.text}\n\n"
        f"🔗 Ссылка для покупателя:\n{link}"
    )

    await state.finish()


def register_deals(dp: Dispatcher):
    dp.register_callback_query_handler(
        create_deal,
        text="create_deal"
    )

    dp.register_message_handler(
        get_description,
        state=DealState.description
    )

    dp.register_message_handler(
        get_price,
        state=DealState.price
    )
