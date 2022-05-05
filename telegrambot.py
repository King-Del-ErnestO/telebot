import telebot
import yfinance as yf

api_key = '5372043296:AAEMGZteUphHx9ltFpAOVfSuVqWZHEDpXA8'
bot = telebot.TeleBot(api_key)

@bot.message_handler(commands=['greet'])

def greet(message):
    bot.reply_to(message, 'Hey, How are you doing?')

@bot.message_handler(commands=['examples'])

def examples(message):
    response = ''
    stock_df = {'APPLE':'APPL', 'AMAZON': 'AMZN', 'FACEBOOK': 'FB', 'TESLA': 'TSLA', 'GOOGLE': 'GOOG',
                 'AIRBNB': 'ABNB', 'ALIBABA': 'BABA', 'CHEVRON': 'CVX', 'EBAY': 'EBAY', 'FORD': 'F', 'HEWLETT PACKARD': 'HP'
    }
    reply = 'The following are the top 10 stocks:\n'
    response = '%s : %s\n'
    r = ''

    for key, value in stock_df.items():
        r += response%(key, value)
    final = reply + r
    bot.send_message(message.chat.id, final)

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, 'Hello!')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'I am a protoype stock bot still under work. Currently I have some basics functions. You can click on: \n/greet \n/hello \n/wsb \n/examples '
                                      '\nOr you can ask for the closing price of a stock by typing: price stock name')

@bot.message_handler(commands=['wsb'])
def get_stocks(message):
    response = ''
    stocks = ['aapl', 'tsla', 'fb']
    stock_data = []
    for stock in stocks:
        data = yf.download(tickers=stock, period='2d', interval='1d')
        data = data.reset_index()
        response += f'---------(stock)---------\n'
        stock_data.append([stock])
        columns = ['stock']
        for index, row in data.iterrows():
            stock_position = len(stock_data) - 1
            price = round(row['Close'], 2)
            format_date = row['Date'].strftime('%m/%d')
            response += f"{format_date}: {price}\n"
            stock_data[stock_position].append(price)
            columns.append(format_date)
        print()

    response = f'{columns[0]: <10}{columns[1]: ^10}{columns[2]: >10}\n'
    for row in stock_data:
        response += f"{row[0]: <10}{row[1]: ^10}{row[2]: >10}\n"
    response += "\nStock Data"
    print(response)
    bot.send_message(message.chat.id, response)


def stock_request(message):
    request = message.text.split()
    if len(request) < 2 or request[0].lower() not in 'price':
        return False
    else:
        return True

@bot.message_handler(func=stock_request)
def send_price(message):
    request = message.text.split()[1]
    data = yf.download(tickers=request, period='5m', interval='1m')
    if data.size > 0:
        data = data.reset_index()
        data["formate_date"] = data["Datetime"].dt.strftime('%m%d %I:%M %p')
        data.set_index('formate_date', inplace=True)
        print(data.to_string())
        result = data['Close'].to_string(header=False) + '\n' + request + ' last 5 minutes closing price'
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, 'NO Data!')


@bot.message_handler(commands=['info'])
def send_welcome(message):
    name = bot.get_me()
    user1 = message.from_user.id
    user = message.from_user.first_name
    message.from_user.last_name
    message.from_user.username
    print(user)
    bot.reply_to(message, "Welcome")

@bot.message_handler(func = lambda msg: msg.text is not None and '/' not in msg.text)
def welcome(message):
    if message.text.lower() == "hi":
        user = message.from_user.first_name + message.from_user.last_name
        bot.send_message(message.chat.id,"Hello! " + user + ", How can I help you today? \n/help")


bot.polling()
