import os

from utils import keyboards
from aiogram import types, Dispatcher
from utils import sqliter
from aiogram.utils.markdown import hbold
from loguru import logger
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

new_sql = sqliter.Sqlite(os.path.abspath(os.path.join('bot_garant.db')))


# @dp.message_handler(commands=['start'])  # Старт - запуск бота, тут происходит добавление в БД + появляется клавиатура
async def main_menu(message: types.Message):
    """
    Команда старт,
    активация бота,
    запись пользователя в БД
    :param message: types.Message
    :return: None
    """
    person_id = message.from_user.id
    new_sql.user_in_bd(person_id)
    await message.answer_photo(
    photo="AgACAgIAAxkBAAMVan1a9SKJZMelmdXkVu1947ZQ_DMAAhkXaxv5--lLBxhEUzSSTAoBAAMCAAN4AAM9BA",
    caption=
    f'👋 {hbold("Добро пожаловать!")}\n\n'
    f'💼 {hbold("Надёжный сервис для безопасных сделок!")}\n'
    f'✨ Автоматизировано, быстро и без лишних хлопот!\n\n'
    f'🔹 Комиссия за услугу: {hbold("7%")}\n'
    f'🔹 Поддержка 24/7: @твой_юзернейм\n\n'
    f'💌 Теперь ваши сделки под защитой! 🛡️',
    reply_markup=keyboards.keyboard
    )

    await message.answer('Главное меню⤵️                  ', reply_markup=keyboards.main_keyboard)


# @dp.message_handler(lambda message: message.text == 'Меню')
async def main_menu_message_reply(message: types.Message):
    """
    Активация главного меню,
    через "Меню"
    :param message: types.Message
    :return: None
    """
    await message.answer('Главное меню⤵️                  ', reply_markup=keyboards.main_keyboard)


