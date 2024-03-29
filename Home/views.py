from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse, parse_qs
import math,threading
from django.core.mail import EmailMessage
from .models import Inbox,Team,Board,Advisor
from Log.models import User,Sponsor,Farmer,Offtaker,Profile
from Transaction.models import TradeInvoice,FarmInvoice,ProduceInvoice
from Asset.models import Trade,Farm

def home(request):
    trades = Trade.objects.all()
    sliderT = Trade.objects.all().order_by('-id')[:3]
    x =  math.floor(Trade.objects.all().count() / 3)

    slide1 = Farm.objects.all().order_by('id')[:3]
    slide2 = Farm.objects.all().order_by('id')[3:7]

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
def dashboard(request):
    ts = TradeInvoice.objects.filter(customer=request.user)
    fs = FarmInvoice.objects.filter(customer=request.user)
    ps = ProduceInvoice.objects.filter(customer=request.user)
    total_count = ts.count() + fs.count() + ps.count()

    if request.method == 'POST':
        status_val = request.POST.get('status') 
        if status_val == 'all':
            trades = ts.order_by('-id')[0:5]
            farms = fs.order_by('-id')[0:5]
            produces = ps.order_by('-id')[0:5]
        else:
            trades = ts.filter(status=status_val).order_by('-id')[0:5]
            farms = fs.filter(status=status_val).order_by('-id')[0:5]
            produces = ps.order_by('-id')[0:5]
    else:
        trades = ts.order_by('-id')[0:5]
        farms = fs.order_by('-id')[0:5]
        produces = ps.order_by('-id')[0:5]

    tradeList = Trade.objects.all()[0:9]
    tradePages = Paginator(tradeList, per_page=2)
    tradePages_2 = Paginator(tradeList, per_page=3)
    pageList = []
    pageList_2 = []
    for page in tradePages:
        pageList.append(page.object_list)
    for page in tradePages_2:
        pageList_2.append(page.object_list)
    context = {
        'trades' : trades,
        'farms': farms,
        'produces' : produces,
        'total_trans' : "{:.2f}".format(get_total_trans(request)),
        'total_count' : total_count,
        'pageList' : pageList,
        'pageList_2' : pageList_2
    }
    return render(request,'Dashboard/dashboard.html', context)

def get_total_trans(request):
    ts = TradeInvoice.objects.filter(customer=request.user).filter(status='Active').union(TradeInvoice.objects.filter(customer=request.user).filter(status='Completed'))
    fs = FarmInvoice.objects.filter(customer=request.user).filter(status='Active').union(FarmInvoice.objects.filter(customer=request.user).filter(status='Completed'))
    ps = ProduceInvoice.objects.filter(customer=request.user).filter(status='Completed')
    total_trans = 0
    for t in ts:
        total_trans = total_trans + t.total_cost
    for f in fs:
        total_trans = total_trans + f.total_cost
    for p in ps:
        total_trans = total_trans + p.total_cost
    return total_trans

@login_required
def trade_log(request):
    pend_count = TradeInvoice.objects.filter(customer=request.user).filter(status='Pending').count()
    act_count = TradeInvoice.objects.filter(customer=request.user).filter(status='Active').count()
    comp_count = TradeInvoice.objects.filter(customer=request.user).filter(status='Completed').count()
    trades_bought = 0
    trades_sold = 0
    for trade in TradeInvoice.objects.filter(customer=request.user).filter(status='Active').union(TradeInvoice.objects.filter(customer=request.user).filter(status='Completed')):
        trades_bought = trades_bought + trade.total_cost
        trades_sold = trades_sold + trade.actual_return
    trades_bal = "{:.2f}".format(trades_sold - trades_bought) 

    # tradeList = TradeInvoice.objects.filter(customer=request.user)
    if request.method == 'POST':
        if not request.POST.get('status_select') == 'none':
            trades = TradeInvoice.objects.filter(customer=request.user).filter(status=request.POST.get('status_select'))
        else:
            trades = TradeInvoice.objects.filter(customer=request.user).filter(name__icontains=request.POST.get('trans_name'))
    else:
        trades= TradeInvoice.objects.filter(customer=request.user)
    context = {
        'trades' : trades,
        'trades_bought' : "{:.2f}".format(trades_bought),
        'trades_sold' : trades_sold,
        'trades_bal' : trades_bal,
        'pend_count' : pend_count,
        'act_count' : act_count,
        'comp_count' : comp_count,
        'total_trans' : "{:.2f}".format(get_total_trans(request)),
        'time' : timezone.now().date()
    }
    return render(request,'Dashboard/tradeLog.html', context)


