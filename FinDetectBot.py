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
first_row = results[0]
print( (first_row.title), '\n')


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
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Список финансовых организаций")
    item2 = types.KeyboardButton("Проверить URL")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}.\n' +
                                      'Данный сервис позволяет:\n\n'
                                      '1) проверить на доступность различные финансовые организации;\n\n'
                                      '2) проверить URL на фишинг.\n\nВыберите финансовую организацию'
                                      ', чтобы узнать ее статус.\nВыберите проверку URL, '
                                      'чтобы проверить оригинальность URL финансовой организации.', reply_markup=markup)

# Функция, обрабатывающая команду /shownames
@bot.message_handler(commands=["shownames"])
def shownames(message, res=False):
    keyboard = types.InlineKeyboardMarkup()
    button_list = (types.InlineKeyboardButton(text="АкБарсБанк", callback_data="АкБарс"),
                   types.InlineKeyboardButton(text="Сбербанк", callback_data="Сбербанк"),
                   types.InlineKeyboardButton(text="Тинькофф", callback_data="Тинькофф"),
                   types.InlineKeyboardButton(text="Открытие", callback_data="Открытие"))
    keyboard.add(*button_list)
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

def checkurlparce(message, res=False):
    message.text
    bot.send_message(message.chat.id, "URL подтвержден.")

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text == 'Список финансовых организаций':
        shownames(message)
    elif message.text == 'Проверить URL':
        checkurl(message)
    elif 'url' in message.text.lower():
        message_list = message.text.split(' ')
        for i in message_list:
            if i == ' ':
                message_list.pop(i)
                i -= 1
        if len(message_list) != 2:
            bot.send_message(message.chat.id, f'Некорректный формат сообщения для проверки URL')
        else:
            checkurlparce(message)
    else:
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')

# Запускаем бота
bot.polling(none_stop=True, interval=0)
