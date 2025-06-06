
from threading import Thread
import time
from django.http import HttpResponse
from django.shortcuts import render
from yahoo_fin.stock_info import tickers_nifty50
import queue
import yfinance as yf
from websockets.sync.client import connect
from asgiref.sync import sync_to_async

def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request, 'trades/stockpicker.html', {'stockpicker': stock_picker})

@sync_to_async
def checkAuthenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True

async def stockTracker(request):
    is_loginned = checkAuthenticated(request)
    if not is_loginned:
        return HttpResponse("Login First")
    stockpicker = request.GET.getlist('stockpicker')
    print(stockpicker)
    data = {}
    available_stocks = tickers_nifty50()

    for i in stockpicker:
        if i not in available_stocks:
            return HttpResponse("Invalid stock ticker")

    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    start = time.time()

    for i in range(n_threads):
        thread = Thread(target=fetch_data, args=(que, stockpicker[i]))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)

    end = time.time()
    print("Time taken:", end - start)
    print(data)

    valid_data = {k: v for k, v in data.items() if v}
    if not valid_data:
        return HttpResponse("Failed to fetch stock data. Please try again later.")

    return render(request, 'trades/stocktracker.html', {'data': valid_data, 'room_name': 'track'})


def fetch_data(q, ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        q.put({ticker: info})
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        q.put({ticker: {}})