# @dp.callback_query_handler(text='button19', state='*')
async def back_to_main_menu(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Переход в главное меню
    через кнопку назад
    :param callback_query: types.CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await callback_query.message.edit_text('Главное меню⤵️                  ')
    await callback_query.message.edit_reply_markup(reply_markup=keyboards.main_keyboard)
    await state.finish()


# @dp.callback_query_handler(text='button16')
async def personal_account(callback_query: types.CallbackQuery):
    """
    Переход пользователем
    в личный кабинет,
    достаем данные из Бд
    :param callback_query: types.CallbackQuery
    :return: None
    """
    check = callback_query.from_user.id
    information = new_sql.get_all_information(check)
    await callback_query.message.edit_text(f'{hbold("🙋Добро пожаловать в личный кабинет!")}\n'
                                           f'Твой 🆔: {callback_query.from_user.id}\n\n'
                                           f'♾{hbold("Совершено сделок")}: {information[1]}\n'
                                           f'🤑{hbold("Продано на")}: {information[2]} RUB\n'
                                           f'💰{hbold("Куплено на")}: {information[0]} RUB')
    await callback_query.message.edit_reply_markup(reply_markup=keyboards.back_main_menu)


class WaiteMes(StatesGroup):
    """
    Прием сообщения пользователем,
    которое он отправил в тех. поддержку
    """
    waite_person_mes = State()


# @dp.callback_query_handler(text='button5')
async def helper_fo_users(callback_query: types.CallbackQuery):
    """
    Прием сообщения пользователем,
    которое он отправил в тех. поддержку
    :param callback_query: types.CallbackQuery
    :return: None
    """
    await callback_query.message.edit_text('Подробно опишите вашу проблему '
                                           'и отправьте ее одним сообщением боту.')
    await callback_query.message.edit_reply_markup(reply_markup=keyboards.inline_kb9)
    await WaiteMes.waite_person_mes.set()  # Принимаем сообщение


# @dp.message_handler(state=WaiteMes.waite_person_mes, content_types=types.ContentTypes.TEXT)
async def waite_message(message: types.Message, state: FSMContext):
    """
    Обрабатываем сообщение,
    добавляем его в нашу БД
    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    person_id = message.from_user.id
    async with state.proxy() as user_data:
        user_data['input_user'] = message.text.replace('\n', ' ')
    answer = user_data['input_user']
    await message.answer('Ваше сообщение на рассмотрении! Ждите ответа🕔')
    logger.info(f"Пользователь: {person_id} написал в тех поддержку |{message.text}|")
    new_sql.add_question(person_id, answer)
    await state.finish()


# @dp.callback_query_handler(text='button15')
async def about_us(callback_query: types.CallbackQuery):
    """
    Преходим в раздел о нас
    :param callback_query: types.CallbackQuery
    :return: None
    """
    await callback_query.message.edit_text(f'{hbold("О нас:")}\n\n'
                                           f'🔒 BOT GARANT защищает интересы сторон при сделках.'
                                           f'Исключить мошеннические действия и проконтролировать исполнение обязательств.\n\n'
                                           f'🛡BOT GARANT является промежуточным звеном при любых сделках и договорах, чтобы стороны соблюдали их условия.\n\n'
                                           f'Если есть дополнительные вопросы, вы можете обратиться в поддержку.\n'
                                           f'Приятного пользования!')

    await callback_query.message.edit_reply_markup(reply_markup=keyboards.inline_kb2)


class Feedback(StatesGroup):
    """
    Создаем состояния
    для принятия отзывов пользователей
    """
    waite_feedback = State()
    waite_callback_answer = State()
    waite_photo = State()
    waite_stars = State()


# @dp.callback_query_handler(text='button3')
async def add_rev(callback_query: types.CallbackQuery):
    """
    Принимаем отзыв от пользователя
    :param callback_query: types.CallbackQuery
    :return: None
    """
    await callback_query.message.edit_text('Напишите ваш отзыв и отправьте его одним сообщением боту =)')
    await callback_query.message.edit_reply_markup(reply_markup=keyboards.inline_kb9)
    await Feedback.waite_feedback.set()


# @dp.message_handler(state=Feedback.waite_feedback, content_types=types.ContentTypes.TEXT)
async def feed_back_2(message: types.Message, state: FSMContext):
    """
    Принимаем оценку по 5-ти
    балльной шкале
    :param  message: types.Message
    :param state: FSMContext
    :return: None
    """
    await state.update_data(feedback=message.text)
    await message.answer('Оцените работу бота по 5-ти балльной шкале\n'
                         'отправьте боту цифру от 1 до 5')
    await Feedback.waite_stars.set()


# @dp.message_handler(state=Feedback.waite_stars)
async def waite_stars(message: types.Message, state: FSMContext):
    """
    Проверка оценки на корректность
    добавление отзыва в БД
    :param message: types.Message
    :param state: FSMContext
    :return: None
    """
    person_id = message.from_user.id
    if message.text.isdigit():
        if 0 < int(message.text) <= 5:
            await state.update_data(stars=message.text)
            user_data = await state.get_data()
            await message.answer('Спасибо за ваш отзыв!😊')
            logger.info(f"Пользователь: {person_id} оставил отзыв |{user_data['feedback']}|{user_data['stars']}/5|")
            new_sql.add_feed_back(
                f'{hbold(user_data["feedback"])}\n\nОценка: {user_data["stars"]}/5\nОставил отзыв: @{message.from_user.username}',
                person_id)
            await state.finish()
        else:
            await message.answer('Введите оценку от 1-5')
    else:
        await message.answer('Введите оценку цифрами, а не буквами')


# @dp.callback_query_handler(text='button2')  # Вывод отзывов из БД
async def send_rev(callback_query: types.CallbackQuery):
    """
    Вывод всех отзывов из БД
    :param callback_query: types.CallbackQuery
    :return: None
    """
    try:
        # await callback_query.message.edit_text('Наши отзывы:')
        await callback_query.message.edit_reply_markup(reply_markup=keyboards.inline_kb9)
        check = new_sql.get_feed_back()
        rev_list = ''
        for i_feed in check:
            if str(*i_feed) != '' and str(*i_feed) != "None":
                for i_elem in i_feed:
                    rev_list += "\n\n" + i_elem
        await callback_query.message.edit_text(rev_list, reply_markup=keyboards.inline_kb9)
    except Exception as exc:
        await callback_query.message.answer("Ой, возникла какая-то ошибка, мы скоро ее починим!")
        logger.error(f'Ошибка: {exc}')


# @dp.callback_query_handler(text='button13')
async def back_button(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Кнопка назад, которая
    возвращает в раздел о нас
    :param callback_query: types.CallbackQuery
    :param state: FSMContext
    :return: None
    """
    await callback_query.message.edit_text(f'{hbold("О нас:")}\n\n'
                                           f'🔒 BOT GARANT защищает интересы сторон при сделках.'
                                           f'Исключить мошеннические действия и проконтролировать исполнение обязательств.\n\n'
                                           f'🛡BOT GARANT является промежуточным звеном при любых сделках и договорах, чтобы стороны соблюдали их условия.\n\n'
                                           f'Если есть дополнительные вопросы, вы можете обратиться в поддержку.\n'
                                           f'Приятного пользования!')
    await callback_query.message.edit_reply_markup(reply_markup=keyboards.inline_kb2)
    await state.finish()


# @dp.callback_query_handler(text='button14')
async def faq(callback_query: types.CallbackQuery):
    """
    Переходим в раздел с FAQ
    :param callback_query: types.CallbackQuery
    :return: None
    """
    await callback_query.message.edit_text(f'{hbold("Политика конфиденциальности:")}\n\n'
                                           f'{hbold("1.1:")} Пользователь дает согласие на обработку и хранение его данных, согласно правилам Телеграм\n\n'
                                           f'{hbold("1.2:")} Администрация @GarantForYoubot не несет ответственность за случайную утечку каких-либо данных'
                                           f'(ставим в известие, что администрация не сохраняет личных данных пользователей, как например номер, а использует только'
                                           f'данные предоставленные самим телеграмом)\n\n'
                                           f'{hbold("2.1:")} Администрация не несет ответственность за товар, предоставленный продавцом и не возвращает за него деньги\n\n'
                                           f'{hbold("2.2:")} Администрация не возвращает деньги за опечатки пользователей, прежде чем что-то отправить перепроверяйте и следуйте инструкции\n\n'
                                           f'{hbold("2.3:")} Администрация в праве вернуть выплату, если утеря средств была произведена из-за технических сбоев бота\n\n'
                                           f'{hbold("2.4:")} Администрация не несет ответственность за незаконченную сделку или сделку, которая проведена вне сервиса\n\n'
                                           f'{hbold("3:")} Если Пользователь решил покинуть Сайт и перейти к сайтам третьих лиц или использовать, или установить программы'
                                           f'третьих лиц, он делает это на свой риск и с этого момента настоящие Правила более не распространяются на Пользователя. При дальнейших'
                                           f'действиях Пользователю стоит руководствоваться применимыми нормами и политикой, в том числе деловыми обычаями тех лиц, чей Контент он собирается использовать.\n\n'
                                           f'{hbold("4.1:")} Размещение сторонней рекламы со стороны пользователей в разделе "оставить отзыв" не одобряется администрацией, а пользователь в таком случае может получить временную блокировку\n\n'
                                           f'{hbold("4.2:")} Спам сообщениями не касающихся темы в раздел "поддержка" не одобряется администрацией и карается временной блокировкой\n\n'
                                           f'{hbold("5:")}  Все объекты, размещенные на Сайте, в том числе элементы дизайна, текст, графические изображения, иллюстрации, видео, скрипты, программы, музыка, звуки и другие объекты и их подборки (далее — Контент),'
                                           f' являются объектами исключительных прав Администрации, Пользователей сервиса и других правообладателей, все права на эти объекты защищены.\n\n'
                                           f'{hbold("6:")} Незнание правил не освобождает от ответственности')

    await callback_query.message.edit_reply_markup(reply_markup=keyboards.inline_kb9)


async def history_menu(callback_query: types.CallbackQuery):
    """
    Просмотр истории пользователем
    :param callback_query: types.CallbackQuery
    :return: None
    """
    user_id = callback_query.from_user.id
    history = new_sql.get_users_history(user_id)
    await callback_query.message.edit_text(history, reply_markup=keyboards.back_to_personal_account)


async def back_to_personal(callback_query: types.CallbackQuery):
    """
    Кнопка назад,
    возращение пользователя
    в его личный кабинет
    :param callback_query: types.CallbackQuery
    :return: None
    """
    user_id = callback_query.from_user.id
    information = new_sql.get_all_information(user_id)
    await callback_query.message.edit_text(f'{hbold("🙋Добро пожаловать в личный кабинет!")}\n'
                                           f'Твой 🆔: {callback_query.from_user.id}\n\n'
                                           f'♾{hbold("Совершено сделок")}: {information[1]}\n'
                                           f'🤑{hbold("Продано на")}: {information[2]} RUB\n'
                                           f'💰{hbold("Куплено на")}: {information[0]} RUB')
    await callback_query.message.edit_reply_markup(reply_markup=keyboards.back_main_menu)


def register_main_menu(dispatcher: Dispatcher):
    """
    Регистрация хэндлеров
    :param dispatcher: Dispatcher
    :return: None
    """
    dispatcher.register_message_handler(
    main_menu,
    commands=['start'],
    state='*'
    )
    dispatcher.register_message_handler(main_menu_message_reply, lambda message: message.text == 'Меню')
    dispatcher.register_callback_query_handler(back_to_main_menu, text='button19', state='*')
    dispatcher.register_callback_query_handler(personal_account, text='button16')
    dispatcher.register_callback_query_handler(helper_fo_users, text='button5')
    dispatcher.register_message_handler(waite_message, state=WaiteMes.waite_person_mes,
                                        content_types=types.ContentTypes.TEXT)
    dispatcher.register_callback_query_handler(about_us, text='button15')
    dispatcher.register_callback_query_handler(add_rev, text='button3')
    dispatcher.register_message_handler(feed_back_2, state=Feedback.waite_feedback,
                                        content_types=types.ContentTypes.TEXT)
    dispatcher.register_message_handler(waite_stars, state=Feedback.waite_stars)
    dispatcher.register_callback_query_handler(send_rev, text='button2')
    dispatcher.register_callback_query_handler(back_button, text='button13', state='*')
    dispatcher.register_callback_query_handler(faq, text='button14')
    dispatcher.register_callback_query_handler(history_menu, text="history")
    dispatcher.register_callback_query_handler(back_to_personal, text="cancel_to_personal_account")