@login_required
def tradeLog_info(request,slug):
    trade = TradeInvoice.objects.get(slug=slug)
    time = timezone.now().date()
    total_duration = (trade.end_date - trade.start_date).days
    duration_left = (trade.end_date - time).days
    if request.method == 'POST':
        print(request.POST)
        trade.delete()
        return redirect('tradeLog_page')
    context ={
        'trade' : trade,
        'time' : time,
        'total_duration' : total_duration,
        'duration_left' : duration_left,
        'total_trans' : "{:.2f}".format(get_total_trans(request)),
    }
    return render(request, 'Dashboard/tradeLog_info.html', context)



@login_required
def farm_log(request):
    pend_count = FarmInvoice.objects.filter(customer=request.user).filter(status='Pending').count()
    act_count = FarmInvoice.objects.filter(customer=request.user).filter(status='Active').count()
    comp_count = FarmInvoice.objects.filter(customer=request.user).filter(status='Completed').count()
    farms_bought = 0
    farms_sold = 0
    for farm in FarmInvoice.objects.filter(customer=request.user).filter(status='Active').union(FarmInvoice.objects.filter(customer=request.user).filter(status='Completed')):
        farms_bought = farms_bought + farm.total_cost
        farms_sold = farms_sold + farm.actual_return
    farms_bal = "{:.2f}".format(farms_sold - farms_bought) 

    if request.method == 'POST':
        if not request.POST.get('status_select') == 'none':
            farms = FarmInvoice.objects.filter(customer=request.user).filter(status=request.POST.get('status_select'))
        else:
            farms = FarmInvoice.objects.filter(customer=request.user).filter(name__icontains=request.POST.get('trans_name'))
    else:
        farms = FarmInvoice.objects.filter(customer=request.user)

    context = {
        'farms' : farms,
        'farms_bought' : farms_bought,
        'farms_sold' : farms_sold,
        'farms_bal' : farms_bal,
        'pend_count' : pend_count,
        'act_count' : act_count,
        'comp_count' : comp_count,
        'total_trans' : "{:.2f}".format(get_total_trans(request)),
        'time' : timezone.now().date()
    }
    return render(request,'Dashboard/farmLog.html', context)

@login_required
def farmLog_info(request,slug):
    farm = FarmInvoice.objects.get(slug=slug)
    time = timezone.now().date()
    total_duration = (farm.end_date - farm.start_date).days
    duration_left = (farm.end_date - time).days
    if request.method == 'POST':
        farm.delete()
        return redirect('farmLog_page')
    context ={
        'total_duration' : total_duration,
        'duration_left' : duration_left,
        'time' : time,
        'farm' : farm,
        'total_trans' : "{:.2f}".format(get_total_trans(request)),
    }
    return render(request, 'Dashboard/farmLog_info.html', context)

@login_required
def produce_log(request):
    produces_bought = 0
    for prod in ProduceInvoice.objects.filter(customer=request.user):
        produces_bought = produces_bought + prod.total_cost

    if request.method == 'POST':
        produces = ProduceInvoice.objects.filter(customer=request.user).filter(name__icontains=request.POST.get('trans_name'))
    else:
        produces =ProduceInvoice.objects.filter(customer=request.user)
    context = {
        'produces' : produces,
        'produces_bought' : produces_bought,
        'total_trans' : "{:.2f}".format(get_total_trans(request)),
    }
    return render(request,'Dashboard/produceLog.html', context)

def produceLog_info(request,slug):
    produce = ProduceInvoice.objects.get(slug=slug)
    if request.method == 'POST':
        produce.delete()
        return redirect('produceLog_page')
    context = {
        'produce' : produce,
        'total_trans' : "{:.2f}".format(get_total_trans(request)),
    }
    return render(request, 'Dashboard/produceLog_info.html', context)

@csrf_exempt
def trans_callback(request,slug):
    current_url = request.build_absolute_uri()
    url = current_url
    parse_result = urlparse(url)
    dict_result = parse_qs(parse_result.query)['checkoutid'][0]
    print(dict_result)
    if slug == 'trade':
        cur_trans = TradeInvoice.objects.get(check_id=dict_result)
        # cur_trans.start_time = timezone.now()
        cur_trans.status = 'Active'
        cur_trans.save()
    elif slug == 'farm':
        cur_trans = FarmInvoice.objects.get(check_id=dict_result)
        cur_trans.status = 'Active'
        cur_trans.save()
    else:
        cur_trans = ProduceInvoice.objects.get(check_id=dict_result)
        cur_trans.status = 'Completed'
        cur_trans.save()
    context = {
        'cur_trans' : cur_trans,
        'res' : dict_result
    }
    return render(request, 'Dashboard/trans_callback.html', context)

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
        'total_trans' : "{:.2f}".format(get_total_trans(request)),
    }
    return render(request, 'Dashboard/profile.html', context)

