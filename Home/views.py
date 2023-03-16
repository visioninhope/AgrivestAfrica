from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import math
from .models import Inbox
from Log.models import User,Sponsor,Farmer,Offtaker,Profile
from Transaction.models import TradeInvoice,TradeLog,TradeReceipt,FarmInvoice,FarmLog,ProduceInvoice,ProduceLog
from Asset.models import Trade


def home(request):
    logout(request)
    trades = Trade.objects.all()
    sliderT = Trade.objects.all().order_by('-id')[:3]
    x =  math.floor(Trade.objects.all().count() / 3)

    slide1 = Trade.objects.all().order_by('id')[:3]
    slide2 = Trade.objects.all().order_by('id')[3:7]

    min_slide1 = Trade.objects.all()[2:3]
    min_slide2 = Trade.objects.all()[:1]
    min_slide3 = Trade.objects.all()[1:2]

    context = {
        'trades' : trades,
        'sliderT' : sliderT,
        'slide1' : slide1,
        'slide2' : slide2,
        'x' : x,
        'min_slide1' : min_slide1,
        'min_slide2' : min_slide2,
        'min_slide3' : min_slide3,
    }
    return render(request,'index.html', context)


def check_job(request):
    if Sponsor.objects.filter(user=request.user).exists():
        print('sponsor')
    elif Farmer.objects.filter(user=request.user).exists():
        print('farmer')
    elif Offtaker.objects.filter(user=request.user).exists():
        print('offtaker')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
@csrf_exempt
def dashboard(request):
    print(request.body)
    total_trans = 0
    ts = TradeInvoice.objects.filter(customer=request.user)
    fs = FarmInvoice.objects.filter(customer=request.user)
    ps = ProduceInvoice.objects.filter(customer=request.user)
    total_count = ts.count() + fs.count() + ps.count()
    for t in ts:
        total_trans = total_trans + t.total_cost
    for f in fs:
        total_trans = total_trans + f.total_cost
    for p in ps:
        total_trans = total_trans + p.total_cost
    if request.method == 'POST':
        search_in = request.POST.get('search')
        search_status = request.POST.get('status')
        if search_in and search_status:
            trades = TradeInvoice.objects.filter(customer=request.user).filter(name__icontains = search_in).filter(status = search_status).values_list('type','name','total_cost','start_date','end_date','status','slug','image_url')
            farms = FarmInvoice.objects.filter(customer=request.user).filter(name__icontains = search_in).filter(status = search_status).values_list('type','name','total_cost','start_date','end_date','status','slug','image_url')
        else:
            if search_in:
                trades = TradeInvoice.objects.filter(customer=request.user).filter(name__icontains = search_in).values_list('type','name','total_cost','start_date','end_date','status','slug','image_url')
                farms = FarmInvoice.objects.filter(customer=request.user).filter(name__icontains = search_in).values_list('type','name','total_cost','start_date','end_date','status','slug','image_url')
            if search_status:
                trades = TradeInvoice.objects.filter(customer=request.user).filter(status = search_status).values_list('type','name','total_cost','start_date','end_date','status','slug','image_url')
                farms = FarmInvoice.objects.filter(customer=request.user).filter(status = search_status).values_list('type','name','total_cost','start_date','end_date','status','slug','image_url')
    else:
        trades = TradeInvoice.objects.filter(customer=request.user).values_list('type','name','total_cost','start_date','end_date','status','slug','image_url')
        farms = FarmInvoice.objects.filter(customer=request.user).values_list('type','name','total_cost','start_date','end_date','status','slug','image_url')
    trans = trades.union(farms)
    tradeList = Trade.objects.all()[1:4]
    tradePages = Paginator(tradeList, 2)
    pageList = []
    for page in tradePages:
        pageList.append(page.object_list)
    context = {
        'trans' : trans,
        'total_trans' : total_trans,
        'total_count' : total_count,
        'pageList' : pageList
    }
    return render(request,'Dashboard/dashboard.html', context)

@login_required
def trade_log(request):
    if request.method == 'POST':
        search_in = request.POST.get('search')
        search_status = request.POST.get('status')
        print(search_status)
        if search_in and search_status:
            print(1)
            trades = TradeInvoice.objects.filter(customer=request.user).filter(name__icontains = search_in).filter(status = search_status)
            print(trades)
        else:
            print(3)
            if search_in:
                trades = TradeInvoice.objects.filter(customer=request.user).filter(name__icontains = search_in)
            if search_status:
                trades = TradeInvoice.objects.filter(customer=request.user).filter(status = search_status)    
        # print(trades)
    else:
        trades = TradeInvoice.objects.filter(customer=request.user)

    pend_count = TradeInvoice.objects.filter(status='Pending').count()
    act_count = TradeInvoice.objects.filter(status='Active').count()
    comp_count = TradeInvoice.objects.filter(status='Completed').count()
    trades_bought = 0
    trades_sold = 0
    tradeList = TradeInvoice.objects.filter(customer=request.user)
    for trade in trades:
        trades_bought = trades_bought + trade.total_cost
        trades_sold = trades_sold + trade.actual_return
    trades_bal = "{:.2f}".format(trades_sold - trades_bought) 

    context = {
        'trades' : trades,
        'trades_bought' : trades_bought,
        'trades_sold' : trades_sold,
        'trades_bal' : trades_bal,
        'pend_count' : pend_count,
        'act_count' : act_count,
        'comp_count' : comp_count,
    }
    return render(request,'Dashboard/tradeLog.html', context)

