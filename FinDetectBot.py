import telebot
from telebot import types
import sys
import locale

import sqlalchemy as db


print(sys.getfilesystemencoding())
print(locale.getpreferredencoding())

engine = db.create_engine('sqlite:///FinDetect.db')
connection = engine.connect()

print(engine.table_names(), '\n')

metadata = db.MetaData()
census = db.Table('Service', metadata, autoload=True, autoload_with=engine)
print(repr(census), '\n')

result_proxy = connection.execute("SELECT title FROM Service")
results = result_proxy.fetchall()
titles = []
for k in results:
    titles.append(*k)
    print(*k)
print(titles)

result_proxy2 = connection.execute("SELECT url FROM Service")
results2 = result_proxy2.fetchall()
url = []
for k in results2:
    url.append(*k)
    print(*k)
print(url)


result_proxy3 = connection.execute("SELECT site_available FROM Service")
results3 = result_proxy3.fetchall()
available = []
for k in results3:
    available.append(*k)
    print(*k)

#print(census.columns.keys())
#query = db.select([census])
#print(query)

#results = connection.execute(db.select([census])).fetchall()
#print(results)

# ResultProxy = connection.execute(query)
# ResultSet = ResultProxy.fetchall()
# print(*ResultSet)


# Создаем экземпляр бота
bot = telebot.TeleBot('5360323055:AAEMToeoFLN-OeWPF4RDmK8rkRy9y17bAuU')

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    keyboard = types.InlineKeyboardMarkup()
    button_list = (types.InlineKeyboardButton(text="Список финансовых организаций", callback_data="Список финансовых организаций"),
                   types.InlineKeyboardButton(text="Сайт FinDetect", url="http://188.120.237.48:5000/"))
    keyboard.add(*button_list)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}.\n' +
                                      'Данный сервис позволяет:\n\n'
                                      '1) проверить на доступность различные финансовые организации;\n\n'
                                      '2) проверить URL на фишинг.\n\nВыберите финансовую организацию'
                                      ', чтобы узнать ее статус.\n\nВведите URL, '
                                      'чтобы проверить оригинальность URL финансовой организации.', reply_markup=keyboard)

# Функция, обрабатывающая команду /shownames
@bot.message_handler(commands=["shownames"])
def shownames(message, res=False):
    global titles

    keyboard = types.InlineKeyboardMarkup()
    for l in titles:
        keyboard.add(types.InlineKeyboardButton(text=l, callback_data=l))

    bot.send_message(message.chat.id, "Выберите финансовую организацию:", reply_markup=keyboard)

# Функция, обрабатывающая команду /checkurl
@bot.message_handler(commands=["checkurl"])
def checkurl(message, res=False):
    bot.send_message(message.chat.id, "Для проверки подлинности URL финансовой организации "
                                      "введите сообщение в формате:\n\n url: <url финансовой организации>")

# Функция, обрабатывающая команду /restart
@bot.message_handler(commands=["restart"])
def restart(message):
    start(message)

# Функция, обрабатывающая команду /site
@bot.message_handler(commands=["site"])
def site(message, res=False):
    keyboard = types.InlineKeyboardMarkup()
    button_list = (types.InlineKeyboardButton(text="Сайт FinDetect", url="http://188.120.237.48:5000/"))
    keyboard.add(button_list)
    bot.send_message(message.chat.id, 'Посетите сайт FinDetect:', reply_markup=keyboard)

# Функция, обрабатывающая команду /help
@bot.message_handler(commands=["help"])
def help(message, res=False):
    keyboard = types.InlineKeyboardMarkup()
    button_list = (types.InlineKeyboardButton(text="Список финансовых организаций", callback_data="Список финансовых организаций"))
    keyboard.add(button_list)
    bot.send_message(message.chat.id, 'Чтобы проверить на доступность финансовую организацию, '
                                      'введите название данной организации или выберите интересующую'
                                      'финансовую организацию из списка:', reply_markup=keyboard)
    bot.send_message(message.chat.id, '\nДля проверки подлинности URL финансовой организации '
                                      'введите URL. Например, https://www.akbars.ru', disable_web_page_preview = True)

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global url, titles
    print("CHECK@")

    print(message.text.lower())
    if ('https://' in message.text.lower()):
        print(message.text.lower(),'-----------------------111111111111111111')
    else:
        print(message.text.lower(),'----------------------2222222222222222')

    for i in range(len(titles)):
        print(message.text, url[i], (url[i]).replace('www.',''))
        if (message.text == url[i]) or ((url[i] + '/') in message.text) or (message.text == (url[i]).replace('www.','')):
            print("++++")
        else:
            print("---")

    if message.text.lower() == 'cписок финансовых организаций':
        shownames(message)
    elif message.text.lower() == 'проверить url':
        bot.send_message(message.chat.id, '\nДля проверки подлинности URL финансовой организации '
                                          'введите URL. Например, https://www.akbars.ru', disable_web_page_preview=True)
    elif ('http://' in message.text.lower()) or ('https://' in message.text.lower()):
        for i in range(len(titles)):
            if (message.text == url[i]) or ((url[i] + '/') in message.text) or (message.text == (url[i]).replace('www.','')):
                bot.send_message(message.chat.id, f"URL {titles[i]} подтвержден\nURL : {url[i]}")
                break
                return 0
            else:
                bot.send_message(message.chat.id, f"URL не потверждён")
                break
                return 0
            i += 1
    elif (message.text.lower() == 'сайт') or ('findetect' in message.text.lower()):
        site(message)
    else:
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, я вас не понял.\n1. Проверить доступность сервиса: нажмите на кнопку, выберите из списка\n2. Проверить оригинальность URL : введите URL <https://example.com> ')


def checkurlparce(message, res=False):
    global url, titles
    print("CHECK")
    for i in range(len(titles)):
        if message.text == url[i] or (url[i] + '/') in message.text:
            bot.send_message(message.chat.id, f"URL {titles[i]} подтвержден\nURL : {url[i]}")

# Обработчик callback'ов
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global titles, url, available

    for p in range(len(titles)):
        print(p)
        if call.data == titles[p]:
            if (available[p] == 1):
                bot.send_message(call.message.chat.id, f'Сервис : {titles[p]}\nДоступность : доступен \nURL : {url[p]}',parse_mode='HTML')
            if (available[p] == 0):
                bot.send_message(call.message.chat.id, f'Сервис : {titles[p]}\nДоступность : не доступен \nURL : {url[p]}',parse_mode='HTML')
            
            # photo = open('./static/img/ON2.png', 'rb')
            # bot.send_photo(call.message.chat.id, photo)
            # file_id = 'AAAaaaZZZzzz'
            # bot.send_photo(call.message.chat.id, file_id)
            # # bot.send_image(call.message.chat.id, '/static/img/ON.svg')

    if call.data == "АкБарс":
        bot.send_message(call.message.chat.id, "АкБарс")
    # elif call.data == "Сбербанк":
    #     bot.send_message(call.message.chat.id, "Сбербанк")
    # elif call.data == "Тинькофф":
    #     bot.send_message(call.message.chat.id, "Тинькофф")
    # elif call.data == "Открытие":
    #     bot.send_message(call.message.chat.id, "Открытие")
    elif call.data == "Список финансовых организаций":
        shownames(call.message)

# Запускаем бота
bot.polling(none_stop=True, interval=0)