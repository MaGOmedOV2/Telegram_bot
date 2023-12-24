import telebot
from extensions import ConvertionException, APIException
from config import key, TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands= ['start'])
def echo_test(message: telebot.types.Message):
    text = "Привет этот бот может переводить валюты. \nесли хотите начать работу с ботом, то напищите команду следующим образом:\n<имя валюты> \n<имя валюты в которую хотите перевести> \n<количество валюты> \nсписок доступных команд открывается при введении команды: /value"
    bot.reply_to(message, text)


@bot.message_handler(commands= ['help'] )
def help(message: telebot.types.Message):
    text = "Чтобы начать работать с ботом введите команду боту следующим способом: \n<имя валюты> \n<имя валюты в которую хотите перенести> \n<количество валюты> \nсписок доступных команд открывается при введении команды: /value"
    bot.reply_to(message, text)


@bot.message_handler(commands= ['value'])
def value(message: telebot.types.Message,):
    text = "Доступные валюты:"
    for keys in key.keys():
        text = '\n'.join((text, keys))
    bot.reply_to(message, text)


@bot.message_handler(content_types= ['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvertionException('Слишком много параметров.')

        elif len(values) != 3:
            raise ConvertionException('Слишком мало параметров')

        base, quote, amound = values
        total_base = APIException.get_price(base,quote, amound)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n {e}')
    else:
        text = f"Цена {amound} {base} в {quote} - {total_base * int(amound)}"
        bot.send_message(message.chat.id, text)

bot.polling()