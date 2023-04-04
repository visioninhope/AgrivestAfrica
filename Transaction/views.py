from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.paginator import Paginator
from Log.models import User, Sponsor
from Asset.models import Trade, Farm, Produce,Partner
from Transaction.models import FarmInvoice,TradeInvoice,ProduceInvoice
from uuid import uuid4
import json,requests

def trades(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        trades = Trade.objects.filter(name__icontains = search)
        if trades:
            tradePages = Paginator(trades, 3)
            pageList = []
            for page in tradePages:
                pageList.append(page.object_list)
        else:
            pageList = []
            messages.error(request, f"Couldn't find a match, Try something else")
    else:
        trades = Trade.objects.all()
        tradePages = Paginator(trades, 3)
        pageList = []
        for page in tradePages:
            pageList.append(page.object_list)
    context = {
        'pageList' : pageList,
    }
    return render(request, 'Trades/trades.html', context)

def makeTrade(request, slug):
    trade = Trade.objects.get(slug=slug)
    partners = trade.partners.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            customer = User.objects.get(username=request.user)
            units = int(request.POST.get('units'))
            total_cost = (units * trade.price) + ((units * trade.price) * (trade.service_charge / 100))
            trade_name = request.POST.get('name')
            partner = request.POST.get('partner')
            harvest_type = request.POST.get('harvest_type')
            extra_notes = request.POST.get('extra_notes')
            if TradeInvoice.objects.filter(customer=request.user).filter(name=trade_name).exists():
                messages.info(request, f"You already have a trade named |-> {trade_name}")
            else:
                tradeInvoice = TradeInvoice()
                tradeInvoice.name = trade_name
                tradeInvoice.customer = customer
                tradeInvoice.trade = trade
                tradeInvoice.partner = Partner.objects.get(name=partner)
                tradeInvoice.harvest_type = harvest_type
                tradeInvoice.price = trade.price
                tradeInvoice.units = units
                tradeInvoice.profit_range_min = trade.ros_min
                tradeInvoice.profit_range_max = trade.ros_max
                tradeInvoice.start_date = trade.start_date
                tradeInvoice.end_date = trade.end_date
                tradeInvoice.base_cost = "{:.2f}".format(units * trade.price)
                tradeInvoice.service_charge = trade.service_charge
                tradeInvoice.total_cost = "{:.2f}".format(total_cost)
                tradeInvoice.pros_min = round((units * trade.price) * (trade.ros_min/100))
                tradeInvoice.pros_max = round((units * trade.price) * (trade.ros_max/100))
                tradeInvoice.totalreturn_min = "{:.2f}".format((float(tradeInvoice.base_cost) + float(tradeInvoice.pros_min))) 
                tradeInvoice.totalreturn_max = "{:.2f}".format((float(tradeInvoice.base_cost) + float(tradeInvoice.pros_max)))
                if extra_notes != '':
                    tradeInvoice.extra_notes = extra_notes
                tradeInvoice.status = 'Pending'
                # payment = request.POST.get('payment')
                # tradeInvoice.payment = payment
                tradeInvoice.save()
                return redirect(trans_pay(total_cost,trade_name, TradeInvoice, 'trade'))
        else:
            messages.error(request, 'Create Account to continue')

    w = trade.name.split()
    crop = w[0]
    context = {
        'trade': trade,
        'partners' : partners,
        'crop': crop,
    }
    return render(request, 'Trades/makeTrade.html', context)

def farms(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        farms = Farm.objects.filter(name__icontains = search)
        if farms:
            farmPages = Paginator(farms, 3)
            pageList = []
            for page in farmPages:
                pageList.append(page.object_list)
        else:
            pageList = []
            messages.error(request, f"Couldn't find a match, Try something else")
    else:
        farms = Farm.objects.all()
        farmPages = Paginator(farms, 3)
        pageList = []
        for page in farmPages:
            pageList.append(page.object_list)
    context = {
        'pageList' : pageList,
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
            farm_name = request.POST.get('name')
            harvest_type = request.POST.get('harvest_type')
            partner = request.POST.get('partner')
            extra_notes = request.POST.get('extra_notes')
            farmInvoice = FarmInvoice()
            if FarmInvoice.objects.filter(customer=request.user).filter(name=farm_name).exists():
                messages.info(request, f"You already have a farm named {farm_name}")
            else:
                farmInvoice.name = farm_name
                farmInvoice.customer = customer
                farmInvoice.farm = farm
                farmInvoice.partner = Partner.objects.get(name=partner)
                farmInvoice.harvest_type = harvest_type
                farmInvoice.price = farm.price
                farmInvoice.units = units
                farmInvoice.profit_range_min = farm.ros_min
                farmInvoice.profit_range_max = farm.ros_max
                farmInvoice.start_date = farm.start_date
                farmInvoice.end_date = farm.end_date
                farmInvoice.base_cost = "{:.2f}".format(units * farm.price)
                farmInvoice.service_charge = farm.service_charge
                farmInvoice.total_cost = "{:.2f}".format(total_cost)
                farmInvoice.pros_min = round((units * farm.price) * (farm.ros_min/100))
                farmInvoice.pros_max = round((units * farm.price) * (farm.ros_max/100))
                farmInvoice.totalreturn_min = "{:.2f}".format(float(farmInvoice.base_cost) + float(farmInvoice.pros_min))
                farmInvoice.totalreturn_max = "{:.2f}".format(float(farmInvoice.base_cost) + float(farmInvoice.pros_max))
                if extra_notes != '':
                    farmInvoice.extra_notes = extra_notes
                farmInvoice.status = 'Pending'
                # payment = request.POST.get('payment')
                farmInvoice.save()
                return redirect(trans_pay(total_cost,farm_name, FarmInvoice, 'farm'))
        else:
            messages.error(request, 'login to continue')
    context = {
        'farm': farm,
        'partners' : partners,
    }
    return render(request, 'Farms/makeFarm.html', context)

def produce(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        produces = Produce.objects.filter(name__icontains = search)
        if produces:
            producePages = Paginator(produces, 4)
            pageList = []
            for page in producePages:
                pageList.append(page.object_list)
        else:
            pageList = []
            messages.error(request, f"Couldn't find a match, Try something else")
    else:
        produces = Produce.objects.all()
        producePages = Paginator(produces, 4)
        pageList = []
        for page in producePages:
            pageList.append(page.object_list)
    produces = Produce.objects.all()
    context = {
        'pageList' : pageList,
        'produces' : produces
    }
    return render(request, 'Produce/produce.html', context)

def buy_produce(request,slug):
    produce = Produce.objects.get(slug=slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            customer = User.objects.get(username=request.user)
            units = int(request.POST.get('units'))
            total_cost = ((units * produce.price))
            produce_name = request.POST.get('name')
            produceInvoice = ProduceInvoice()
            if ProduceInvoice.objects.filter(customer=request.user).filter(name=produce_name).exists():
                messages.info(request, f"You already have a produce named {produce_name}")
            else:
                produceInvoice.name = produce_name
                produceInvoice.customer = customer
                produceInvoice.produce = produce
                produceInvoice.price = produce.price
                produceInvoice.units = units
                produceInvoice.base_cost = "{:.2f}".format(units * produce.price)
                produceInvoice.total_cost = "{:.2f}".format(total_cost)
                produceInvoice.image_url = produce.image.url
                # payment = request.POST.get('payment')
                # produceInvoice.payment = payment
                produceInvoice.save()
                return redirect(trans_pay(total_cost,produce_name, ProduceInvoice, 'produce'))
    context ={
        'produce' : produce
    }
    return render(request, 'Produce/buyProduce.html', context)    

def trans_pay(total_cost, trans_name,trans_obj,type):
    cur_trans = trans_obj.objects.get(name=trans_name)
    url = "https://payproxyapi.hubtel.com/items/initiate"
    token = str(uuid4())
    payload = json.dumps({
        "totalAmount": total_cost,
        "description": trans_name,
        "callbackUrl": f'https://www.agrivestafrica.com/trans_callback/{type}/',
        "returnUrl": f'https://www.agrivestafrica.com/trans_callback/{type}/',
        "merchantAccountNumber": "2017279",
        "cancellationUrl": "https://www.agrivestafrica.com/trades/",
        "clientReference": token
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic TjhaWlBtODoxZThiYmI5NzFmMmE0ZmI3OGYwNjIwYzFjMTU0NmYxMg=='
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    link = json.loads(response.text)['data']['checkoutUrl']
    check_id = json.loads(response.text)['data']['checkoutId']

    cur_trans.check_id = check_id
    cur_trans.paylink = f'{link}'
    cur_trans.save()
    link = f'{link}'
    return link
