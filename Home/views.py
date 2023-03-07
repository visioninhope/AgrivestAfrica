from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import math
from Log.models import User,Sponsor,Farmer,Offtaker,Profile
from Transaction.models import TradeInvoice,TradeLog,TradeReceipt,FarmInvoice,FarmLog
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


#@login_required
def dashboard(request):
    context = {
        'trades' : TradeInvoice.objects.filter(customer=request.user),
        'farms' : FarmInvoice.objects.filter(customer=request.user)
    }
    return render(request,'Dashboard/dashboard.html', context)

#@login_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def trade_log(request):
    # trades = TradeInvoice.objects.filter(customer=request.user)
    trades = TradeInvoice.objects.all()
    pend_count = TradeInvoice.objects.filter(status='Pending').count()
    act_count = TradeInvoice.objects.filter(status='Active').count()
    comp_count = TradeInvoice.objects.filter(status='Completed').count()
    trades_bought = 0
    trades_sold = 0
    for trade in trades:
        trades_bought = trades_bought + trade.total_cost
        trades_sold = trades_sold + trade.actual_return
    trades_bal = "{:.2f}".format(trades_sold - trades_bought) 


    # if request.GET.get('checkoutid'):
    #     check_id = request.GET.get('checkoutid')
    #     trade_receipt = TradeReceipt.objects.get(check_id=check_id).trade
    #     trade_invoice = TradeInvoice.objects.get(trade_name=trade_receipt)
    #     trade_invoice.status = 'Active'
    #     trade_invoice.save()

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

#@login_required
def tradeLog_info(request,slug):
    trade = TradeInvoice.objects.get(slug=slug)
    context ={
        'trade' : trade
    }
    return render(request, 'Dashboard/tradeLog_info.html', context)

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

#@login_required
def farmLog_info(request,slug):
    farm = FarmInvoice.objects.get(slug=slug)
    context ={
        'farm' : farm
    }
    return render(request, 'Dashboard/farmLog_info.html', context)

from django.utils import timezone
#@login_required
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
        else:
            profile = Profile()
            profile.user = user
            profile.first_name = request.POST.get('first_name')
            profile.last_name = request.POST.get('last_name')
            profile.other_name = request.POST.get('other_name')
            profile.profile_pic = request.FILES.get('profile_pic')
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
            profile.id_pic_front = request.FILES.get('id_pic_front')
            profile.id_pic_back = request.FILES.get('id_pic_back')
            profile.last_updated = timezone.now()
            if request.POST.get('referral'):
                profile.referral_code = request.POST.get('referral')
            profile.save()
            return redirect('dashboard')
    context = {
        'pro_exists' : pro_exists,
        'pro_info' : pro_info,
    }
    return render(request, 'Dashboard/profile.html', context)


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

def sitemap(request):
    return render(request, 'sitemap.xml')


from rest_framework import generics
from rest_framework.views import APIView,Response
from .serializers import BagSerializer
from rest_framework.permissions import AllowAny


# @csrf_exempt
class EmptyView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = BagSerializer

    def get(self, request):
        return Response({'test':'good'})
    def post(self, request):
        return Response({'info':request.data})
