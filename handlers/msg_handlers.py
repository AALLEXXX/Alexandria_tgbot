from create_bot import db, bot
from aiogram import Router, types, F

msg_router = Router()

@msg_router.message(F.photo)
async def handle_photo_message(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_photo(act_chat[2], photo=message.photo[-1].file_id)


@msg_router.message(F.audio)
async def handle_audio_message(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_audio(act_chat[2], message.audio.file_id)


@msg_router.message(F.video)
async def handle_video_message(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_video(act_chat[2], message.video.file_id)


@msg_router.message(F.video_note)
async def handle_video_circe_message(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_video_note(act_chat[2], message.video_note.file_id)


@msg_router.message(F.sticker)
async def handle_stickers_message(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_sticker(act_chat[2], message.sticker.file_id)


@msg_router.message(F.voice)
async def handle_voice_message(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_voice(act_chat[2], message.voice.file_id)


@msg_router.message(F.text)
async def anon_chat(message: types.Message):
    act_chat = db.get_active_chat(message.chat.id)
    if db.check_active_chat(message.chat.id):
        await bot.send_message(act_chat[2], message.text)