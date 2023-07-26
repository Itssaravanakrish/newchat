TOKEN = "5815738068:AAH0CLsYyazHP9XgR_1b66pYh02kXMsgxxM"
PAYMENTS_TOKEN = "1744374395:TEST:9bc7a3556eb1e8bed305"

REGISTER_TEXT = "_Для начало общения, вы должны выбрать ваш пол нажимая на кнопку._"
ERROR_REGISTER = "_Вы должны выбрать пол, для общения с людьми.\nЕсли у вас возникла какая то ошибка, вводите команду /register_"

START = "_Привет! Добро пожаловать в анонимный чат.\nДля того чтобы найти собеседника, напишите /search, или нажмите на кнопку ниже._"

SEARCH = "👫 Начать диалог"
STOP_SEARCH = "❌ Отменить поиск"
SEARCH_MALE = "🔎 Поиск по полу"

CORRECT_MY_LINK = "_Вы успешно дали свой телеграм аккаунт вашему собеседнику ✔_"


SEARCH_PROCESS = "_⌛ Идёт поиск собеседника..._"

STOP_SEARCH_TEXT = "_Вы успешно отменили поиск собеседника ✔_"

SEARCH_TRUE = """_Собеседник найден 🦊\n\n/next - искать нового собеседника\n/stop - остановить диалог_\n\n`https://t.me/AnonymChatyBot`"""


STOP_DIALOG_TEXT = "_Вы закончили диалог с собеседником.\nДля того чтобы найти собеседника, напишите /search_"
SEARCH_DRUGOGO_TEXT = "_Вы закончили диалог с собеседником и начали поиск нового собеседника._"

STOP_DIALOG_TEXT_SOBESEDNIK = "_Ваш собеседник закончил с вами диалог.\nДля того чтобы найти собеседника, напишите /search_"
CANCEl_STOP_DIALOG_TEXT = "_❌ Вы не находитесь в поиске_"
CANCEl_STOP_SEARCH_TEXT = "_❌ Вы не находитесь в диалоге_"
CANCEL_TEXT = "_❌ Вы находитесь в диалоге._"
CANCEL_SEARCH_PROCESS = "_❌ Вы находитесь в поиске._"

BOT_BLOCKED = "_Переписка с собеседником закончена, ваш собеседник заблокировал бота ❌_"

CANCEL_TEXT_BOT = "_Напишите /search чтобы искать собеседника_"


MALE = "Мужской"
FEMALE = "Женский"

MALE_CORRECT_TEXT = "Вы успешно выбрали мужской пол"
FEMALE_CORRECT_TEXT = "Вы успешно выбрали женский пол"

# SEARCH_MALE_MALE = "👦 Поиск мужчин"
# SEARCH_MALE_FEMALE = "👩 Поиск женщин"
BACK = "👈 Назад"

# BUTTON_MALE_TEXT = "_Вы успешно выбрали поиск по полу, выберите какой пол хотите выбрать._"

BACK_TEXT = "_Вы успешно вернулись назад._"





# class search_male(StatesGroup):
#     buttons_search = State()

