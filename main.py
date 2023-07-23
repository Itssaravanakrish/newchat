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
                button2 = types.KeyboardButton(cfg.SEARCH_MALE)
                markup.add(button1, button2)
                await message.answer(cfg.START, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            else:
                await message.answer(cfg.CANCEL_TEXT, parse_mode=types.ParseMode.MARKDOWN)

@dp.callback_query_handler(state=register.reg_1)
async def register_akk(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.message.chat.type == types.ChatType.PRIVATE:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        button1 = types.KeyboardButton(cfg.SEARCH)
        button2 = types.KeyboardButton(cfg.SEARCH_MALE)
        markup.add(button1, button2)
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
            button2 = types.KeyboardButton(cfg.SEARCH_MALE)
            markup.add(button1, button2)
            await dp.bot.send_message(message.from_user.id, cfg.STOP_DIALOG_TEXT, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            await dp.bot.send_message(chat_info, cfg.STOP_DIALOG_TEXT_SOBESEDNIK, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
        else:

            await message.answer(cfg.CANCEl_STOP_DIALOG_TEXT, parse_mode=types.ParseMode.MARKDOWN)

@dp.message_handler(commands=['search'])
async def search(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
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
                await message.answer(cfg.CANCEL_SEARCH_PROCESS, parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.answer(cfg.CANCEL_TEXT, parse_mode=types.ParseMode.MARKDOWN)

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

            if db.create_chat(message.from_user.id, chat_two) == False:
                db.add_queue(message.from_user.id)
                await message.answer(cfg.SEARCH_PROCESS, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            else:
                await dp.bot.send_message(message.from_user.id, cfg.SEARCH_TRUE, parse_mode=types.ParseMode.MARKDOWN)
                await dp.bot.send_message(chat_two, cfg.SEARCH_TRUE, parse_mode=types.ParseMode.MARKDOWN)
        elif queue_info != False:
            await message.answer(cfg.CANCEl_STOP_SEARCH_TEXT, parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.answer(cfg.CANCEL_SEARCH_PROCESS, parse_mode=types.ParseMode.MARKDOWN)

@dp.message_handler(commands=['link'])
async def link(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        chat_info = db.get_active_chat(message.from_user.id)
        if chat_info != False:
            await dp.bot.send_message(chat_info, f"*Собеседник отправил вам {func.nick_with_link('ссылку', chat_info)} своей телеграм аккаунта*", parse_mode=types.ParseMode.MARKDOWN)
        else:
            await message.answer(cfg.CANCEl_STOP_SEARCH_TEXT, parse_mode=types.ParseMode.MARKDOWN)

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
                    await message.answer(cfg.CANCEL_SEARCH_PROCESS, parse_mode=types.ParseMode.MARKDOWN)
            else:
                await message.answer(cfg.CANCEL_TEXT, parse_mode=types.ParseMode.MARKDOWN)
        elif message.text == cfg.STOP_SEARCH:
            if db.get_queue(message.from_user.id):
                db.delete_queue(message.from_user.id)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                button1 = types.KeyboardButton(cfg.SEARCH)
                button2 = types.KeyboardButton(cfg.SEARCH_MALE)
                markup.add(button1, button2)
                await message.answer(cfg.STOP_SEARCH_TEXT, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            else:
                await message.answer(cfg.CANCEl_STOP_DIALOG_TEXT, parse_mode=types.ParseMode.MARKDOWN)
        elif message.text == cfg.SEARCH_MALE:
            current_date = datetime.now()
            if db.check_dates(message.from_user.id) is not None:
                database_date_obj = datetime.strptime(db.check_dates(message.from_user.id), '%Y-%m-%d %H:%M:%S.%f')
                if current_date > database_date_obj:
                    # эта функция если прошла подписка
                    db.del_dates(message.from_user.id)
                elif current_date < database_date_obj:
                    # кнопки поиск мужчины или женщины
                    await message.answer("у вас есть подписка")
            else:
                if cfg.PAYMENTS_TOKEN.split(':') == 'TEST':
                    await message.answer("Тестовый платёж")


                await bot.send_invoice(message.chat.id,
                                       title="Подписка на бота",
                                       description="Активация подписки на бота на 1 день!",
                                       provider_token=cfg.PAYMENTS_TOKEN,
                                       currency='rub',
                                       photo_url="https://cdn.xxl.thumbs.canstockphoto.ru/%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D0%B0-%D0%BA%D0%B0%D1%80%D1%82%D0%B0-%D1%81%D1%82%D0%BE%D0%BA%D0%BE%D0%B2%D0%B0%D1%8F-%D1%84%D0%BE%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F_csp5148789.jpg",
                                       photo_width=360,
                                       photo_height=254,
                                       is_flexible=False,
                                       prices=[PRICE],
                                       start_parameter='one-day-subscription',
                                       payload='test-invoice-payload')
        else:
            chat_info = db.get_active_chat(message.from_user.id)
            queue_info = db.get_queue(message.from_user.id)
            if chat_info != False:
                try:
                    await dp.bot.send_message(chat_info, message.text)
                except BotBlocked:
                    db.delete_chat(message.from_user.id)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    button1 = types.KeyboardButton(cfg.SEARCH)
                    button2 = types.KeyboardButton(cfg.SEARCH_MALE)
                    markup.add(button1, button2)
                    await message.answer(cfg.BOT_BLOCKED, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
            elif queue_info == False:
                await message.answer(cfg.CANCEL_TEXT_BOT, parse_mode=types.ParseMode.MARKDOWN)

@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    # {message.successful_payment.total_amount // 100} {message.successful_payment.currency}
    if db.check_dates(message.from_user.id) is not None:
        current_date = db.check_dates(message.from_user.id)
        next_day = current_date + timedelta(days=1)
        db.update_dates(message.from_user.id, next_day)
        await bot.send_message(message.chat.id, f"Вы успешно продлили подписку на 1 день!")
    else:
        current_date = datetime.now()
        next_day = current_date + timedelta(days=1)
        db.add_dates(message.from_user.id, next_day)
        await bot.send_message(message.chat.id, f"Вы успешно приобрели подписку на 1 день!")


if __name__ == '__main__':
    executor.start_polling(dp)
