from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .utils import send_otp
import pyotp
from datetime import datetime
from django.views.decorators.cache import never_cache
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from admin_sid.models import *

# Create your views here.


            



@never_cache
def home(request):
    product = Product.objects.all()
    return render(request,"app/home.html",{'product':product})



def sign_up(request):
    return render(request, 'app/usersignup.html')


def signup_perform(request):
    if request.method == 'POST':
        first_name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exists')
            return redirect('sign_up')
        elif User.objects.filter(username=username).exists():
            messages.error(request, ':Username is already exists')
            return redirect('sign_up')
        else:
            if password_1 == password_2:
                request.session['mail'] = email
                request.session['user_data'] = {
                    'username': username,
                    'first_name': first_name,
                    'email': email,
                    'password': password_1
                }
                send_otp(request)
                return redirect('otp')
            else:
                messages.error(request, "Password doesn't match")
                return redirect('sign_up')
    else:
        messages.error(request, 'Method not allowed')
        return redirect('sign_up')


def otp(request):
    return render(request, 'app/otp.html')


def otp_perform(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_data = request.session.get('user_data')
        otp_key = request.session.get('otp_key')
        otp_valid = request.session.get('otp_valid')
        if otp_key and otp_valid is not None:
            valid_otp = datetime.fromisoformat(otp_valid)
            print(otp_valid)
            if valid_otp > datetime.now():
                totp = pyotp.TOTP(otp_key, interval=60)
                if totp.verify(otp):
                    user = User.objects.create_user(**user_data)
                    request.session['user'] = user.email
                    login(request, user)
                    clear_session(request)
                    return redirect('user_login')
                else:
                    messages.error(request, 'OTP invalid')
                    return redirect('otp')
            else:
                clear_session(request)
                messages.error(request, 'OTP expired')
                return redirect('sign_up')
        else:
            clear_session(request)
            messages.error(request, 'Didnt get any otp')
            return redirect('sign_up')
    else:
        clear_session(request)
        return redirect('sign_up')


def clear_session(request):
    key = ['otp_key', 'otp_valid', 'user_data','mail']
    for key in key:
        if key in request.session:
            del request.session[key]
    

def user_login(request):
    return render(request,'app/userlogin.html')

    
def login_perform(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            if User.objects.get(username=username).is_active:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_superuser:
                        login(request, user)
                        return redirect('admin_dsh')
                    else:
                        login(request, user)
                        return redirect('home')
                else:
                    messages.error(request, "Username or password is incorrect")
                    return redirect('home')
            else:
                messages.error(request, "User is Blocked")
                return redirect('user_login')
        else:
            messages.error(request,"User doesn't exists")
            return redirect('user_login')
    else:
        return redirect('user_login')


@never_cache
def home_perform(request):
    # Your view logic for the home page here
    if not request.user.is_authenticated:
        return render(request, 'app/userlogin.html')
    else:
        return redirect('home')

@never_cache    
def rubik_3(request):
    product = Product.objects.all()
    return render(request,'app/3x3rubiks.html',{'product':product})
   

@never_cache    
def view_product(request,pid):
    vi_product = Product.objects.get(id=pid)
    return render(request,'app/view_product.html',{'vi_product':vi_product})
    

def log_out(request):
    request.session.flush() 
    logout(request)
    return redirect('home')



