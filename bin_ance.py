from binance.client import Client
import config
import datetime
import sched, time
import telegram

condition_ratio = 20
your_chat_id = 0

client = Client(config.key, config.security)
info = client.get_account()
s = sched.scheduler(time.time, time.sleep)

bot = telegram.Bot(token=config.token)
updates = bot.get_updates()

tickers = ['BTCUSDT', 'SLPBUSD', 'TROYUSDT', 'FXSBUSD', 'TVKBUSD', 'BURGERUSDT']

balances = info['balances']


def exch_info():
    for s in client.get_exchange_info()['symbols']:
        print(s['symbol'])


def meanVolume(interv, klinesArr):
    n = interv
    sum = 0
    while n - 1 >= 0:
        sum += float(klinesArr[-n - 1][5])
        n += -1
    if sum == 0:
        sum = interv
    else:
        pass
    return sum / interv


def checkCondition(ticker):
    global condition_ratio
    klines = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "20 minutes ago UTC")
    meanV = meanVolume(15, klines)
    if float(klines[-1][5]) > condition_ratio * meanV:
        print(
            f'Huge amount of {ticker} coins traded at time {datetime.datetime.now()}. The ratio - {float(klines[-1][5]) / meanV}')
        bot.send_message(
            text=f'Huge amount of {ticker} coins traded at time {datetime.datetime.now()}. The ratio - {float(klines[-1][5]) / meanV}',
            chat_id=your_chat_id)
    else:
        # print(f"{datetime.datetime.now().time()}... {ticker}... No matches. The ratio of current volume and mean volume is {float(klines[-1][5])/meanV}")
        pass


def tickers_loop(tickersArr):
    for t in tickersArr:
        checkCondition(t)
    s.enter(10, 1, tickers_loop, (tickers,))


def main_function():
    s.enter(10, 1, tickers_loop, (tickers,))
    s.run()


main_function()