@login_required
def inbox(request):
    inboxes = Inbox.objects.all()
    context = {
        'inboxes' : inboxes,
        'total_trans' : "{:.2f}".format(get_total_trans(request)),
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
def terms_and_conditions(request):
    return render(request, 'Extras/terms_and_conditions.html')
def contact(request):
    print('contact')
        # if request.method == 'POST':
        #     email = request.POST.get('email')
        #     subject = request.POST.get('subject')
        # contact_mail = threading.Thread(target=send_contact_mail, args=(email,subject))
        # contact_mail.start()
    return render(request, 'Extras/contact.html')

# def send_contact_mail(email,subject):
#     print('me')
#     recipient =  'support@agrivestafrica.com'
#     subject = subject
#     sender = email
#     message = EmailMessage(subject, sender, [recipient])
#     message.send()

def how_to(request):
    return render(request, 'Extras/how_to.html')
def blog_soya(request):
    return render(request, 'Extras/blog_soya.html')

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

def logout_user(request):
    logout(request)
    return redirect('homepage')

def create_item(request, Obj):
    name = request.POST.get('name')
    position = request.POST.get('position')
    bio = request.POST.get('bio')
    image = request.FILES['image']
    Obj.objects.create(name=name, position=position, bio=bio, image=image)

def edit_item(request, item):
    form_type = request.POST.get('type')
    if form_type == 'delete':
        item.delete()
    else:
        name = request.POST.get('name')
        position = request.POST.get('position')
        bio = request.POST.get('bio')            
        item.name = name
        item.position = position
        item.bio = bio
        if 'image' in request.FILES:
            image = request.FILES['image']
            item.image = image
        item.save()

def cms_team(request):
    context = {
        'teams' : Team.objects.all()
    }
    return render(request, 'Cms/team.html', context)

def cms_add_team(request):
    if request.method == 'POST':
        create_item(request, Team)
        return redirect('cms_team_page')
    return render(request, 'Cms/add_team.html')

def cms_edit_team(request, id):
    team = Team.objects.get(id=id)
    if request.method == 'POST':
        edit_item(request, team)
        return redirect('cms_team_page')
    context = {
        'team' : team
    }
    return render(request, 'Cms/edit_team.html', context)

def cms_board(request):
    context = {
        'boards' : Board.objects.all()
    }
    return render(request, 'Cms/board.html', context)

def cms_add_board(request):
    if request.method == 'POST':
        create_item(request, Board)
        return redirect('cms_board_page')
    return render(request, 'Cms/add_board.html')

def cms_edit_board(request, id):
    board = Board.objects.get(id=id)
    if request.method == 'POST':
        edit_item(request, board)
        return redirect('cms_board_page')
    context = {
        'board' : board
    }
    return render(request, 'Cms/edit_board.html', context)

def cms_advisor(request):
    context = {
        'advisors' : Advisor.objects.all()
    }
    return render(request, 'Cms/advisor.html', context)

def cms_add_advisor(request):
    if request.method == 'POST':
        create_item(request, Advisor)
        return redirect('cms_advisor_page')
    return render(request, 'Cms/add_advisor.html')

def cms_edit_advisor(request, id):
    advisor = Advisor.objects.get(id=id)
    if request.method == 'POST':
        edit_item(request, advisor)
        return redirect('cms_advisor_page')
    context = {
        'advisor' : advisor
    }
    return render(request, 'Cms/edit_advisor.html', context)

import requests
from uuid import uuid4

def testpay(request):
    url = "https://smp.hubtel.com/api/merchants/2017026/send/mobilemoney"
    token = str(uuid4())
    payload = json.dumps({
        "RecipientName":"Joe Doe",
        "RecipientMsisdn":"233558420368",
        "CustomerEmail": "recipient@gmail.com",
        "Channel":"mtn-gh",
        "Amount":1,
        "PrimaryCallbackUrl":"https://www.google.com/",
        "Description": "Withdrawal",
        "ClientReference":token
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic TjhaWlBtODoxZThiYmI5NzFmMmE0ZmI3OGYwNjIwYzFjMTU0NmYxMg=='
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # url = "https://webhook.site/73db4705-d87a-4177-913b-ec42533f51c2"

    # payload = {}
    # headers = {}
    # response = requests.request("POST", url, headers=headers, data=payload)

    context = {
        'info' : response.status_code
    }
    
    return render(request, 'testpay.html', context)


