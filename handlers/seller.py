# handlers/seller.py

import os

from utils import keyboards
from utils import sqliter
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold
from loguru import logger
from loader import bot
from aiogram.dispatcher.filters.state import State, StatesGroup

new_sql = sqliter.Sqlite(os.path.abspath(os.path.join('bot_garant.db')))


class WaiteSoldMessage(StatesGroup):
    """
    Режим FSM, создаем состояния
    для принятия ID,
    предметов для продажи и
    и стоимости
    """
    waite_id = State()
    waite_sold_item = State()
    waite_cost = State()


# @dp.callback_query_handler(text='button17')
async def started_seller(callback_query: types.CallbackQuery):
    """
    Режим продавца,
    запрос ID начало сделки
    :param callback_query: types.CallbackQuery
    :return: None
    """
    await callback_query.message.edit_text('Вы перешли в раздел продавца, следуйте дальнейшим указаниями бота:')
    await callback_query.message.edit_reply_markup(reply_markup=keyboards.back_main_menu)
    await callback_query.message.answer('Введите ID покупателя, если его у вас нет, то пускай'
                                        ' покупатель запросит его у бота в разделе "Я покупатель"'
                                        '\nДля отмены сделки нажмите кнопку "Назад"')
    await callback_query.answer()
    await WaiteSoldMessage.waite_id.set()


# @dp.message_handler(state=WaiteSoldMessage.waite_id, content_types=types.ContentTypes.TEXT)
async def waite_sold_items(message: types.Message, state: FSMContext):
    """
    Запрос предметов на продажу,
    проверка на корректность введенного ID
    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    await state.update_data(id=message.text)
    user_data = await state.get_data()

    if user_data['id'].isdigit() and len(user_data["id"]) <= 10:
        if int(message.text) != int(message.from_user.id):
            await message.answer('Введите предметы, которые собираетесь продавать (все в одном сообщении, для отмены сделки нажмите на кнопку ниже):', reply_markup=keyboards.cancel_button)
            await WaiteSoldMessage.waite_sold_item.set()
        else:
            await message.answer('ID введен некорректно, повторите попытку ввода(заметьте ID не должен содержать букв и превышать 10 символов)')
    else:
        await message.answer('Вы не можете проводить сделку сами с собой!')


# @dp.message_handler(state=WaiteSoldMessage.waite_sold_item, content_types=types.ContentTypes.TEXT)  # Запрос цены
async def waite_cost(message: types.Message, state: FSMContext):
    """
    Запрашиваем цену у покупателя,
    попутно все данные сохраняем в словарь
    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    await state.update_data(item=message.text)
    await message.answer('Введите сумму за которую вы продаете данные предметы'
                         '(для отмены сделки нажмите на кнопку ниже): ', reply_markup=keyboards.cancel_button)
    await WaiteSoldMessage.waite_cost.set()


# @dp.message_handler(state=WaiteSoldMessage.waite_cost, content_types=types.ContentTypes.TEXT)
async def send_all_info_about_offer(message: types.Message, state: FSMContext):
    """
    Отправка сведений покупателю,
    добавление ID суммы сделки,
    формирование и обновление данных
    у пользователей в личном кабинете
    :param message: types.Message
    :param state: FSMContext
    :return None
    """
    person_id = message.from_user.id
    try:

        if message.text.isdigit():
            user_data = await state.get_data()
            history = (f'{hbold("Сведения сделки:")}\n'
                       f'1️⃣ID покупателя:{user_data["id"]}\n'
                       f'2️⃣Предметы для продажи:{user_data["item"]}\n'
                       f'3️⃣Цена за все:{message.text}')
            await message.answer(history, reply_markup=keyboards.keyboard)
            await bot.send_message(user_data["id"], history + f'\n{hbold("Данные корректны?")}', reply_markup=keyboards.inline_kb3)
            logger.info(f'{message.from_user.username} предложил сделку: {user_data["id"]}, цена: {message.text}, Предметы для продажи: {user_data["item"]}')
            new_sql.add_second_id(person_id, user_data["id"])
            new_sql.add_money(person_id, user_data["id"], message.text)
            counter_1 = new_sql.get_all_information(person_id)
            counter_2 = new_sql.get_all_information(user_data["id"])
            first = int(counter_1[1]) + 1
            second = int(counter_2[1]) + 1
            first_pay = int(counter_1[2]) + int(message.text)
            second_sold = int(counter_2[0]) + int(message.text)
            logger.info(f"{first_pay}--{second_sold} сохранено в личный кабинет!")
            new_sql.add_pay(str(second_sold), user_data["id"])
            new_sql.add_sold(str(first_pay), person_id)
            new_sql.add_count(str(first), person_id)
            new_sql.add_count(str(second), user_data["id"])
            new_sql.add_history(history, person_id)
            new_sql.add_history(history, user_data["id"])
            await state.finish()
        else:
            await message.answer('Введите сумму цифрами!')

    except Exception as exc:
        logger.error(f'Ошибка: {exc}')
        await message.answer('Данные о ID указаны некорректно, проверьте правильность написания!'
                             ' Или попросите покупателя отправить ID повторно.')
        await state.finish()


