
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from create_bot import bot, db
from aiogram.enums.chat_type import ChatType
from aiogram.filters import Command
from aiogram.filters import CommandStart

main_router = Router()


# обработчик комнады старт
@main_router.message(CommandStart())
async def start_command(message: types.Message):
    # weather = types.InlineKeyboardButton(text="💫Погода💫", callback_data="pogoda")
    builder = InlineKeyboardBuilder()
    # проверяем если активный чат отсутствует тогда даем доступ к кнопкам поиска
    if db.check_user_in_queue(message.chat.id) is False and db.check_active_chat(message.chat.id) is False:
        anon_chat1 = types.InlineKeyboardButton(text="Анонимный чат👁🌐", callback_data="anon_chat")
        builder.add(anon_chat1)
        await message.answer("Привет! 🖖", reply_markup=builder.as_markup())
    else:
        await message.answer(text='Привет!')


# обработчик команды стоп, нужен чтобы остановить активный чат
@main_router.message(Command('stop'))
async def stop_chat_command(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    # проверяем чат на активность если он еще активен то прощаемся и останавливаем его удалив из базы данных
    if db.check_active_chat(message.chat.id):
        await bot.send_message(act_chat[2], 'Ваш собеседник покинул чат😔')
        await bot.send_message(act_chat[2], 'Чат завершен📴')
        await bot.send_message(act_chat[1], 'Вы покинули чат😔')
        await bot.send_message(act_chat[1], 'Чат завершен📴')
        db.stop_chat(message.chat.id)
    else:
        await bot.send_message(message.chat.id, '⛔У вас нет активного чата⛔️')


# дальше идут обработчики различных типов сообщения для общения в активном чате


# конфликт проверки чек чат в обработчиках и остальных функциях
@main_router.message(F.photo)
async def handle_photo_message(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_photo(act_chat[2], photo=message.photo[-1].file_id)


@main_router.message(F.audio)
async def handle_audio_message(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_audio(act_chat[2], message.audio.file_id)


@main_router.message(F.video)
async def handle_video_message(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_video(act_chat[2], message.video.file_id)


@main_router.message(F.video_note)
async def handle_video_circe_message(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_video_note(act_chat[2], message.video_note.file_id)


@main_router.message(F.sticker)
async def handle_stikers_message(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_sticker(act_chat[2], message.sticker.file_id)


@main_router.message(F.voice)
async def handle_voice_message(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_voice(act_chat[2], message.voice.file_id)


@main_router.message(F.text)
async def anon_chat(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_message(act_chat[2], message.text)


async def anon_chat_but(callback_query):
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)

    keyboard = InlineKeyboardBuilder()

    looking = types.InlineKeyboardButton(text="Найти собеседника🔮", callback_data="gender selection")
    return_but = types.InlineKeyboardButton(text="вернуться↩", callback_data="return")

    keyboard.add(looking, return_but)

    await bot.send_message(callback_query.from_user.id, "Анонимный чат👁🌐", reply_markup=keyboard.as_markup())


async def queue_with_reg(callback_query):
    if db.get_sex(callback_query.message.chat.id) is False:
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)

        keyboard = InlineKeyboardBuilder()

        boy = types.InlineKeyboardButton(text="парень🙎", callback_data="reg_guy")
        girl = types.InlineKeyboardButton(text="девушка🙎‍♀", callback_data="reg_girl")

        keyboard.add(boy, girl)
        await bot.send_message(callback_query.from_user.id, "Пройдите регистрацию. Укажите ваш пол:",
                               reply_markup=keyboard.as_markup())

    else:
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)

        keyboard = InlineKeyboardBuilder()

        boy = types.InlineKeyboardButton(text="парень🙎", callback_data="sex_guy")
        girl = types.InlineKeyboardButton(text="девушка🙎‍♀️", callback_data="sex_girl")
        any_sex = types.InlineKeyboardButton(text="любой🚻", callback_data="sex_any")
        return_but = types.InlineKeyboardButton(text="вернуться↩", callback_data="return")

        keyboard.add(boy, girl, any_sex, return_but)
        await bot.send_message(callback_query.from_user.id, "Пол собеседника:", reply_markup=keyboard.as_markup())

    # конец обработчиков сообщений для чата


async def waiting(callback_query, chat_id, sex):
    db.add_queue(chat_id, sex)
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)

    keyboard = InlineKeyboardBuilder()
    stop_queue = types.InlineKeyboardButton(text="❌Остановить поиск❌", callback_data="stop_queue")
    keyboard.add(stop_queue)
    await bot.send_message(callback_query.from_user.id, "Поиск начался🔮", reply_markup=keyboard.as_markup())
    sticker = await bot.send_sticker(callback_query.message.chat.id,
                                     sticker='CAACAgIAAxkBAAILWWSpysWYaY5CTv2Pbv4hd3tGePU6AAJeXAEAAWOLRgz16gRfGZceQS8E')
    sticker_1 = sticker.message_id
    db.save_sticker_id(sticker_1, chat_id)


async def queue(callback_query, sex):
    chat_id = callback_query.message.chat.id

    if db.check_user_in_queue(chat_id) is False and db.check_active_chat(chat_id) is False:
        user0 = db.check_sex(chat_id, sex)
        if user0:
            user0_sticker = db.get_sticker_id(user0)
            db.create_chat(user0, chat_id)
            act_chat = db.get_active_chat(chat_id)
            try:
                await bot.delete_message(chat_id=user0,
                                         message_id=user0_sticker)
            except Exception as ex:
                print(ex)
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)

            await bot.send_message(act_chat[1], "Добро пожаловать в чат🤝")
            await bot.send_message(act_chat[2], "Добро пожаловать в чат🤝")
        else:
            await waiting(callback_query, chat_id, sex)
    else:
        await bot.send_message(callback_query.from_user.id, "хватит дудосить")


async def return_func(callback_query):
    chat_id = callback_query.message.chat.id
    await bot.delete_message(chat_id=callback_query.message.chat.id,
                             message_id=callback_query.message.message_id)
    keyboard = InlineKeyboardBuilder()
    weather = types.InlineKeyboardButton(text="💫Погода💫", callback_data="pogoda")
    # проверка чата на активность
    if db.check_user_in_queue(chat_id) is False and db.check_active_chat(chat_id) is False:
        anon_chat1 = types.InlineKeyboardButton(text="Анонимный чат👁🌐", callback_data="anon_chat")
        keyboard.add(weather, anon_chat1)
    else:
        keyboard.add(weather)
    await bot.send_message(callback_query.from_user.id, "Привет! 🖖", reply_markup=keyboard.as_markup())


# Обработчик нажатий на кнопки
@main_router.callback_query()
async def process_callback_button(callback_query: types.CallbackQuery):
    chat_type = callback_query.message.chat.type
    # проверяем что бот находит в личном чате с пользователем а не в группе
    if chat_type == ChatType.PRIVATE:
        # Получение данных из нажатой кнопки
        button_data = callback_query.data
        chat_id = callback_query.message.chat.id
        if button_data == 'return':
            await return_func(callback_query)
        #
        # if button_data == "pogoda":
        #     await show_pogoda(callback_query)
        #
        # elif button_data == "pogoda_moscow":
        #     url = 'https://world-weather.ru/pogoda/russia/moscow/'
        #     await bot.send_message(callback_query.from_user.id, get_weather(url) + " в Москве на данный момент")
        # elif button_data == "pogoda_sp":
        #     url = 'https://world-weather.ru/pogoda/russia/saint_petersburg/'
        #     await bot.send_message(callback_query.from_user.id, get_weather(url) + " в Питере на данный момент")
        # elif button_data == "pogoda_sev":
        #     url = 'https://world-weather.ru/pogoda/russia/sevastopol/'
        #     await bot.send_message(callback_query.from_user.id, get_weather(url) + " в Севастополе на данный момент")

        if button_data == 'anon_chat':
            await anon_chat_but(callback_query)

        if button_data == 'gender selection':
            await queue_with_reg(callback_query)

        if button_data == 'reg_guy':
            await bot.send_message(callback_query.from_user.id, "✅Успешная регистрация!✅")
            await anon_chat_but(callback_query)
            db.add_sex(chat_id, 'guy')

        if button_data == 'reg_girl':
            await bot.send_message(callback_query.from_user.id, "✅Успешная регистрация!✅")
            await anon_chat_but(callback_query)
            db.add_sex(chat_id, 'girl')

        if button_data == 'sex_guy':
            await queue(callback_query, 'guy')

        if button_data == 'sex_girl':
            await queue(callback_query, 'girl')

        if button_data == 'sex_any':
            await queue(callback_query, 'any')

        if button_data == 'stop_queue':
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=db.get_sticker_id(chat_id))
            chat_id = callback_query.message.chat.id
            db.stop_queue(chat_id)
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
            keyboard = InlineKeyboardBuilder()
            return_but = types.InlineKeyboardButton(text="вернуться↩️", callback_data="return")
            keyboard.add(return_but)
            await bot.send_message(callback_query.from_user.id, "❌поиск остановлен❌", reply_markup=keyboard.as_markup())



