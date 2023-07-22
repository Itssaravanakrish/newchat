from aiogram import Bot, Dispatcher, executor, types
from data import DataBase
from aiogram.utils.exceptions import BotBlocked
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher.storage import FSMContext
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config as cfg
import logging
import functions as func

logging.basicConfig(level=logging.INFO)

bot = Bot(cfg.TOKEN)
dp = Dispatcher(bot)
db = DataBase('192.168.2.35', '5432', 'anonchat', 'anon_user', 'anon828282')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        chat_info = db.get_active_chat(message.from_user.id)
        if(not db.check_user(message.from_user.id)):
            db.add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
        if chat_info == False:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.SEARCH)
            markup.add(button1)
            await message.answer(cfg.START, reply_markup=markup)
        else:
            await message.answer(cfg.CANCEL_TEXT)

@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        chat_info = db.get_active_chat(message.from_user.id)
        if chat_info != False:
            db.delete_chat(message.from_user.id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.SEARCH)
            markup.add(button1)
            await dp.bot.send_message(message.from_user.id, cfg.STOP_DIALOG_TEXT, reply_markup=markup)
            await dp.bot.send_message(chat_info, cfg.STOP_DIALOG_TEXT_SOBESEDNIK, reply_markup=markup)
        else:

            await message.answer(cfg.CANCEl_STOP_DIALOG_TEXT)

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
            await dp.bot.send_message(chat_info, cfg.STOP_DIALOG_TEXT_SOBESEDNIK, reply_markup=markups)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.STOP_SEARCH)
            markup.add(button1)

            chat_two = db.get_user_queue()

            if db.create_chat(message.from_user.id, chat_two) == False:
                db.add_queue(message.from_user.id)
                await message.answer(cfg.SEARCH_PROCESS, reply_markup=markup)
            else:
                markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                buttons1 = types.KeyboardButton(cfg.SEARCH_DRUGOGO)
                buttons2 = types.KeyboardButton(cfg.STOP_DIALOG)
                buttons3 = types.KeyboardButton(cfg.TAKE_MY_LINK)
                markup1.add(buttons1, buttons3, buttons2)
                await dp.bot.send_message(message.from_user.id, cfg.SEARCH_TRUE, reply_markup=markup1)
                await dp.bot.send_message(chat_two, cfg.SEARCH_TRUE, reply_markup=markup1)
        else:
            if queue_info == False:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                button1 = types.KeyboardButton(cfg.STOP_SEARCH)
                markup.add(button1)

                chat_two = db.get_user_queue()

                if db.create_chat(message.from_user.id, chat_two) == False:
                    db.add_queue(message.from_user.id)
                    await message.answer(cfg.SEARCH_PROCESS, reply_markup=markup)
                else:
                    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    buttons1 = types.KeyboardButton(cfg.SEARCH_DRUGOGO)
                    buttons2 = types.KeyboardButton(cfg.STOP_DIALOG)
                    buttons3 = types.KeyboardButton(cfg.TAKE_MY_LINK)
                    markup1.add(buttons1, buttons3, buttons2)
                    await dp.bot.send_message(message.from_user.id, cfg.SEARCH_TRUE, reply_markup=markup1)
                    await dp.bot.send_message(chat_two, cfg.SEARCH_TRUE, reply_markup=markup1)
            else:
                await message.answer(cfg.CANCEL_SEARCH_PROCESS)


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        if message.text == cfg.SEARCH:
            chat_info = db.get_active_chat(message.from_user.id)
            queue_info = db.get_queue(message.from_user.id)
            if chat_info == False:
                if queue_info == False:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    button1 = types.KeyboardButton(cfg.STOP_SEARCH)
                    markup.add(button1)

                    chat_two = db.get_user_queue()

                    if db.create_chat(message.from_user.id, chat_two) == False:
                        db.add_queue(message.from_user.id)
                        await message.answer(cfg.SEARCH_PROCESS, reply_markup=markup)
                    else:
                        try:
                            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                            buttons1 = types.KeyboardButton(cfg.SEARCH_DRUGOGO)
                            buttons2 = types.KeyboardButton(cfg.STOP_DIALOG)
                            buttons3 = types.KeyboardButton(cfg.TAKE_MY_LINK)
                            markup1.add(buttons1, buttons3, buttons2)
                            await dp.bot.send_message(message.from_user.id, cfg.SEARCH_TRUE, reply_markup=markup1)
                            await dp.bot.send_message(chat_two, cfg.SEARCH_TRUE, reply_markup=markup1)
                        except BotBlocked:
                            db.delete_chat(message.from_user.id)
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                            button1 = types.KeyboardButton(cfg.SEARCH)
                            markup.add(button1)
                            await message.answer(cfg.BOT_BLOCKED, reply_markup=markup)
                else:
                    await message.answer(cfg.CANCEL_SEARCH_PROCESS)
            else:
                await message.answer(cfg.CANCEL_TEXT)
        elif message.text == cfg.STOP_DIALOG:
            chat_info = db.get_active_chat(message.from_user.id)
            if chat_info != False:
                db.delete_chat(message.from_user.id)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                button1 = types.KeyboardButton(cfg.SEARCH)
                markup.add(button1)
                await dp.bot.send_message(message.from_user.id, cfg.STOP_DIALOG_TEXT, reply_markup=markup)
                await dp.bot.send_message(chat_info, cfg.STOP_DIALOG_TEXT_SOBESEDNIK, reply_markup=markup)
            else:
                await message.answer(cfg.CANCEl_STOP_SEARCH_TEXT)
        elif message.text == cfg.TAKE_MY_LINK:
            chat_info = db.get_active_chat(message.from_user.id)
            if chat_info != False:
                await dp.bot.send_message(message.from_user.id, cfg.CORRECT_MY_LINK, parse_mode=types.ParseMode.MARKDOWN)
                await dp.bot.send_message(chat_info, f"Ваш собеседник дал {func.nick_with_link('ссылку', message.from_user.id)} на свой аккаунт телеграм.", parse_mode=types.ParseMode.MARKDOWN)
            else:
                await message.answer(cfg.CANCEl_STOP_SEARCH_TEXT)
        elif message.text == cfg.STOP_SEARCH:
            if db.get_queue(message.from_user.id):
                db.delete_queue(message.from_user.id)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                button1 = types.KeyboardButton(cfg.SEARCH)
                markup.add(button1)
                await message.answer(cfg.STOP_SEARCH_TEXT, reply_markup=markup)
            else:
                await message.answer(cfg.CANCEl_STOP_DIALOG_TEXT)
        elif message.text == cfg.SEARCH_DRUGOGO:
            chat_info = db.get_active_chat(message.from_user.id)
            if chat_info != False:
                db.delete_chat(message.from_user.id)
                markups = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                buttons1 = types.KeyboardButton(cfg.SEARCH)
                markups.add(buttons1)
                await dp.bot.send_message(chat_info, cfg.STOP_DIALOG_TEXT_SOBESEDNIK, reply_markup=markups)

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                button1 = types.KeyboardButton(cfg.STOP_SEARCH)
                markup.add(button1)

                chat_two = db.get_user_queue()

                if db.create_chat(message.from_user.id, chat_two) == False:
                    db.add_queue(message.from_user.id)
                    await message.answer(cfg.SEARCH_PROCESS, reply_markup=markup)
                else:
                    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    buttons1 = types.KeyboardButton(cfg.SEARCH_DRUGOGO)
                    buttons2 = types.KeyboardButton(cfg.STOP_DIALOG)
                    markup1.add(buttons1, buttons2)
                    await dp.bot.send_message(message.from_user.id, cfg.SEARCH_TRUE, reply_markup=markup1)
                    await dp.bot.send_message(chat_two, cfg.SEARCH_TRUE, reply_markup=markup1)
            else:
                await message.answer(cfg.CANCEl_STOP_DIALOG_TEXT)
        else:
            chat_info = db.get_active_chat(message.from_user.id)
            if chat_info != False:
                try:
                    await dp.bot.send_message(chat_info, message.text)
                except BotBlocked:
                    db.delete_chat(message.from_user.id)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    button1 = types.KeyboardButton(cfg.SEARCH)
                    markup.add(button1)
                    await message.answer(cfg.BOT_BLOCKED, reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp)
