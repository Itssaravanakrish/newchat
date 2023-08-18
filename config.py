TOKEN = "5815738068:AAH0CLsYyazHP9XgR_1b66pYh02kXMsgxxM"

def ERROR_REGISTER():
    return "_You must select a gender to communicate with people.\nIf you encounter any error, enter the /register command_\n\n_Вы должны выбрать пол, для общения с людьми.\nЕсли у вас возникла какая то ошибка, вводите команду /register_\n\n_Մարդկանց հետ շփվելու համար դուք պետք է ընտրեք ձեր սեռը:\Եթե ունեք որևէ սխալ, մուտքագրեք /register հրամանը:_"

def START(language):
    if language == 0:
        return "_Hello! Welcome to the anonymous chat.\nTo find someone, type /search, or click the button below._"
    elif language == 1:
        return "_Привет! Добро пожаловать в анонимный чат.\nДля того чтобы найти собеседника, напишите /search, или нажмите на кнопку ниже._"
    elif language == 2:
        return "_Ողջույն: Բարի գալուստ անանուն զրույց:\nԻնչ-որ մեկին գտնելու համար մուտքագրեք /search կամ սեղմեք ներքևի կոճակը:_"

def SEARCH(language):
    if language == 0:
        return "👫 Start a conversation"
    elif language == 1:
        return "👫 Начать диалог"
    elif language == 2:
        return "👫 Սկսել զրույց"


def STOP_SEARCH(language):
    if language == 0:
        return "❌ Cancel search"
    elif language == 1:
        return "❌ Отменить поиск"
    elif language == 2:
        return "❌ Չեղարկել որոնումը"

def CORRECT_MY_LINK(language):
    if language == 0:
        return "_You have successfully given your telegram account to your interlocutor ✔_"
    elif language == 1:
        return "_Вы успешно дали свой телеграм аккаунт вашему собеседнику ✔_"
    elif language == 2:
        return "«_Դուք հաջողությամբ փոխանցել եք ձեր telegram-ը զրուցակցին ✔_»"

def SEARCH_PROCESS(language):
    if language == 0:
        return "_⌛ Looking for a companion..._"
    elif language == 1:
        return "_⌛ Идёт поиск собеседника..._"
    elif language == 2:
        return "_⌛ Ուղեկից եմ փնտրում..._"

def STOP_SEARCH_TEXT(language):
    if language == 0:
        return "_You have successfully canceled the search for a companion ✔_"
    elif language == 1:
        return "_Вы успешно отменили поиск собеседника ✔_"
    elif language == 2:
        return "_Դուք հաջողությամբ չեղարկել եք ուղեկիցի որոնումը ✔_"

def SEARCH_TRUE(language):
    if language == 0:
        return """_Interlocutor found 🦊\n\n/next - search for a new interlocutor\n/stop - stop dialogue_\n/link - send your telegram\n\n`https://t.me/AnonymChatyBot`"""
    elif language == 1:
        return """_Собеседник найден 🦊\n\n/next - искать нового собеседника\n/stop - остановить диалог_\n/link - отправить свой телеграм\n\n`https://t.me/AnonymChatyBot`"""
    elif language == 2:
        return """_Գտնվել է զրուցակիցը 🦊\n\n/next - որոնել նոր զրուցակից\n/stop - դադարեցնել երկխոսությունը_\n/link - ուղարկել ձեր telegram-ը\n\n`https://t.me/AnonymChatyBot`"""

def STOP_DIALOG_TEXT(language):
    if language == 0:
        return "You have finished the dialogue with the interlocutor.\To find the interlocutor, type /search_"
    elif language == 1:
        return "_Вы закончили диалог с собеседником.\nДля того чтобы найти собеседника, напишите /search_"
    elif language == 2:
        return "_Դուք ավարտել եք երկխոսությունը զրուցակցի հետ։\Զրուցակցին գտնելու համար մուտքագրեք /search_"

def SEARCH_DRUGOGO_TEXT(language):
    if language == 0:
        return "_You have finished the dialogue with the interlocutor and have begun the search for a new interlocutor._"
    elif language == 1:
        return "_Вы закончили диалог с собеседником и начали поиск нового собеседника._"
    elif language == 2:
        return "_Դուք ավարտել եք երկխոսությունը զրուցակցի հետ և սկսել եք նոր զրուցակցի փնտրտուքները:"

def STOP_DIALOG_TEXT_SOBESEDNIK(language):
    if language == 0:
        return "_Your interlocutor has finished the dialogue with you.\To find the interlocutor, type /search_"
    elif language == 1:
        return "_Ваш собеседник закончил с вами диалог.\nДля того чтобы найти собеседника, напишите /search_"
    elif language == 2:
        return "_Ձեր զրուցակիցն ավարտել է երկխոսությունը ձեզ հետ։\nԶրուցակցին գտնելու համար մուտքագրեք /search_"