# Оплата поиск по полу

        # elif message.text == cfg.SEARCH_MALE:
        #     current_date = datetime.now()
        #     if db.check_dates(message.from_user.id) is not None:
        #         database_date_obj = datetime.strptime(db.check_dates(message.from_user.id), '%Y-%m-%d %H:%M:%S.%f')
        #         if current_date > database_date_obj:
        #             # эта функция если прошла подписка
        #             db.del_dates(message.from_user.id)
        #             if cfg.PAYMENTS_TOKEN.split(':') == 'TEST':
        #                 await message.answer("Тестовый платёж")


        #             await bot.send_invoice(message.chat.id,
        #                                 title="Подписка на бота",
        #                                 description="Активация подписки на бота на 1 день!",
        #                                 provider_token=cfg.PAYMENTS_TOKEN,
        #                                 currency='rub',
        #                                 photo_url="https://cdn.xxl.thumbs.canstockphoto.ru/%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D0%B0-%D0%BA%D0%B0%D1%80%D1%82%D0%B0-%D1%81%D1%82%D0%BE%D0%BA%D0%BE%D0%B2%D0%B0%D1%8F-%D1%84%D0%BE%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F_csp5148789.jpg",
        #                                 photo_width=360,
        #                                 photo_height=254,
        #                                 is_flexible=False,
        #                                 prices=[PRICE],
        #                                 start_parameter='one-day-subscription',
        #                                 payload='test-invoice-payload')
        #         elif current_date < database_date_obj:
        #             # кнопки поиск мужчины или женщины если есть подписка
        #             markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        #             button1 = types.KeyboardButton(cfg.SEARCH_MALE_MALE)
        #             button2 = types.KeyboardButton(cfg.SEARCH_MALE_FEMALE)
        #             button3 = types.KeyboardButton(cfg.BACK)
        #             markup.add(button1, button2, button3)
        #             await message.answer(cfg.BUTTON_MALE_TEXT, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
        #             await search_male.buttons_search.set()
        #     else:
        #         if cfg.PAYMENTS_TOKEN.split(':') == 'TEST':
        #             await message.answer("Тестовый платёж")


        #         await bot.send_invoice(message.chat.id,
        #                                title="Подписка на бота",
        #                                description="Активация подписки на бота на 1 день!",
        #                                provider_token=cfg.PAYMENTS_TOKEN,
        #                                currency='rub',
        #                                photo_url="https://cdn.xxl.thumbs.canstockphoto.ru/%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D0%B0-%D0%BA%D0%B0%D1%80%D1%82%D0%B0-%D1%81%D1%82%D0%BE%D0%BA%D0%BE%D0%B2%D0%B0%D1%8F-%D1%84%D0%BE%D1%82%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%8F_csp5148789.jpg",
        #                                photo_width=360,
        #                                photo_height=254,
        #                                is_flexible=False,
        #                                prices=[PRICE],
        #                                start_parameter='one-day-subscription',
        #                                payload='test-invoice-payload')



# @dp.pre_checkout_query_handler(lambda query: True)
# async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

# @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
# async def successful_payment(message: types.Message):
#     print("SUCCESSFUL PAYMENT:")
#     payment_info = message.successful_payment.to_python()
#     for k, v in payment_info.items():
#         print(f"{k} = {v}")

    # {message.successful_payment.total_amount // 100} {message.successful_payment.currency}
    # if db.check_dates(message.from_user.id) is not None:
    #     # current_date = db.check_dates(message.from_user.id)
    #     database_date_obj = datetime.strptime(db.check_dates(message.from_user.id), '%Y-%m-%d %H:%M:%S.%f')
    #     next_day = database_date_obj + timedelta(days=1)
    #     db.update_dates(message.from_user.id, next_day)
    #     await bot.send_message(message.chat.id, f"Вы успешно продлили подписку на 1 день!")
    # else:
    #     current_date = datetime.now()
    #     next_day = current_date + timedelta(days=1)
    #     db.add_dates(message.from_user.id, next_day)
    #     await bot.send_message(message.chat.id, f"Вы успешно приобрели подписку на 1 день!")

# @dp.message_handler(content_types=['text'], state=search_male.buttons_search)
# async def search_buttons(message: types.Message, state: FSMContext):
#     if message.chat.type == types.ChatType.PRIVATE:
#         if message.text == cfg.BACK:
#             markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#             button1 = types.KeyboardButton(cfg.SEARCH)
#             button2 = types.KeyboardButton(cfg.SEARCH_MALE)
#             markup.add(button1, button2)
#             await message.answer(cfg.BACK_TEXT, reply_markup=markup, parse_mode=types.ParseMode.MARKDOWN)
#             await state.finish()