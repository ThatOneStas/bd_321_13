import telebot
from telebot import types
import requests
import json

baseURL = "https://bank.gov.ua/NBUStatService/v1"
currency_data = []

bot = telebot.TeleBot("6433719050:AAE6tnR7jOSBza4uelfvAW5JTYmQW-GiAk8")

print('_____ START BOT _____')

counters = {
    "menu": 0,
    "admins": [6269605642],
    "admin": False
}
converter_data = {
    "curr": '',
    "amount": 0
}
users = {}

def save_user(cid):
    with open("users.json", 'r') as file:
        Users = json.load(file)

    if cid not in Users:
        Users.append(cid)

    with open('users.json', 'w') as f:
        json.dump(Users, f)

def getDataCurrency():
    LINK = f"{baseURL}/statdirectory/exchange?json"
    resp = requests.get(LINK)
    DATA = resp.json()
    for i in DATA:
        currency_data.append(i)

def set_choice_currency(msg):
    converter_data["curr"] = msg.text
    cid = msg.chat.id
    mess = bot.send_message(cid, "Введіть сумму для обміну:")
    bot.register_next_step_handler(mess, set_amount)



def total_price(cid):
    baseURL = "https://fakestoreapi.com"
    if __name__ == "__main__":
        response = requests.get(f"{baseURL}/products")
        data = response.json()
        total_price = 0
        for i in data:
            total_price += i['price']
        bot.send_message(cid, total_price, reply_markup=second_reply_menu())

def set_amount(msg):
    converter_data["amount"] = msg.text
    curr_obj = None
    for item in currency_data:
        if item['txt'] == converter_data['curr']:
            curr_obj = item.copy()
            break
    print(curr_obj)

    result = float(converter_data["amount"]) / float(curr_obj["rate"])
    result = round(result, 2)
    txt = f"{result} {curr_obj['cc']}"
    bot.send_message(msg.chat.id, txt, reply_markup=second_reply_menu())
### REPLY KEYBOARD

def main_reply_menu(cid):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('💡Ask me'), types.KeyboardButton('Next'))
    markup.row(types.KeyboardButton('InlineMenu'))
    markup.row(types.KeyboardButton('/start'), types.KeyboardButton('/update'), types.KeyboardButton("/spam"))
    if cid in counters['admins']:
        markup.row(types.KeyboardButton('Admin'))
        counters["admin"] = True

        print(counters["admin"])

    return markup

def second_reply_menu():
    markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup_2.row(types.KeyboardButton('Price'), types.KeyboardButton('Convertor'))
    markup_2.row(types.KeyboardButton('back'))
    return markup_2

def currency_reply_menu():
    markup_3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    counter = 0
    buttons = []
    for curr in currency_data:
        counter += 1
        btn = types.KeyboardButton(curr['txt'])
        buttons.append(btn)
        if counter == 3:
            markup_3.row(buttons[0],buttons[1])
            counter = 0
            buttons = []
    return markup_3

### INLINE MENU

def get_user_name(msg):
    cid = msg.chat.id
    txt = msg.text
    users[f'{cid}'] = {}
    users[f'{cid}']['name'] = txt
    mess = bot.send_message(cid, 'Input your age: ')
    bot.register_next_step_handler(mess, get_user_age)

def get_user_age(msg):
    cid = msg.chat.id
    txt = msg.text
    users[f"{cid}"]["age"] = txt
    msg_text = f'Name: {users[f"{cid}"]["name"]} \n' \
               f'Age: {users[f"{cid}"]["age"]}'
    bot.send_message(cid, msg_text, reply_markup=main_reply_menu(cid))


@bot.message_handler(commands=['admin'])
def admins(msg):
    cid = msg.chat.id
    if cid in admins:
        bot.send_message(cid, "Hello admin!")
    else:
        bot.send_message(cid, "Not allowed")
@bot.message_handler(commands=['spam'])
def send_spam(msg):
    with open("users.json", 'r') as file:
        users = json.load(file)

    for id in users:
        try:
            bot.send_message(id, "👋")
        except Exception as err:
            print(err)
@bot.message_handler(commands=['start'])
def send_welcome(msg):
    cid = msg.chat.id
    temp_text = '<u>Test</u>'
    bot.send_message(cid, temp_text, reply_markup=main_reply_menu(cid), parse_mode='html')
    print(msg.chat.id)

@bot.message_handler(commands=['update'])
def some_msg(msg):
    cid = msg.chat.id
    bot.reply_to(msg, "Update✅", reply_markup=main_reply_menu(cid), parse_mode='html')

@bot.message_handler(func=lambda message: True)
def echo_all(msg):
    cid = msg.chat.id

    if msg.text == 'Next' and counters['menu'] == 0:
        bot.send_message(cid, 'Done✅', reply_markup=second_reply_menu())
        counters['menu'] += 1
    elif msg.text == 'main':
        bot.send_message(cid, "Returned to main✅", reply_markup=main_reply_menu(cid))
        counters['menu'] -= counters['menu']
    elif msg.text == 'back' and counters['menu'] == 1:
        bot.send_message(cid, "Returned back✅", reply_markup=main_reply_menu(cid))
        counters['menu'] -= counters['menu']
    elif msg.text == 'back' and counters['menu'] == 2:
        bot.send_message(cid, "Returned back✅", reply_markup=second_reply_menu())
        counters['menu'] -= 1

    elif msg.text == '💡Ask me':
        mess = bot.send_message(cid, 'Input your name: ')
        bot.register_next_step_handler(mess, get_user_name)
    elif msg.text == 'Price':
        total_price(cid)
    elif msg.text == 'Convertor':
        getDataCurrency()
        mess = bot.send_message(cid, "Оберіть валюту:", reply_markup=currency_reply_menu())
        bot.register_next_step_handler(mess, set_choice_currency)

    elif msg.text == 'Admin':
        if counters["admin"] == True:
            bot.send_message(cid, 'Welcome Admin!', reply_markup=main_reply_menu(cid))
        else:
            bot.send_message(cid, 'Error 418', reply_markup=main_reply_menu(cid))


bot.infinity_polling()