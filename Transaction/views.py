from django.shortcuts import render,redirect
import requests,json
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from Log.models import User, Sponsor
from Asset.models import Trade, Farm, Market
from Transaction.models import FarmInvoice,FarmLog,TradeInvoice,TradeLog
from random import randint
import math


def trades(request):
    if request.method == 'POST':
        active = 'yes'
        search = request.POST.get('search')
        res = Trade.objects.filter(name__icontains = search)
        res.count()
        print(res.count())
        if res.count() > 0:
            result_page = Paginator(res,3)
        else:
            result_page = ''
            messages.error(request, f"Couldn't find a match, Try something else")
    else:
        active = 'no'
        result_page = None
    trades = Trade.objects.all()
    tradePages = Paginator(trades, 3)
    pageList = []
    for page in tradePages:
        pageList.append(page.object_list)
    context = {
        'active' : active,
        'result_page' : result_page,
        'pageList' : pageList,
    }
    return render(request, 'Trades/trades.html', context)

def makeTrade(request, slug):
    trade = Trade.objects.get(slug=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            customer = User.objects.get(username=request.user)
            units = int(request.POST.get('units'))
            total_cost = (units * trade.price) + ((units * trade.price) * (trade.service_charge / 100))
            trade_name = request.POST.get('trade_name')
            extra_notes = request.POST.get('extra_notes')
            tradeInvoice = TradeInvoice()
            if TradeInvoice.objects.filter(customer=request.user).filter(trade_name=trade_name).exists():
                messages.info(request, f"You already have a trade named |-> {trade_name}")
            else:
                tradeInvoice.trade_name = trade_name
                tradeInvoice.customer = customer
                tradeInvoice.trade = trade
                tradeInvoice.price = trade.price
                tradeInvoice.units = units
                tradeInvoice.profit_range_min = trade.ros_min
                tradeInvoice.profit_range_max = trade.ros_max
                tradeInvoice.start_date = trade.start_date
                tradeInvoice.end_date = trade.end_date
                tradeInvoice.base_cost = units * trade.price
                tradeInvoice.service_charge = trade.service_charge
                tradeInvoice.total_cost = total_cost
                tradeInvoice.pros_min = round((units * trade.price) * (trade.ros_min/100))
                tradeInvoice.pros_max = round((units * trade.price) * (trade.ros_max/100))
                tradeInvoice.totalreturn_min = (int(tradeInvoice.base_cost) + int(tradeInvoice.pros_min))
                tradeInvoice.totalreturn_max = (int(tradeInvoice.base_cost) + int(tradeInvoice.pros_max))
                tradeInvoice.image_url = trade.image.url
                if extra_notes != '':
                    tradeInvoice.extra_notes = extra_notes
                tradeInvoice.status = 'Pending'
                payment = request.POST.get('payment')
                tradeInvoice.payment = payment
                tradeInvoice.save()
                tradeLog = TradeLog()
                tradeLog.trade_name = trade_name
                tradeLog.customer = customer
                tradeLog.price = trade.price
                tradeLog.units = units
                tradeLog.profit_range_min = tradeInvoice.profit_range_min
                tradeLog.profit_range_max = tradeInvoice.profit_range_max
                tradeLog.start_date = trade.start_date
                tradeLog.end_date = trade.end_date
                tradeLog.base_cost = tradeInvoice.base_cost
                tradeLog.service_charge = trade.service_charge
                tradeLog.total_cost = tradeInvoice.total_cost
                token = randint(1000,9999)
                tradeLog.token = token
                tradeLog.status = 'Pending'
                tradeLog.save()

                print(total_cost, 'total')
                url = "https://payproxyapi.hubtel.com/items/initiate"

                payload = json.dumps({
                    "totalAmount": total_cost,
                    "description": trade_name,
                    "callbackUrl": "https://www.agrivestafrica.com/dashboard/",
                    "returnUrl": "https://www.agrivestafrica.com/dashboard/",
                    "merchantAccountNumber": "2017279",
                    "cancellationUrl": "https://www.agrivestafrica.com/trades/",
                    "clientReference": token
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Basic bXkxS0ExUjphMjgzNGM3NjA2NzY0MzY2ODdhNTBjZGJkYTM0OGJlNA=='
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                link = json.loads(response.text)['data']['checkoutUrl']
                return redirect(f'{link}')
        else:
            messages.error(request, 'Create Account to continue')

    w = trade.name.split()
    crop = w[0]
    context = {
        'trade': trade,
        'crop': crop,
    }
    return render(request, 'Trades/makeTrade.html', context)



def farms(request):
    if request.method == 'POST':
        active = 'yes'
        search = request.POST.get('search')
        res = Farm.objects.filter(name__icontains = search)
        res.count()
        print(res.count())
        if res.count() > 0:
            result_page = Paginator(res,3)
        else:
            result_page = ''
            messages.error(request, f"Couldn't find a match, Try something else")
    else:
        active = 'no'
        result_page = None
    farms = Farm.objects.all()
    farmPages = Paginator(farms, 3)
    pageList = []
    for page in farmPages:
        pageList.append(page.object_list)
    context = {
        'pageList' : pageList,
        'active' : active,
        'result_page' : result_page
    }
    return render(request, 'Farms/farms.html', context)


def makeFarm(request, slug):
    farm = Farm.objects.get(slug=slug)
    partners = farm.partners.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            customer = User.objects.get(username=request.user)
            units = int(request.POST.get('units'))
            total_cost = (units * farm.price) + ((units * farm.price) * (farm.service_charge / 100))
            farm_name = request.POST.get('farm_name')
            extra_notes = request.POST.get('extra_notes')
            farmInvoice = FarmInvoice()
            if FarmInvoice.objects.filter(customer=request.user).filter(farm_name=farm_name).exists():
                messages.info(request, f"You already have a farm named {farm_name}")
            else:
                farmInvoice.farm_name = farm_name
                farmInvoice.customer = customer
                farmInvoice.farm = farm.name
                farmInvoice.location = farm.location
                farmInvoice.price = farm.price
                farmInvoice.units = units
                farmInvoice.profit_range_min = farm.ros_min
                farmInvoice.profit_range_max = farm.ros_max
                farmInvoice.start_date = farm.start_date
                farmInvoice.end_date = farm.end_date
                farmInvoice.base_cost = units * farm.price
                farmInvoice.service_charge = farm.service_charge
                farmInvoice.total_cost = total_cost
                farmInvoice.pros_min = round((units * farm.price) * (farm.ros_min/100))
                farmInvoice.pros_max = round((units * farm.price) * (farm.ros_max/100))
                farmInvoice.totalreturn_min = (int(farmInvoice.base_cost) + int(farmInvoice.pros_min))
                farmInvoice.totalreturn_max = (int(farmInvoice.base_cost) + int(farmInvoice.pros_max))
                if extra_notes != '':
                    farmInvoice.extra_notes = extra_notes
                farmInvoice.status = 'Pending'
                payment = request.POST.get('payment')
                farmInvoice.payment = payment
                farmInvoice.save()
                farmLog = FarmLog()
                farmLog.farm_name = farm_name
                farmLog.customer = customer
                farmLog.location = farm.location
                farmLog.price = farm.price
                farmLog.units = units
                farmLog.profit_range_min = farm.ros_min
                farmLog.profit_range_max = farm.ros_max
                farmLog.start_date = farm.start_date
                farmLog.end_date = farm.end_date
                farmLog.base_cost = units * farm.price
                farmLog.service_charge = farm.service_charge
                farmLog.total_cost = total_cost
                farmLog.status = 'Pending'
                farmLog.save()
        else:
            messages.error(request, 'Create Account to continue')
    context = {
        'farm': farm,
        'partners' : partners,
    }
    return render(request, 'Farms/makeFarm.html', context)

def markets(request):
    markets = Market.objects.all()
    context = {
        'markets' : markets
    }
    return render(request, 'Markets/markets.html', context)



def callback(request):

    return render(request, 'callback.html')