def CANCEL_STOP_DIALOG_TEXT(language):
    if language == 0:
        return "_❌ You are not looking for_"
    elif language == 1:
        return "_❌ Вы не находитесь в поиске_"
    elif language == 2:
        return "_❌ Դուք չեք փնտրում_"

def CANCEl_STOP_SEARCH_TEXT(language):
    if language == 0:
        return "_❌ You are not in dialogue_"
    elif language == 1:
        return "_❌ Вы не находитесь в диалоге_"
    elif language == 2:
        return "_❌ Դուք երկխոսության մեջ չեք_"

def CANCEL_TEXT(language):
    if language == 0:
        return "_❌ You are in a dialogue._"
    elif language == 1:
        return "_❌ Вы находитесь в диалоге._"
    elif language == 2:
        return "_❌ Դու երկխոսության մեջ ես:_"

def CANCEL_SEARCH_PROCESS(language):
    if language == 0:
        return "_❌ You are in search._"
    elif language == 1:
        return "_❌ Вы находитесь в поиске._"
    elif language == 2:
        return "_❌ Դուք որոնումների մեջ եք։_"


def BOT_BLOCKED(language):
    if language == 0:
        return "_Correspondence with the interlocutor is over, your interlocutor has blocked the bot ❌_"
    elif language == 1:
        return "_Переписка с собеседником закончена, ваш собеседник заблокировал бота ❌_"
    elif language == 2:
        return "_Զրուցակցի հետ նամակագրությունն ավարտված է, ձեր զրուցակիցն արգելափակել է բոտը ❌_"

def CANCEL_TEXT_BOT(language):
    if language == 0:
        return "_Type /search to search for a friend_"
    elif language == 1:
        return "_Напишите /search чтобы искать собеседника_"
    elif language == 2:
        return "_Մուտքագրեք /search ընկեր փնտրելու համար_"



def LANGUAGE_CORRECT_TEXT(language):
    if language == 0:
        return "You have successfully selected English"
    elif language == 1:
        return "Вы успешно выбрали русский язык"
    elif language == 2:
        return "Դուք հաջողությամբ ընտրել եք հայերենը"

def CANCEL_DOCUMENT_TEXT(language):
    if language == 0:
        return "_You can only send text or photo!_"
    elif language == 1:
        return "_Вы можете отправить только текст или фото!_"
    elif language == 2:
        return "_Դուք կարող եք ուղարկել միայն տեքստ կամ լուսանկար:"

def LINK(language, links):
    if language == 0:
        return f"The interlocutor sent you a {links} of his telegram account"
    elif language == 1:
        return f"Собеседник отправил вам {links} своего телеграм аккаунта"
    elif language == 2:
        return f"Զրուցակիցը ձեզ ուղարկել է իր telegram-ի {links}"

def LINK_SSILKA(language):
    if language == 0:
        return "link"
    elif language == 1:
        return "ссылку"
    elif language == 2:
        return "հղումը"


def ERROR_DOCUMENT(language):
    if language == 0:
        return "An error occurred, this file cannot be sent"
    elif language == 1:
        return "Произошла ошибка, данный файл нельзя отправить"
    elif language == 2:
        return "Սխալ է տեղի ունեցել, այս ֆայլը չի կարող ուղարկվել"

def SETTINGS(language):
    if language == 0:
        return "🔧 Settings"
    elif language == 1:
        return "🔧 Настройки"
    elif language == 2:
        return "🔧 Կարգավորումներ"

def CHANGE_LANGUAGE(language):
    if language == 0:
        return "♻️Change language"
    elif language == 1:
        return "♻️Поменять язык"
    elif language == 2:
        return "♻️Փոխել լեզուն"

def BACK(language):
    if language == 0:
        return "🔙 Back"
    elif language == 1:
        return "🔙 Назад"
    elif language == 2:
        return "🔙 Վերադառնալ"

def SELECT_SETTINGS_TEXT(language):
    if language == 0:
        return "Choose the appropriate option:"
    elif language == 1:
        return "Выберите подходящую опцию:"
    elif language == 2:
        return "Ընտրեք համապատասխան տարբերակը:"

def SELECT_LANGUAGE_TEXT(language):
    if language == 0:
        return "Select the language you want to change to."
    elif language == 1:
        return "Выберите язык, на которую хотите поменять."
    elif language == 2:
        return "Ընտրեք այն լեզուն, որին ցանկանում եք փոխել:"

def BACK_TEXT(language):
    if language == 0:
        return "You are back."
    elif language == 1:
        return "Вы вернулись назад."
    elif language == 2:
        return "Դու վերադարձար:"

def SELECT_SETTINGS_CORRECT(language):
    if language == 0:
        return "You have selected an option."
    elif language == 1:
        return "Вы выбрали опцию."
    elif language == 2:
        return "Դուք ընտրել եք տարբերակ:"
