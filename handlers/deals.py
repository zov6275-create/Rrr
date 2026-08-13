from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import random


# временное хранилище сделок
deals = {}


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

    deals[str(deal_id)] = {
        "description": data["description"],
        "price": message.text,
        "seller": message.from_user.id
    }

    bot = await message.bot.get_me()

    link = f"https://t.me/{bot.username}?start=deal_{deal_id}"

    await message.answer(
        f"✅ Сделка создана!\n\n"
        f"📄 Описание:\n{data['description']}\n\n"
        f"💰 Цена:\n{message.text}\n\n"
        f"🔗 Ссылка покупателю:\n{link}"
    )

    await state.finish()


# открытие сделки по ссылке
async def open_deal(message: types.Message):
    args = message.get_args()

    if args.startswith("deal_"):

        deal_id = args.replace("deal_", "")

        if deal_id in deals:

            deal = deals[deal_id]

            await message.answer(
                f"💼 Сделка\n\n"
                f"📄 Описание:\n{deal['description']}\n\n"
                f"💰 Цена:\n{deal['price']}\n\n"
                f"Продавец: {deal['seller']}"
            )

        else:
            await message.answer(
                "❌ Сделка не найдена"
            )


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

    dp.register_message_handler(
        open_deal,
        commands=["start"]
    )
