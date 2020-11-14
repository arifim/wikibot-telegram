import telebot
from telebot import types
import wikipedia

CHAT_ID = None
SAD_FACE = '😔'
USA_FLAG = '🇺🇸'
RUS_FLAG = '🇷🇺'

bot = telebot.TeleBot(token=MY_TOKEN)

buttons = types.InlineKeyboardMarkup(row_width=1)
btn_en = types.InlineKeyboardButton(text='English', callback_data='en')
btn_ru = types.InlineKeyboardButton(text='Русский', callback_data='ru')
buttons.add(btn_en, btn_ru)

@bot.message_handler(commands=['start', 'help', 'lang'])
def command_habdler(message):
    CHAT_ID = message.chat.id
    if message.text == '/start':
        bot.send_message(chat_id=CHAT_ID, text='Hello. This is WikiBot. I can search articles in wikipedia')
    elif message.text == '/help':
        bot.send_message(chat_id=CHAT_ID, text='At this time I cannot help you, but I will try next time')
    elif message.text == '/lang':
        bot.send_message(chat_id=CHAT_ID, text='Chose language', reply_markup=buttons).text
       

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    try:
        message_id = bot.send_message(chat_id=message.chat.id, text='Please wait. I am searching...').message_id
        try:
            page = wikipedia.page(message.text)
        except wikipedia.exceptions.DisambiguationError:
            bot.delete_message(chat_id=message.chat.id, message_id=message_id)
            bot.send_message(chat_id=message.chat.id, text='I found several articles. Which one are u looking for?')
            bot.send_message(chat_id=message.chat.id, text='https://en.wikipedia.org/wiki/' + message.text)
        except wikipedia.PageError:
            bot.delete_message(chat_id=message.chat.id, message_id=message_id)
            bot.send_message(chat_id=message.chat.id, text="There is no any page that match you query " + SAD_FACE)
        else:
            bot.delete_message(chat_id=message.chat.id, message_id=message_id)
            bot.send_message(chat_id=message.chat.id, text=page.title + '\n' + page.summary[0:512] + '...' + '\n' + page.url)
    except telebot.apihelper.ApiException:
        print("API exception")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    wikipedia.set_lang(call.data)
    bot.answer_callback_query(call.id, 
                            text=USA_FLAG + " Language setting update" if call.data == 'en' else RUS_FLAG + " Настройки языка обновены")
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

bot.polling()
