from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail,EmailMessage
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
        name = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if User.objects.filter(username=name).exists():
            messages.info(request, f"username already taken")
        elif User.objects.filter(email=email).exists():
            messages.info(request, f"email already registered with us")
        else:
            if len(pass1) < 4:
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
                sponsor.username = name
                sponsor.user = user
                res_email = user.email
                sponsor.save()
                if user.is_active:
                    authenticate(username=name,pasword=pass1)
                    login(request,user)   
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
        else:
            if len(pass1) < 4:
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
                farmer.username = name
                farmer.user = user
                res_email = user.email
                farmer.save()
                if user.is_active:
                    authenticate(username=name,pasword=pass1)
                    login(request,user)   
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
        else:
            if len(pass1) < 4:
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
                offtaker.username = name
                offtaker.user = user
                res_email = user.email
                offtaker.save()
                if user.is_active:
                    authenticate(username=name,pasword=pass1)
                    login(request,user)   
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
    sender = settings.EMAIL_HOST_USER
    message = EmailMessage(subject, welcome_message, sender, [recipient])
    message.content_subtype = 'html'
    message.send()

def login_user(request):
    if request.method == 'POST':
        user_username = request.POST.get('username')
        user_password = request.POST.get('pass1')
        if User.objects.filter(username=user_username).exists():
            user = authenticate(username=user_username, password=user_password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
            else:
                messages.info(request, 'invalid credentials')
        elif User.objects.filter(email=user_username).exists():
            user_username = User.objects.get(email=user_username).username
            user = authenticate(username=user_username, password=user_password)
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
            print('user non existent')
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
    mail_from = settings.EMAIL_HOST_USER
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