@login_required
def tradeLog_info(request,slug):
    trade = TradeInvoice.objects.get(slug=slug)
    context ={
        'trade' : trade
    }
    return render(request, 'Dashboard/tradeLog_info.html', context)

@login_required
def farm_log(request):
    farms = FarmInvoice.objects.filter(customer=request.user)
    pend_count = FarmInvoice.objects.filter(status='Pending').count()
    act_count = FarmInvoice.objects.filter(status='Active').count()
    comp_count = FarmInvoice.objects.filter(status='Completed').count()
    farms_bought = 0
    farms_sold = 0
    for farm in farms:
        farms_bought = farms_bought + farm.total_cost
        farms_sold = farms_sold + farm.actual_return
    farms_bal = "{:.2f}".format(farms_sold - farms_bought) 
    context = {
        'farms' : farms,
        'farms_bought' : farms_bought,
        'farms_sold' : farms_sold,
        'farms_bal' : farms_bal,
        'pend_count' : pend_count,
        'act_count' : act_count,
        'comp_count' : comp_count
    }
    return render(request,'Dashboard/farmLog.html', context)

@login_required
def farmLog_info(request,slug):
    farm = FarmInvoice.objects.get(slug=slug)
    context ={
        'farm' : farm
    }
    return render(request, 'Dashboard/farmLog_info.html', context)

@login_required
def produce_log(request):
    produces =ProduceInvoice.objects.filter(customer=request.user)
    produces_bought = 0
    for prod in produces:
        produces_bought = produces_bought + prod.total_cost
    context = {
        'produces' : produces,
        'produces_bought' : produces_bought
    }
    return render(request,'Dashboard/produceLog.html', context)

def produceLog_info(request,slug):
    produce = ProduceInvoice.objects.get(slug=slug)
    context = {
        'produce' : produce,
    }
    return render(request, 'Dashboard/produceLog_info.html', context)

@login_required
def profile(request):
    pro_exists = False
    user = User.objects.get(username=request.user)
    if Profile.objects.filter(user=user).exists():
        pro_exists = True
        pro_info = Profile.objects.get(user=user)
    else:
        pro_info = ''
    if request.method == 'POST':
        if pro_exists:
            profile = Profile.objects.get(user=user)
            print(profile)
        else:
            profile = Profile()
            profile.user = user
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.other_name = request.POST.get('other_name')
        profile.gender = request.POST.get('gender')
        profile.relationship = request.POST.get('relationship')
        profile.profession = request.POST.get('profession')
        profile.email = request.POST.get('email')
        profile.contact = request.POST.get('contact')
        profile.dob = request.POST.get('dob')
        profile.cor = request.POST.get('cor')
        profile.nationality = request.POST.get('nationality')
        profile.address = request.POST.get('address')
        profile.id_card = request.POST.get('id_card')
        profile.id_number = request.POST.get('id_num')
        profile.next_of_kin = request.POST.get('nok')
        profile.nok_relation = request.POST.get('nok_relation')
        profile.nok_contact = request.POST.get('nok_contact')
        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES.get('profile_pic')
        if request.FILES.get('id_pic_front'):
            profile.id_pic_front = request.FILES.get('id_pic_front')
        if request.FILES.get('id_pic_back'):
            profile.id_pic_back = request.FILES.get('id_pic_back')
        if request.POST.get('referral'):
            profile.referral_code = request.POST.get('referral')
        profile.last_updated = timezone.now()
        profile.save()
        return redirect('profile_page')
    context = {
        'pro_exists' : pro_exists,
        'pro_info' : pro_info,
    }
    return render(request, 'Dashboard/profile.html', context)

@login_required
def inbox(request):
    inboxes = Inbox.objects.all()
    context = {
        'inboxes' : inboxes
    }
    return render(request, 'Dashboard/inbox.html', context)

def dash_overview(request):
    return render(request, 'Dashboard/overview.html')
def dash_transactions(request):
    return render(request, 'Dashboard/transactions.html')
def dash_produce(request):
    return render(request, 'Dashboard/produce.html')


###EXTRAS###
def about(request):
    return render(request, 'Extras/about.html')
def advisors(request):
    return render(request, 'Extras/advisors.html')
def board(request):
    return render(request, 'Extras/board.html')
def faq(request):
    return render(request, 'Extras/faq.html')
def gallery(request):
    return render(request, 'Extras/gallery.html')
def get_started(request):
    return render(request, 'Extras/get_started.html')
def team(request):
    return render(request, 'Extras/team.html')
def traction(request):
    return render(request, 'Extras/traction.html')
def webinar(request):
    return render(request, 'Extras/webinar.html')
def what_we_do(request):
    return render(request, 'Extras/what_we_do.html')
def testimonials(request):
    return render(request, 'Extras/testimonials.html')    
def referrals(request):
    return render(request, 'Extras/referrals.html') 
def investors(request):
    return render(request, 'Extras/investors.html')
def blog(request):
    return render(request, 'Extras/blog.html')
def contact(request):
    return render(request, 'Extras/contact.html')
def how_to(request):
    return render(request, 'Extras/how_to.html')

def mailPortal(request):
    if request.method == 'POST':
        inbox = Inbox()
        inbox.title = request.POST.get('title')
        inbox.content = request.POST.get('content')
        inbox.image = request.FILES.get('image')
        inbox.save()
    return render(request, 'mailPortal.html')

def sitemap(request):
    return render(request, 'sitemap.xml')

