import telebot
from config import keys, TOKEN
from extension import ConvertionException, CurrencyConverter
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help (message: telebot.types.Message):
    text= "Вас приветствует  ConvertCurrencyBot.\
          Чтобы начать работу введите команду в\
          следующем формате:\
          \n<имя валюты которую необходимо перевести>\
           <в какую валюту перевести>\
           <количество переводимой валюты>\
          \nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values (message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Проверьте количество параметров')

        base, quote, amount = values
        total_base = CurrencyConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка в команде:\n {e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Неизвестная ошибка:\n {e}')
    else:
        total_base = float(total_base)
        amount = float(amount)
        text = f'Конвертация {amount} {base} в {quote}-{round(total_base*amount,3)}'
        bot.send_message(message.chat.id, text)


bot.polling()


