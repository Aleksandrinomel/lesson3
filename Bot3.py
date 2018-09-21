from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, RegexHandler, Filters
import settings
import ephem
import re
import datetime
import ast
from telebot import types
from telegram import KeyboardButton, ReplyKeyboardMarkup



# обрабатывает команду бота /planet и выводит созвездие, в котором сейчас находится планета
def greet_user(bot, update):
    if update.message.text.split()[0] == '/planet':
        now = datetime.datetime.now()
        planet_is = 'ephem.' + update.message.text.split()[1] + "('" + str(now) + "')"
        constell = ephem.constellation(eval(planet_is))
        update.message.reply_text(
            'Планета ' + update.message.text.split()[1] + ' сейчас находится в созвездии ' + constell[1])


# обрабатывает команду бота /wordcount и выводит кол-во слов, находящихся в ""
def count_word(bot, update):
    text = re.sub('\/wordcount |\=|\-|\,|\.|\(|\)|\!|\?', '', update.message.text)

    if text[0] == '"' and text[-1] == '"':
        count_words = len(text.strip('"').split())
        update.message.reply_text('Количество слов: ' + (str(count_words)))
    else:
        update.message.reply_text('Текст должен быть в ""')


# обрабатывает команду бота /calc и выводит результат простого выражения
def calc(bot, update):
    if update.message.text[-1] == '=':
        expression = re.sub('\/calc |\=|\ ', '', update.message.text)
        list_numbers = list(re.split("[+-/*]+", expression))
        try:
            if '+' in expression:
                update.message.reply_text(str(int(list_numbers[0]) + int(list_numbers[1])))
            elif '-' in expression:
                update.message.reply_text(str(int(list_numbers[0]) - int(list_numbers[1])))
            elif '/' in expression:
                try:
                    update.message.reply_text(str(int(list_numbers[0]) / int(list_numbers[1])))
                except ZeroDivisionError:
                    update.message.reply_text('На ноль делить нельзя')
            elif '*' in expression:
                update.message.reply_text(str(int(list_numbers[0]) * int(list_numbers[1])))
        except ValueError:
            update.message.reply_text('Проверьте правильность написания и наличие чисел')


# клавиатура для калькулятора
def start_keyboard(bot, update):
    keyboard = [[KeyboardButton("1"),
                 KeyboardButton("2"),
                 KeyboardButton("3"),
                 KeyboardButton("+")],
                [KeyboardButton("4"),
                 KeyboardButton("5"),
                 KeyboardButton("6"),
                 KeyboardButton("-")],
                [KeyboardButton("7"),
                 KeyboardButton("8"),
                 KeyboardButton("9"),
                 KeyboardButton("*")],
                [KeyboardButton("0"),
                 KeyboardButton("00"),
                 KeyboardButton("/"),
                 KeyboardButton("=")]
                ]


    reply_markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text("Калькулятор", reply_markup=reply_markup)


# калькулятор
expression = ''
def keyboard_calc(bot, update):
    if update.message.text != '=':
        global expression
        expression += update.message.text
    else:
        list_numbers = list(re.split("[+-/*]+", expression))
        try:
            if '+' in expression:
                update.message.reply_text(str(int(list_numbers[0]) + int(list_numbers[1])))
            elif '-' in expression:
                update.message.reply_text(str(int(list_numbers[0]) - int(list_numbers[1])))
            elif '/' in expression:
                try:
                    update.message.reply_text(str(int(list_numbers[0]) / int(list_numbers[1])))
                except ZeroDivisionError:
                    update.message.reply_text('На ноль делить нельзя')
            elif '*' in expression:
                update.message.reply_text(str(int(list_numbers[0]) * int(list_numbers[1])))
        except ValueError:
            update.message.reply_text('Проверьте правильность написания и наличие чисел')
        expression = ''


# переводит слова в арифметическое выражение и вычисляет его
def lexical_calc(bot, update):
    if 'сколько будет' in update.message.text:
        digits = {'ноль': 0, 'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5, 'шесть': 6, 'семь': 7, 'восемь': 8, 'девять': 9}
        text = update.message.text.replace('на', '').split()
        print(text)
        digit1 = text[2]
        digit2 = text[4]
        if text[3] == 'минус':
            update.message.reply_text(digits[digit1] - digits[digit2])
        elif text[3] == 'плюс':
            update.message.reply_text(digits[digit1] + digits[digit2])
        elif text[3] == 'умножить':
            update.message.reply_text(digits[digit1] * digits[digit2])
        elif text[3] == 'разделить':
            update.message.reply_text(digits[digit1] / digits[digit2])


# отвечает на вопрос: 'Когда ближайшее полнолуние после ...'
def full_moon(bot, update):
    if 'Когда ближайшее полнолуние после' in update.message.text:
        text = update.message.text.strip('?').replace('-','/').split()
        update.message.reply_text('Следующее новолуние будет: ' + str(ephem.next_full_moon(text[4])))


# города
list_city = ['Москва', 'Астрахань', 'Адам', 'Милан', 'Новгород', 'Дмитров']
def goroda(bot, update):
    city = update.message.text.split()[1]
    if city[-1] == 'ь':
        litera = city[-2]
    else:
        litera = city[-1]
    if city in list_city:
        i = list_city.index(city)
        list_city.pop(i)
        for gorod in list_city:
            if gorod.lower()[0] == litera:
                ind = list_city.index(gorod)
                update.message.reply_text(list_city.pop(ind))
                break
        print(list_city)
    else:
        update.message.reply_text('Такого города нет в списке')

# возвращает список городов к исходному значению
def re_goroda(bot, update):
    global list_city
    list_city = ['Москва', 'Астрахань', 'Адам', 'Милан', 'Новгород', 'Дмитров']







def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('key', start_keyboard))
    dp.add_handler(CommandHandler('wordcount', count_word))
    dp.add_handler(CommandHandler('planet', greet_user))
    dp.add_handler(CommandHandler('calc', calc))
    dp.add_handler(CommandHandler('goroda', goroda))
    dp.add_handler(CommandHandler('re_goroda', re_goroda))
    dp.add_handler(RegexHandler('^(1|2|3|4|5|6|7|8|9|0|00|-|=|\+|\*|\/)$', keyboard_calc))
    dp.add_handler(MessageHandler(Filters.text, full_moon))
    dp.add_handler(MessageHandler(Filters.text, lexical_calc))



    mybot.start_polling()
    mybot.idle()

main()