# @dp.callback_query_handler(text='btn7')
async def callback_no(callback_query: types.CallbackQuery):
    """
    Дополнительная проверка,
    покупатель подтверждает,
    что все данные по настояще корректны
    :param callback_query: types.CallbackQuery
    :return: None
    """
    await callback_query.message.edit_reply_markup()
    first_id = callback_query.from_user.id
    await bot.send_message(new_sql.take_second_id(first_id), 'Покупатель отклонил сделку. Причина: Данные сделки некорректны!'
                                                             '\nОбсудите со второй стороной подробнее сведения сделки.')


# @dp.callback_query_handler(text='btn6')  # Переход к подтверждению оплаты
async def user_pay(callback_query: types.CallbackQuery):
    """
    Покупатель подтвердил корректность данных сделки.
    Оплата происходит вне бота (любым удобным способом,
    о котором стороны договариваются самостоятельно),
    бот лишь фиксирует факт оплаты по нажатию кнопки.
    :param callback_query: types.CallbackQuery
    :return: None
    """
    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer('Финальная часть сделки. Переведите оплату продавцу удобным вам способом '
                                        '(договоритесь со второй стороной лично), а затем нажмите кнопку ниже:',
                                        reply_markup=keyboards.inline_kb4)
    await callback_query.answer()


# @dp.callback_query_handler(text='btn8')  # Покупатель подтверждает, что перевёл оплату
async def user_confirm_pay(callback_query: types.CallbackQuery):
    """
    Покупатель вручную подтверждает,
    что перевёл оплату продавцу.
    Бот не проводит и не проверяет
    реальный денежный перевод.
    :param callback_query: types.CallbackQuery
    :return: None
    """
    await callback_query.message.edit_reply_markup()
    person_id = callback_query.from_user.id
    await callback_query.message.answer('Оплата отмечена как выполненная!✅', reply_markup=keyboards.keyboard)
    await bot.send_message(new_sql.take_second_id(person_id), 'Покупатель подтвердил оплату сделки, выполните свою часть сделки!'
                                                              ' После выполнения подтвердите ниже:', reply_markup=keyboards.inline_kb5)
    logger.info('Покупатель подтвердил оплату сделки!')


# @dp.callback_query_handler(text='btn9')  # Проверка офера покупателем, после чего подтверждение сделки
async def check_offer(callback_query: types.CallbackQuery):
    """
    Проверка офера покупателем,
    переход к следующему шагу
    :param callback_query: types.CallbackQuery
    :return: None
    """
    await callback_query.message.edit_reply_markup()
    person_id = callback_query.from_user.id
    await bot.send_message(new_sql.take_second_id(person_id), 'Продавец выполнил свою часть сделки,'
                                                              ' как можно тщательнее все проверьте и подтвердите сделку',
                           reply_markup=keyboards.inline_kb6)


# @dp.callback_query_handler(text='btn10')  # Подтверждение успешного завершения сделки
async def get_money(callback_query: types.CallbackQuery):
    """
    Последний шаг: покупатель подтвердил получение товара,
    сделка считается завершённой. Расчёт между сторонами
    происходит вне бота, реальные переводы бот не выполняет.
    :param callback_query: types.CallbackQuery
    :return: None
    """
    person_is = callback_query.from_user.id
    await callback_query.message.edit_reply_markup()
    await bot.send_message(new_sql.take_second_id(person_is), 'Сделка прошла успешно! Покупатель подтвердил получение товара.',
                           reply_markup=keyboards.keyboard)
    await callback_query.message.answer('Сделка завершена!✅', reply_markup=keyboards.keyboard)
    logger.info('Сделка завершена, товар получен покупателем')


async def cancel_button(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Отмена сделки, через
    инлайн клавиатуру
    :param  callback_query: types.CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await state.finish()
    await callback_query.message.answer('Сделка отменена...')
    await callback_query.message.edit_reply_markup()


def register_seller_handlers(dispatcher: Dispatcher):
    """
    Регистрация хэндлеров
    :param dispatcher: Dispatcher
    :return: None
    """
    dispatcher.register_callback_query_handler(started_seller, text='button17')
    dispatcher.register_message_handler(waite_sold_items, state=WaiteSoldMessage.waite_id, content_types=types.ContentTypes.TEXT)
    dispatcher.register_message_handler(waite_cost, state=WaiteSoldMessage.waite_sold_item, content_types=types.ContentTypes.TEXT)
    dispatcher.register_message_handler(send_all_info_about_offer, state=WaiteSoldMessage.waite_cost, content_types=types.ContentTypes.TEXT)
    dispatcher.register_callback_query_handler(user_pay, text='btn6')
    dispatcher.register_callback_query_handler(user_confirm_pay, text='btn8')
    dispatcher.register_callback_query_handler(callback_no, text='btn7')
    dispatcher.register_callback_query_handler(check_offer, text='btn9')
    dispatcher.register_callback_query_handler(get_money, text='btn10')
    dispatcher.register_callback_query_handler(cancel_button, text='cancel', state='*')
