from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import random


# временное хранилище сделок
deals = {}


class DealState(StatesGroup):
    description = State()
    price = State()


# кнопка "Создать сделку"
async def create_deal(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "💼 Создание сделки\n\n"
        "Введите описание сделки:"
    )

    await DealState.description.set()


# получение описания
async def get_description(message: types.Message, state: FSMContext):

    await state.update_data(
        description=message.text
    )

    await message.answer(
        "💰 Введите цену сделки:"
    )

    await DealState.price.set()


# получение цены и создание сделки
async def get_price(message: types.Message, state: FSMContext):

    data = await state.get_data()

    deal_id = str(random.randint(10000, 99999))


    # сохраняем сделку
    deals[deal_id] = {
        "description": data["description"],
        "price": message.text,
        "seller": message.from_user.id
    }


    bot_username = (await message.bot.get_me()).username

    link = (
        f"https://t.me/{bot_username}"
        f"?start=deal_{deal_id}"
    )


    await message.answer(
        "✅ Сделка создана!\n\n"
        f"📄 Описание:\n{data['description']}\n\n"
        f"💰 Цена:\n{message.text}\n\n"
        "🔗 Отправьте эту ссылку покупателю:\n"
        f"{link}"
    )


    await state.finish()



# открытие сделки покупателем
async def open_deal(message: types.Message):

    args = message.get_args()


    if not args.startswith("deal_"):
        return


    deal_id = args.replace(
        "deal_",
        ""
    )


    if deal_id in deals:

        deal = deals[deal_id]


        await message.answer(
            "💼 Сделка\n\n"
            f"📄 Описание:\n{deal['description']}\n\n"
            f"💰 Цена:\n{deal['price']}\n\n"
            f"👤 Продавец ID:\n{deal['seller']}"
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
