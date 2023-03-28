from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail,EmailMessage,get_connection
from django.template.loader import render_to_string
from django.conf import settings 
from random import randint
import threading
from .models import User, Sponsor, Farmer, Offtaker
from Cache.models import Password_Token

def welcome(request):
    return render(request, 'welcome.html')

def s_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if User.objects.filter(username=name).exists():
            messages.info(request, f"username already taken")
        elif User.objects.filter(email=email).exists():
            messages.info(request, f"email already registered with us")
        elif len(pass1) < 4:
            messages.info(request, f"password too short")
        elif pass1 != pass2:
                messages.info(request, f"Passwords don't match")
        else: 
            user = User()
            user.username = name
            user.email = email
            pass1_ = make_password(pass1)
            user.password = pass1_
            user.is_sponsor = True
            user.save()
            sponsor = Sponsor()
            sponsor.user = user
            res_email = user.email
            sponsor.save()
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')   
            welcome_mail = threading.Thread(target=send_welcome_mail, args=(name,res_email))
            welcome_mail.start()
            messages.success(request, 'Account Created Successfully')
            return redirect('dashboard')
    return render(request, 'registration/s_register.html')

def f_register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if User.objects.filter(username=name).exists():
            messages.info(request, f"username already taken")
        elif User.objects.filter(email=email).exists():
            messages.info(request, f"email already registered with us")
        elif len(pass1) < 4:
            messages.info(request, f"password too short")
        elif pass1 != pass2:
            messages.info(request, f"Passwords don't match")
        else:
            user = User()
            user.username = name
            user.email = email
            pass1_ = make_password(pass1)
            user.password = pass1_
            user.is_sponsor = True
            user.save()
            farmer = Farmer()
            farmer.user = user
            res_email = user.email
            farmer.save()
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')    
            welcome_mail = threading.Thread(target=send_welcome_mail, args=(name,res_email))
            welcome_mail.start()
            messages.success(request, 'Account Created Successfully')
            return redirect('dashboard')
    return render(request, 'registration/f_register.html')

def o_register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if User.objects.filter(username=name).exists():
            messages.info(request, f"username already taken")
        elif User.objects.filter(email=email).exists():
            messages.info(request, f"email already registered with us")
        elif len(pass1) < 4:
            messages.info(request, f"password too short")
        elif pass1 != pass2:
                messages.info(request, f"Passwords don't match")
        else:
            user = User()
            user.username = name
            user.email = email
            pass1_ = make_password(pass1)
            user.password = pass1_
            user.is_sponsor = True
            user.save()
            offtaker = Offtaker()
            offtaker.user = user
            res_email = user.email
            offtaker.save()
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')    
            welcome_mail = threading.Thread(target=send_welcome_mail, args=(name,res_email))
            welcome_mail.start()
            messages.success(request, 'Account Created Successfully')
            return redirect('dashboard')
    return render(request, 'registration/o_register.html')

def send_welcome_mail(name,res_email):
    info = {'username' : name}
    html_template = 'welcome.html'
    welcome_message = render_to_string(html_template, context=info)
    recipient = res_email
    subject = 'Welcome To AgriVest Africa'
    sender = 'support@agrivestafrica.com'
    message = EmailMessage(subject, welcome_message, sender, [recipient])
    message.content_subtype = 'html'
    message.send()

def login_user(request):
    if request.method == 'POST':
        user_username = request.POST.get('username')
        user_password = request.POST.get('pass1')
        print(user_username,user_password)
        if User.objects.filter(username=user_username).exists():
            user = authenticate(username=user_username, password=user_password)
            if user:
                if user.is_active:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('dashboard')
            else:
                messages.info(request, 'invalid credentials')
        elif User.objects.filter(email=user_username).exists():
            user_username = User.objects.get(email=user_username).username
            user = authenticate(username=user_username, password=user_password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
        else:
            messages.info(request, 'invalid credentials')
    return render(request, 'generic/login.html')

def logout_user(request):
    logout(request)
    return redirect('homepage')

def map(request):
    return render(request, 'map.html')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            email = User.objects.get(username=username).email
            mail_thread = threading.Thread(target=send_reset_email, args=(user,email))
            mail_thread.start()
            messages.info(request, f'An email has been sent to {email}')
        elif User.objects.filter(email=username).exists():
            user = User.objects.get(email=username)
            email = User.objects.get(email=username).email
            mail_thread = threading.Thread(target=send_reset_email, args=(user,email))
            mail_thread.start()
            messages.info(request, f'An email has been sent to {email}')
        else:
            messages.info(request, f'User does not exist, try again')
    return render(request, 'generic/forgot_password.html')

def send_reset_email(user,email):
    token = randint(1000,9999)
    pass_token = Password_Token()
    pass_token.user = user
    pass_token.token = token
    pass_token.save()
    link = f"https://agrivestafrica-production.up.railway.app/reset_password/{token}/"
    subject = 'Reset Password'
    html_template = 'generic/reset_mail.html'
    lis = {
        'link' : link,
        'token' : token
    }
    html_message = render_to_string(html_template, context=lis)
    mail_from = 'noreply@agrivestafrica.com'
    message = EmailMessage(subject, html_message, mail_from, [email])
    message.content_subtype = 'html'
    message.send()
    
def reset_password(request, token):
    pass_user = Password_Token.objects.get(token=token).user
    if request.method == 'POST':
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if len(pass1) < 4:
            messages.info(request, f'Password Too Weak')
        elif pass1 != pass2:
            messages.info(request, "Passwords don't match")
        else:
            user = User.objects.get(username=pass_user)
            user.password = make_password(pass1)
            user.save()
            Password_Token.objects.last().delete()
            return redirect('dashboard')
    return render(request, 'generic/reset_password.html')



def tes(request):
    context = {
        'token' : 0000
    }
    return render(request, 'generic/reset_mail.html')

import requests,json
def hubtel(request):
    url = "https://payproxyapi.hubtel.com/items/initiate"
    ref = randint(1000,9999)

    payload = json.dumps({
    "totalAmount": 1,
    "description": "Test with Joseph",
    "callbackUrl": "https://www.agrivestafrica.com/hub_call/",
    "returnUrl": "https://www.agrivestafrica.com/hub_call/",
    "merchantAccountNumber": "2017279",
    "cancellationUrl": "https://www.agrivestafrica.com/hub_cancel/",
    "clientReference": ref
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic UjZOeXlKUjpiN2E1ZjI5YTg0YTQ0NTRkYWYwMWE3NzllYWU1ZmZkMQ=='
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    context = {
        'response' : response.status_code,
        'res_text' : response.text
    }
    return render(request, 'hubtel.html', context)

def hub_call(request):
    return render(request, 'hub_call.html')

def hub_cancel(request):
    return render(request, 'hub_cancel.html')


from Asset.models import Trade
from django.core.paginator import Paginator

def temp(request):
    trades = Trade.objects.all().order_by('id')
    tradePages = Paginator(trades, 3)
    pageList = []
    for page in tradePages:
        pageList.append(page.object_list)
    context = {
        'pageList' : pageList
    }
    return render(request, 'registration/temp.html', context)