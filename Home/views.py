from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import math
from Log.models import User,Sponsor,Farmer,Offtaker
from Asset.models import Trade


def home(request):
    logout(request)
    trades = Trade.objects.all()
    sliderT = Trade.objects.all().order_by('-id')[:3]
    x = (Trade.objects.all().count() / 3)
    slide1 = Trade.objects.all().order_by('-id')[x*2:x*3]
    slide2 = Trade.objects.all().order_by('-id')[x:x*2]
    slide3 = Trade.objects.all().order_by('-id')[:x]

    min_slide1 = Trade.objects.last()
    min_slide2 = Trade.objects.all()[:1]
    min_slide3 = Trade.objects.all()[1:2]
    min_slide4 = Trade.objects.all()[2:3]
    min_slide5 = Trade.objects.all()[3:4]
    min_slide6 = Trade.objects.all()[4:5]

    context = {
        'trades' : trades,
        'sliderT' : sliderT,
        'slide1' : slide1,
        'slide2' : slide2,
        'slide3' : slide3,
        'x' : x,
        'min_slide1' : min_slide1,
        'min_slide2' : min_slide2,
        'min_slide3' : min_slide3,
        'min_slide4' : min_slide4,
        'min_slide5' : min_slide5, 
        'min_slide6' : min_slide6
    }
    return render(request,'index.html', context)


def check_job(request):
    if Sponsor.objects.filter(user=request.user).exists():
        print('sponsor')
    elif Farmer.objects.filter(user=request.user).exists():
        print('farmer')
    elif Offtaker.objects.filter(user=request.user).exists():
        print('offtaker')

@login_required
def dashboard(request):
    return render(request,'Dashboard/dashboard.html')

@login_required
def profile(request):
    return render(request, 'Dashboard/profile.html')
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



