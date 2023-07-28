from aiogram import Bot, Dispatcher, executor, types
from data import DataBase
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime, timedelta
from aiogram.types.message import ContentType
import config as cfg
import logging
import functions as func

logging.basicConfig(level=logging.INFO)

bot = Bot(cfg.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
db = DataBase('192.168.2.35', '5432', 'anonchat', 'anon_user', 'anon828282')

PRICE = types.LabeledPrice(label="Подписка на день", amount=500*100)

class register(StatesGroup):
    reg_1 = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        chat_info = db.get_active_chat(message.from_user.id)
        if(not db.check_user(message.from_user.id)):
            markup = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton(cfg.MALE, callback_data='male')
            button2 = types.InlineKeyboardButton(cfg.FEMALE, callback_data='female')
            markup.add(button1, button2)
            await message.answer(cfg.REGISTER_TEXT, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await register.reg_1.set()
        else:
            if chat_info == False:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                button1 = types.KeyboardButton(cfg.SEARCH)
                markup.add(button1)
                await message.answer(cfg.START, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            else:
                await message.answer(cfg.CANCEL_TEXT, parse_mode=types.ParseMode.MARKDOWN)

#command search
async def search(message):
    chat_info = db.get_active_chat(message.from_user.id)
    queue_info = db.get_queue(message.from_user.id)
    if chat_info == False:
        if queue_info == False:
            chann = db.get_channels()
            admin_channels = await get_admin_channels(chann)
            text = cfg.TEXT_SUBCRIBE
            for i, item in enumerate(admin_channels, 1):
                text += f"\n {i}. {item}"
            for i in admin_channels:
                subscribded = await check_user_subscription(i, message.from_user.id)
                if subscribded or db.check_channels() is None:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    button1 = types.KeyboardButton(cfg.STOP_SEARCH)
                    markup.add(button1)

                    chat_two = db.get_user_queue()

                    if db.create_chat(message.from_user.id, chat_two) == False:
                        db.add_queue(message.from_user.id)
                        await message.answer(cfg.SEARCH_PROCESS, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
                    else:
                        try:
                            await dp.bot.send_message(message.from_user.id, cfg.SEARCH_TRUE, reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                            await dp.bot.send_message(chat_two, cfg.SEARCH_TRUE, reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                        except BotBlocked:
                            db.delete_chat(message.from_user.id)
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                            button1 = types.KeyboardButton(cfg.SEARCH)
                            button2 = types.KeyboardButton(cfg.SEARCH_MALE)
                            markup.add(button1, button2)
                            await message.answer(cfg.BOT_BLOCKED, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
                else:
                    await message.answer(text)
        else:
            await message.answer(cfg.CANCEL_SEARCH_PROCESS, parse_mode=types.ParseMode.MARKDOWN)
    else:
        await message.answer(cfg.CANCEL_TEXT, parse_mode=types.ParseMode.MARKDOWN)

#check admin in channel
async def check_bot_admin_rights(channel_username):
    try:
        bot_info = await bot.get_me()

        # Получаем информацию о членстве бота в канале по @username
        chat_member = await bot.get_chat_member(f"{channel_username}", bot_info.id)

        # Проверяем, есть ли у бота права администратора в канале
        if chat_member.status == 'administrator':
            return True
        else:
            return False

    except Exception as e:
        # Если возникла ошибка, бот скорее всего не имеет прав администратора в канале
        return False

async def get_admin_channels(channel_usernames):
    admin_channels = []
    for channel_username in channel_usernames:
        if await check_bot_admin_rights(channel_username):
            admin_channels.append(channel_username)
    return admin_channels

#check subcribed user in channel
async def check_user_subscription(channel_username, user_id):
    try:
        # Получаем информацию о членстве пользователя в канале
        chat_member = await bot.get_chat_member(f"{channel_username}", user_id)

        # Проверяем, является ли пользователь участником канала
        if chat_member.status == 'member' or chat_member.status == 'creator':
            return True
        else:
            return False

    except Exception as e:
        # Если возникла ошибка, пользователь скорее всего не является участником канала
        return False

#command cancel_search
async def cancel_search(message):
    if db.get_queue(message.from_user.id):
        db.delete_queue(message.from_user.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton(cfg.SEARCH)
        markup.add(button1)
        await message.answer(cfg.STOP_SEARCH_TEXT, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
    else:
        await message.answer(cfg.CANCEl_STOP_DIALOG_TEXT, parse_mode=types.ParseMode.MARKDOWN)

@dp.callback_query_handler(state=register.reg_1)
async def register_akk(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.message.chat.type == types.ChatType.PRIVATE:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton(cfg.SEARCH)
        markup.add(button1)
        if callback_query.data == 'male':
            db.add_user(callback_query.from_user.id, callback_query.from_user.first_name, callback_query.from_user.username, 'male')
            await callback_query.answer(cfg.MALE_CORRECT_TEXT)
            await callback_query.message.answer(cfg.START, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await state.finish()
        elif callback_query.data == 'female':
            db.add_user(callback_query.from_user.id, callback_query.from_user.first_name, callback_query.from_user.username, 'female')
            await callback_query.answer(cfg.FEMALE_CORRECT_TEXT)
            await callback_query.message.answer(cfg.START, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await state.finish()

@dp.message_handler(state=register.reg_1)
async def error_text_register(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        if message.text == "/register":
            markup = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton(cfg.MALE, callback_data='male')
            button2 = types.InlineKeyboardButton(cfg.FEMALE, callback_data='female')
            markup.add(button1, button2)
            await message.answer(cfg.REGISTER_TEXT, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.answer(cfg.ERROR_REGISTER, parse_mode=types.ParseMode.MARKDOWN)

@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        chat_info = db.get_active_chat(message.from_user.id)
        if chat_info != False:
            db.delete_chat(message.from_user.id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.SEARCH)
            markup.add(button1)
            await dp.bot.send_message(message.from_user.id, cfg.STOP_DIALOG_TEXT, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await dp.bot.send_message(chat_info, cfg.STOP_DIALOG_TEXT_SOBESEDNIK, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
        else:

            await message.answer(cfg.CANCEl_STOP_SEARCH_TEXT, parse_mode=types.ParseMode.MARKDOWN)

@dp.message_handler(commands=['search'])
async def search_commands(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await search(message)

@dp.message_handler(commands=['next'])
async def next(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        chat_info = db.get_active_chat(message.from_user.id)
        queue_info = db.get_queue(message.from_user.id)
        if chat_info != False:
            db.delete_chat(message.from_user.id)
            markups = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            buttons1 = types.KeyboardButton(cfg.SEARCH)
            markups.add(buttons1)
            await dp.bot.send_message(chat_info, cfg.STOP_DIALOG_TEXT_SOBESEDNIK, reply_markup=markups, parse_mode=types.ParseMode.MARKDOWN)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.STOP_SEARCH)
            markup.add(button1)

            chat_two = db.get_user_queue()
            chann = db.get_channels()
            admin_channels = await get_admin_channels(chann)
            text = cfg.TEXT_SUBCRIBE
            for i, item in enumerate(admin_channels, 1):
                text += f"\n {i}. {item}"
            for i in admin_channels:
                subscribded = await check_user_subscription(i, message.from_user.id)
                if subscribded:
                    if db.create_chat(message.from_user.id, chat_two) == False:
                        db.add_queue(message.from_user.id)
                        await message.answer(cfg.SEARCH_PROCESS, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
                    else:
                        await dp.bot.send_message(message.from_user.id, cfg.SEARCH_TRUE, parse_mode=types.ParseMode.MARKDOWN)
                        await dp.bot.send_message(chat_two, cfg.SEARCH_TRUE, parse_mode=types.ParseMode.MARKDOWN)
                else:
                    markups = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    buttons1 = types.KeyboardButton(cfg.SEARCH)
                    markups.add(buttons1)
                    await message.answer(text, reply_markup=markups)
        elif queue_info != False:
            await message.answer(cfg.CANCEl_STOP_SEARCH_TEXT, parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.answer(cfg.CANCEL_SEARCH_PROCESS, parse_mode=types.ParseMode.MARKDOWN)

@dp.message_handler(commands=['link'])
async def link(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        chat_info = db.get_active_chat(message.from_user.id)
        if chat_info != False:
            await dp.bot.send_message(chat_info, f"Собеседник отправил вам {func.nick_with_link('ссылку', message.from_user.id)} своей телеграм аккаунта", parse_mode=types.ParseMode.MARKDOWN)
            await message.answer(cfg.CORRECT_MY_LINK, parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.answer(cfg.CANCEl_STOP_SEARCH_TEXT, parse_mode=types.ParseMode.MARKDOWN)

@dp.message_handler(commands=['cancel'])
async def cancel_search_commands(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await cancel_search(message)

@dp.message_handler(commands=['channels'])
async def channels(message: types.Message):
    chann = db.get_channels()
    admin_channels = await get_admin_channels(chann)
    text = cfg.TEXT_SUBCRIBE
    for i, item in enumerate(admin_channels, 1):
        text += f"\n {i}. {item}"
    for i in admin_channels:
        subscribded = await check_user_subscription(i, message.from_user.id)
        if subscribded:
            await message.answer("Вы подписаны на каналы!")
        else:
            await message.answer(text)

@dp.message_handler(content_types=['text', 'photo', 'document', 'video'])
async def text(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        if message.text == cfg.SEARCH:
            await search(message)
        elif message.text == cfg.STOP_SEARCH:
            await cancel_search(message)
        else:
            chat_info = db.get_active_chat(message.from_user.id)
            queue_info = db.get_queue(message.from_user.id)
            if chat_info != False:
                try:
                    if message.text:
                        await dp.bot.send_message(chat_info, message.text)
                    elif message.photo:
                        if message.caption:
                            await dp.bot.send_photo(chat_info, message.photo[-1].file_id, caption=message.caption)
                        else:
                            await dp.bot.send_photo(chat_info, message.photo[-1].file_id)
                    elif message.video:
                        if message.caption:
                            await dp.bot.send_video(chat_info, message.video.file_id, caption=message.caption)
                        else:
                            await dp.bot.send_video(chat_info, message.video.file_id)
                    else:
                        await message.answer(cfg.CANCEL_DOCUMENT_TEXT, parse_mode=types.ParseMode.MARKDOWN)
                except BotBlocked:
                    db.delete_chat(message.from_user.id)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    button1 = types.KeyboardButton(cfg.SEARCH)
                    markup.add(button1)
                    await message.answer(cfg.BOT_BLOCKED, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            elif queue_info == False:
                await message.answer(cfg.CANCEL_TEXT_BOT, parse_mode=types.ParseMode.MARKDOWN)



if __name__ == '__main__':
    executor.start_polling(dp)
