from django.shortcuts import render,redirect
import requests,json
from django.contrib import messages
from django.http import JsonResponse
from Log.models import User, Sponsor
from Asset.models import Trade, Farm, Market
from Transaction.models import FarmInvoice,FarmLog,TradeInvoice,TradeLog
import math

def trades(request):
    z = math.ceil(Trade.objects.all().count()/3)
    s = -3
    e = 0
    tradeRow = []
    for i in range(z):
        s = s+3
        e = e+3
        trade = Trade.objects.all()[s:e]
        tradeRow.append(trade)
    context = {
        'tradeRow': tradeRow
    }
    return render(request, 'Trades/trades.html', context)

def makeTrade(request, id):
    trade = Trade.objects.get(id=id)
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
                tradeLog.status = 'Pending'
                tradeLog.save()
                return redirect('trades_page')
        else:
            messages.error(request, 'Create Account to continue')
            '''
            mobileNumber = request.POST.get('mobile')
            amount = int(request.POST.get('amount'))
            ref = request.POST.get('ref')
            user2 = 'evviouhu'
            pass2 = 'lrrnebkb'

            data = {
                "amount": amount,
                "title": trade_name,
                "description": trade.name,
                "clientReference": ref,
                "callbackUrl": "https://edmanager-production.up.railway.app/callback",
                #"cancellationUrl": "http://127.0.0.1:8000/cancel",
                #"returnUrl": "http://127.0.0.1:8000/return",
            }
            url = f'https://devp-reqsendmoney-230622-api.hubtel.com/request-money/{mobileNumber}'
            headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "authorization": "Basic ZXZ2aW91aHU6bHJybmVia2I="
                }
            response = requests.post(url, headers, json=data)
            raws = response.text
            raw = json.loads(raws)
            v = raw['data']['paylinkUrl']
            if response.status_code == 201:
                return redirect(f'{v}')
            '''
    w = trade.name.split()
    crop = w[0]
    context = {
        'trade': trade,
        'crop': crop,
    }
    return render(request, 'Trades/makeTrade.html', context)

def farms(request):
    z = math.ceil(Trade.objects.all().count()/3)
    s = -3
    e = 0
    farmRow = []
    for i in range(z):
        s = s+3
        e = e+3
        farm = Farm.objects.all()[s:e]
        farmRow.append(farm)
    context = {
        'farmRow': farmRow
    }
    return render(request, 'Farms/farms.html', context)

def makeFarm(request, id):
    customer = User.objects.get(username=request.user)
    farm = Farm.objects.get(id=id)
    end = farm.end_date
    start = farm.start_date
    if request.method == 'POST':
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
    context = {
        'farm': farm,
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