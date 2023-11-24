from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router
from create_bot import bot, db
from aiogram.enums.chat_type import ChatType
from aiogram.filters import Command
from aiogram.filters import CommandStart

main_router = Router()


@main_router.message(CommandStart())
async def start_command(message: types.Message):
    """
    Обработчик команды /start.

    Args:
        message (types.Message): Объект сообщения.

    Returns:
        None
    """
    builder = InlineKeyboardBuilder()
    if db.check_user_in_queue(message.chat.id) is False and db.check_active_chat(message.chat.id) is False:
        anon_chat1 = types.InlineKeyboardButton(text="Анонимный чат👁🌐", callback_data="anon_chat")
        builder.add(anon_chat1)
        await message.answer("Привет! 🖖", reply_markup=builder.as_markup())
    else:
        await message.answer(text='Привет!')


@main_router.message(Command('stop'))
async def stop_chat_command(message: types.Message):
    """
    Обработчик команды /stop.

    Args:
        message (types.Message): Объект сообщения.

    Returns:
        None
    """
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_message(act_chat[2], 'Ваш собеседник покинул чат😔')
        await bot.send_message(act_chat[2], 'Чат завершен📴')
        await bot.send_message(act_chat[1], 'Вы покинули чат😔')
        await bot.send_message(act_chat[1], 'Чат завершен📴')
        db.stop_chat(message.chat.id)
    else:
        await bot.send_message(message.chat.id, '⛔У вас нет активного чата⛔️')


# ==================================================================================

async def anon_chat_but(callback_query: types.CallbackQuery):
    """
    Обработчик кнопки "Анонимный чат👁🌐".

    Args:
        callback_query (types.CallbackQuery): Объект callback_query.

    Returns:
        None
    """
    msg = callback_query.message
    await msg.delete()

    keyboard = InlineKeyboardBuilder()
    looking = types.InlineKeyboardButton(text="Найти собеседника🔮", callback_data="gender selection")
    return_but = types.InlineKeyboardButton(text="вернуться↩", callback_data="return")

    keyboard.add(looking, return_but)

    await bot.send_message(callback_query.from_user.id, "Анонимный чат👁🌐", reply_markup=keyboard.as_markup())


async def queue_with_reg(callback_query: types.CallbackQuery):
    """
    Обработчик кнопки "gender selection" для запуска процесса регистрации.

    Args:
        callback_query (types.CallbackQuery): Объект callback_query.

    Returns:
        None
    """
    msg = callback_query.message
    if db.get_sex(callback_query.message.chat.id) is False:
        await msg.delete()

        keyboard = InlineKeyboardBuilder()

        boy = types.InlineKeyboardButton(text="парень🙎", callback_data="reg_guy")
        girl = types.InlineKeyboardButton(text="девушка🙎‍♀", callback_data="reg_girl")

        keyboard.add(boy, girl)
        await bot.send_message(callback_query.from_user.id, "Пройдите регистрацию. Укажите ваш пол:",
                               reply_markup=keyboard.as_markup())

    else:
        await msg.delete()

        keyboard = InlineKeyboardBuilder()

        boy = types.InlineKeyboardButton(text="парень🙎", callback_data="sex_guy")
        girl = types.InlineKeyboardButton(text="девушка🙎‍♀️", callback_data="sex_girl")
        any_sex = types.InlineKeyboardButton(text="любой🚻", callback_data="sex_any")
        return_but = types.InlineKeyboardButton(text="вернуться↩", callback_data="return")

        keyboard.add(boy, girl, any_sex, return_but)
        await bot.send_message(callback_query.from_user.id, "Пол собеседника:", reply_markup=keyboard.as_markup())

    # конец обработчиков сообщений для чата


async def waiting(callback_query: types.CallbackQuery, chat_id, sex):
    msg = callback_query.message
    db.add_queue(chat_id, sex)
    await msg.delete()

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


@main_router.callback_query()
async def process_callback_button(callback_query: types.CallbackQuery):
    chat_type = callback_query.message.chat.type
    msg = callback_query.message

    if chat_type == ChatType.PRIVATE:
        data = callback_query.data
        chat_id = callback_query.message.chat.id
        if data == 'return':
            await msg.delete()
            await start_command(msg)

        elif data == 'anon_chat':
            await anon_chat_but(callback_query)

        elif data == 'gender selection':
            await queue_with_reg(callback_query)

        elif data == 'reg_guy' or data == 'reg_girl':
            sex = data.split('_')[1]
            await bot.send_message(callback_query.from_user.id, "✅Успешная регистрация!✅")
            await anon_chat_but(callback_query)
            db.add_sex(chat_id, f'{sex}')

        elif data == 'sex_guy' or data == 'sex_girl' or data == 'sex_any':
            sex = data.split('_')[1]
            await queue(callback_query, f'{sex}')

        elif data == 'stop_queue':
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
