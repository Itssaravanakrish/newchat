from aiogram import Bot, Dispatcher, executor, types
from data import DataBase
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from googletrans import Translator
import config as cfg
import logging
import functions as func

logging.basicConfig(level=logging.INFO)

bot = Bot(cfg.TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
db = DataBase('192.168.2.35', '5432', 'anonchat', 'anon_user', 'anon828282')

class Register(StatesGroup):
    reg_1 = State()

class Settings_cl(StatesGroup):
    settings_1 = State()
    settings_change = State()
    language_change = State()

def text_translator(text, src, dest):
    try:
        translator = Translator()
        translations = translator.translate(text=text, src=src, dest=dest)

        return translations.text
    except Exception as es:
        return es

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        chat_info = db.get_active_chat(message.from_user.id)
        if(not db.check_user(message.from_user.id)):
            markup = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton("English", callback_data='english')
            button2 = types.InlineKeyboardButton("Русский", callback_data='russian')
            button3 = types.InlineKeyboardButton("Հայերեն", callback_data='armenian')
            markup.add(button1, button2, button3)
            await message.answer("SELLECT LANGUAGE", reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await Register.reg_1.set()
        else:
            lang = db.get_lang(message.from_user.id)
            if chat_info == False:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                button1 = types.KeyboardButton(cfg.SEARCH(lang))
                button2 = types.KeyboardButton(cfg.SETTINGS(lang))
                markup.add(button1, button2)
                await message.answer(cfg.START(lang), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            else:
                await message.answer(cfg.CANCEL_TEXT(lang), parse_mode=types.ParseMode.MARKDOWN)

#command search
async def search(message):
    chat_info = db.get_active_chat(message.from_user.id)
    queue_info = db.get_queue(message.from_user.id)
    lang = db.get_lang(message.from_user.id)
    if chat_info == False:
        if queue_info == False:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.STOP_SEARCH(lang))
            markup.add(button1)

            chat_two = db.get_user_queue()

            if db.create_chat(message.from_user.id, chat_two) == False:
                db.add_queue(message.from_user.id)
                await message.answer(cfg.SEARCH_PROCESS(lang), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            else:
                try:
                    lang_two = db.get_lang(chat_two)
                    await dp.bot.send_message(message.from_user.id, cfg.SEARCH_TRUE(lang), reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                    await dp.bot.send_message(chat_two, cfg.SEARCH_TRUE(lang_two), reply_markup=types.ReplyKeyboardRemove(), parse_mode=types.ParseMode.MARKDOWN)
                except BotBlocked:
                    db.delete_chat(message.from_user.id)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    button1 = types.KeyboardButton(cfg.SEARCH(lang))
                    button2 = types.KeyboardButton(cfg.SETTINGS(lang))
                    markup.add(button1, button2)
                    await message.answer(cfg.BOT_BLOCKED(lang), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.answer(cfg.CANCEL_SEARCH_PROCESS(lang), parse_mode=types.ParseMode.MARKDOWN)
    else:
        await message.answer(cfg.CANCEL_TEXT(lang), parse_mode=types.ParseMode.MARKDOWN)

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

#command cancel_search
async def cancel_search(message):
    lang = db.get_lang(message.from_user.id)
    if db.get_queue(message.from_user.id):
        db.delete_queue(message.from_user.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton(cfg.SEARCH(lang))
        button2 = types.KeyboardButton(cfg.SETTINGS(lang))
        markup.add(button1, button2)
        await message.answer(cfg.STOP_SEARCH_TEXT(lang), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
    else:
        await message.answer(cfg.CANCEl_STOP_SEARCH_TEXT(lang), parse_mode=types.ParseMode.MARKDOWN)

@dp.callback_query_handler(state=Register.reg_1)
async def register_akk(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.message.chat.type == types.ChatType.PRIVATE:
        if callback_query.data == 'english':
            db.add_user(callback_query.from_user.id, callback_query.from_user.first_name, callback_query.from_user.username, 0)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.SEARCH(0))
            button2 = types.KeyboardButton(cfg.SETTINGS(0))
            markup.add(button1, button2)
            await callback_query.answer(cfg.LANGUAGE_CORRECT_TEXT(0))
            await callback_query.message.answer(cfg.START(0), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await state.finish()
        elif callback_query.data == 'russian':
            db.add_user(callback_query.from_user.id, callback_query.from_user.first_name, callback_query.from_user.username, 1)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.SEARCH(1))
            button2 = types.KeyboardButton(cfg.SETTINGS(1))
            markup.add(button1, button2)
            await callback_query.answer(cfg.LANGUAGE_CORRECT_TEXT(1))
            await callback_query.message.answer(cfg.START(1), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await state.finish()
        elif callback_query.data == 'armenian':
            db.add_user(callback_query.from_user.id, callback_query.from_user.first_name, callback_query.from_user.username, 2)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.SEARCH(2))
            button2 = types.KeyboardButton(cfg.SETTINGS(2))
            markup.add(button1, button2)
            await callback_query.answer(cfg.LANGUAGE_CORRECT_TEXT(2))
            await callback_query.message.answer(cfg.START(2), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await state.finish()

@dp.message_handler(state=Register.reg_1)
async def error_text_register(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        if message.text == "/register":
            markup = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton("English", callback_data='english')
            button2 = types.InlineKeyboardButton("Русский", callback_data='russian')
            button3 = types.InlineKeyboardButton("Հայերեն", callback_data='armenian')
            markup.add(button1, button2, button3)
            await message.answer("SELECT LANGUAGE", reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.answer(cfg.ERROR_REGISTER(), parse_mode=types.ParseMode.MARKDOWN)

@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        chat_info = db.get_active_chat(message.from_user.id)
        lang = db.get_lang(message.from_user.id)
        if chat_info != False:
            db.delete_chat(message.from_user.id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.SEARCH(lang))
            button2 = types.KeyboardButton(cfg.SETTINGS(lang))
            markup.add(button1, button2)
            lang_two = db.get_lang(chat_info)
            markups = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            buttons1 = types.KeyboardButton(cfg.SEARCH(lang_two))
            buttons2 = types.KeyboardButton(cfg.SETTINGS(lang_two))
            markup.add(buttons1, buttons2)
            await dp.bot.send_message(message.from_user.id, cfg.STOP_DIALOG_TEXT(lang), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await dp.bot.send_message(chat_info, cfg.STOP_DIALOG_TEXT_SOBESEDNIK(lang_two), reply_markup=markups, parse_mode=types.ParseMode.MARKDOWN)
        else:

            await message.answer(cfg.CANCEl_STOP_SEARCH_TEXT(lang), parse_mode=types.ParseMode.MARKDOWN)

@dp.message_handler(commands=['search'])
async def search_commands(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await search(message)

@dp.message_handler(commands=['next'])
async def next(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        chat_info = db.get_active_chat(message.from_user.id)
        queue_info = db.get_queue(message.from_user.id)
        lang = db.get_lang(message.from_user.id)
        if chat_info != False:
            db.delete_chat(message.from_user.id)
            markups = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            buttons1 = types.KeyboardButton(cfg.SEARCH(lang))
            buttons2 = types.KeyboardButton(cfg.SETTINGS(lang))
            markups.add(buttons1, buttons2)

            lang_two = db.get_lang(chat_info)
            markup_two = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button_two1 = types.KeyboardButton(cfg.SEARCH(lang_two))
            button_two2 = types.KeyboardButton(cfg.SETTINGS(lang))
            markup_two.add(button_two1, button_two2)
            await dp.bot.send_message(chat_info, cfg.STOP_DIALOG_TEXT_SOBESEDNIK(lang_two), reply_markup=markup_two, parse_mode=types.ParseMode.MARKDOWN)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.STOP_SEARCH(lang))
            markup.add(button1)
            chat_two = db.get_user_queue()
            if db.create_chat(message.from_user.id, chat_two) == False:
                db.add_queue(message.from_user.id)
                await message.answer(cfg.SEARCH_PROCESS(lang), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            else:
                lang_two = db.get_lang(chat_two)
                await dp.bot.send_message(message.from_user.id, cfg.SEARCH_TRUE(lang), parse_mode=types.ParseMode.MARKDOWN)
                await dp.bot.send_message(chat_two, cfg.SEARCH_TRUE(lang_two), parse_mode=types.ParseMode.MARKDOWN)
        elif queue_info != False:
            await message.answer(cfg.CANCEL_SEARCH_PROCESS(lang), parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.answer(cfg.CANCEl_STOP_SEARCH_TEXT(lang), parse_mode=types.ParseMode.MARKDOWN)

@dp.message_handler(commands=['link'])
async def link(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        chat_info = db.get_active_chat(message.from_user.id)
        lang = db.get_lang(message.from_user.id)
        lang_two = db.get_lang(chat_info)
        if chat_info != False:
            await dp.bot.send_message(chat_info, cfg.LINK(lang_two, func.nick_with_link(cfg.LINK_SSILKA(lang_two), message.from_user.id)), parse_mode=types.ParseMode.MARKDOWN)
            await message.answer(cfg.CORRECT_MY_LINK(lang), parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.answer(cfg.CANCEl_STOP_SEARCH_TEXT(lang), parse_mode=types.ParseMode.MARKDOWN)

@dp.message_handler(commands=['cancel'])
async def cancel_search_commands(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await cancel_search(message)

@dp.message_handler(content_types=['text', 'photo', 'document', 'video'])
async def text(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        lang = db.get_lang(message.from_user.id)
        if message.text == cfg.SEARCH(lang):
            await search(message)
        elif message.text == cfg.STOP_SEARCH(lang):
            await cancel_search(message)
        elif message.text == cfg.SETTINGS(lang):
            markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button_settings1 = types.KeyboardButton(cfg.CHANGE_LANGUAGE(lang))
            button_settings2 = types.KeyboardButton(cfg.BACK(lang))
            markup_settings.add(button_settings1, button_settings2)
            await message.answer(cfg.SELECT_SETTINGS_TEXT(lang))
            await Settings_cl.settings_1.set()
        else:
            chat_info = db.get_active_chat(message.from_user.id)
            queue_info = db.get_queue(message.from_user.id)
            if chat_info != False:
                try:
                    lang_two = db.get_lang(chat_info)
                    lang_text = db.get_lang_text(message.from_user.id)
                    lang_text_two = db.get_lang_text(chat_info)
                    try:
                        if message.text:
                            if lang == lang_two:
                                await dp.bot.send_message(chat_info, message.text)
                            else:
                                await dp.bot.send_message(chat_info, text_translator(text=message.text, src=lang_text, dest=lang_text_two))
                        elif message.photo:
                            if message.caption:
                                if lang == lang_two:
                                    await dp.bot.send_photo(chat_info, message.photo[-1].file_id, caption=message.caption)
                                else:
                                    await dp.bot.send_photo(chat_info, message.photo[-1].file_id, caption=text_translator(text=message.caption, src=lang_text, dest=lang_text_two))
                            else:
                                await dp.bot.send_photo(chat_info, message.photo[-1].file_id)
                        elif message.video:
                            if message.caption:
                                if lang == lang_two:
                                    await dp.bot.send_video(chat_info, message.video.file_id, caption=message.caption)
                                else:
                                    await dp.bot.send_video(chat_info, message.video.file_id, caption=text_translator(text=message.caption, src=lang_text, dest=lang_text_two))
                            else:
                                await dp.bot.send_video(chat_info, message.video.file_id)
                        else:
                            await message.answer(cfg.CANCEL_DOCUMENT_TEXT(lang), parse_mode=types.ParseMode.MARKDOWN)
                    except Exception as ex:
                        await message.answer(cfg.ERROR_DOCUMENT(lang), parse_mode=types.ParseMode.MARKDOWN)
                        print(f"[ERROR] {ex}")
                except BotBlocked:
                    db.delete_chat(message.from_user.id)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    button1 = types.KeyboardButton(cfg.SEARCH(lang))
                    button2 = types.KeyboardButton(cfg.SETTINGS(lang))
                    markup.add(button1, button2)
                    await message.answer(cfg.BOT_BLOCKED(lang), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            elif queue_info == False:
                await message.answer(cfg.CANCEL_TEXT_BOT(lang), parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(state=Settings_cl.settings_1)
async def settings_cl_func(message: types.Message, state: FSMContext):
    if message.chat.type == types.ChatType.PRIVATE:
        lang = db.get_lang(message.from_user.id)
        if message.text == cfg.CHANGE_LANGUAGE(lang):
            markup = types.InlineKeyboardMarkup(row_width=1)
            button1 = types.InlineKeyboardButton(cfg.BACK(lang), callback_data='english')
            button2 = types.InlineKeyboardButton(cfg.BACK(lang), callback_data='russian')
            button3 = types.InlineKeyboardButton(cfg.BACK(lang), callback_data='armenian')
            button4 = types.InlineKeyboardButton(cfg.BACK(lang), callback_data='back')
            markup.add(button1, button2, button3, button4)
            await message.answer(cfg.SELECT_LANGUAGE_TEXT(lang), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await Settings_cl.language_change.set()
        elif message.text == cfg.BACK(lang):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.SEARCH(lang))
            button2 = types.KeyboardButton(cfg.SETTINGS(lang))
            markup.add(button1, button2)
            await message.answer(cfg.BACK_TEXT(lang), parse_mode=types.ParseMode.MARKDOWN)
            await state.reset_state()
        else:
            await message.answer(cfg.SELECT_SETTINGS_TEXT(lang))

@dp.callback_query_handler(state=Settings_cl.language_change)
async def register_akk(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.message.chat.type == types.ChatType.PRIVATE:
        lang = db.get_lang(callback_query.from_user.id)
        if callback_query.data == 'english':
            db.add_user(callback_query.from_user.id, callback_query.from_user.first_name, callback_query.from_user.username, 0)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.SEARCH(0))
            button2 = types.KeyboardButton(cfg.SETTINGS(0))
            markup.add(button1, button2)
            await callback_query.answer(cfg.LANGUAGE_CORRECT_TEXT(0))
            await callback_query.message.answer(cfg.START(0), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await state.finish()
        elif callback_query.data == 'russian':
            db.add_user(callback_query.from_user.id, callback_query.from_user.first_name, callback_query.from_user.username, 1)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.SEARCH(1))
            button2 = types.KeyboardButton(cfg.SETTINGS(1))
            markup.add(button1, button2)
            await callback_query.answer(cfg.LANGUAGE_CORRECT_TEXT(1))
            await callback_query.message.answer(cfg.START(1), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await state.finish()
        elif callback_query.data == 'armenian':
            db.add_user(callback_query.from_user.id, callback_query.from_user.first_name, callback_query.from_user.username, 2)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button1 = types.KeyboardButton(cfg.SEARCH(2))
            button2 = types.KeyboardButton(cfg.SETTINGS(2))
            markup.add(button1, button2)
            await callback_query.answer(cfg.LANGUAGE_CORRECT_TEXT(2))
            await callback_query.message.answer(cfg.START(2), reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await state.finish()
        elif callback_query.data == 'back':
            markup_settings = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button_settings1 = types.KeyboardButton(cfg.CHANGE_LANGUAGE(lang))
            button_settings2 = types.KeyboardButton(cfg.BACK(lang))
            markup_settings.add(button_settings1, button_settings2)
            await callback_query.message.answer(cfg.SELECT_SETTINGS_TEXT(lang))
            await Settings_cl.settings_1.set()

if __name__ == '__main__':
    executor.start_polling(dp)
