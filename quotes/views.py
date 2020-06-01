import json

import requests
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import StockForm
from .models import Stock


def home(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=YOUR_API_TOKEN")

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})
    else:
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/aapl/quote?token=YOUR_API_TOKEN")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api': api})


def about(request):
    return render(request, 'about.html', {})


def add_stocks(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, 'Stock has been added')
            return redirect('add_stocks')

    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get(
                "https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token"
                                                                               "=pk_836c0f55f55940788d27b5e7d1620885")

            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, 'add_stocks.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, 'Stock has been deleted')
    return redirect('delete_stocks')


def delete_stock(request):
    ticker = Stock.objects.all()
    return render(request, 'delete_stocks.html', {'ticker': ticker})
