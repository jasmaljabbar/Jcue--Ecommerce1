from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .utils import send_otp
import pyotp
from datetime import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.


            

def home_all(request):
    return render(request,"app/home_all.html")

def home(request):
    if request.user.is_authenticated:

        return render(request,"app/home.html")
    else:
        return render(request,"app/home_all.html")



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
        digit1 = request.POST.get('digit1', '')
        digit2 = request.POST.get('digit2', '')
        digit3 = request.POST.get('digit3', '')
        digit4 = request.POST.get('digit4', '')
        digit5 = request.POST.get('digit5', '')
        digit6 = request.POST.get('digit6', '')

        combined_otp = digit1 + digit2 + digit3 + digit4 + digit5 + digit6
        otp = combined_otp
        user_data = request.session.get('user_data')
        otp_key = request.session.get('otp_key')
        otp_valid = request.session.get('otp_valid')
        if otp_key and otp_valid is not None:
            valid_otp = datetime.fromisoformat(otp_valid)
            if valid_otp > datetime.now():
                totp = pyotp.TOTP(otp_key, interval=60)
                if totp.verify(otp):
                    user = User.objects.create_user(**user_data)
                    request.session['user'] = user.email
                    login(request, user)
                    del request.session['otp_key']
                    del request.session['otp_valid']
                    del request.session['user_data']
                    del request.session['mail']
                    return redirect('user_login')
                else:
                    messages.error(request, 'OTP invalid')
                    return redirect('otp')
            else:
                messages.error(request, 'OTP expired')
                return redirect('sign_up')
        else:
            messages.error(request, 'Didnt get any otp')
            return redirect('sign_up')
    else:
        return redirect('sign_up')
    

def user_login(request):
    return render(request,'app/userlogin.html')

    
def login_perform(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin_dsh')
            else:
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect")
            return redirect('/')


@login_required
def home_perform(request):
    # Your view logic for the home page here
    if not request.user.is_authenticated:
        return render(request, 'app/userlogin.html')
    else:
        return render(request,'app/home_all.html')
    

def log_out(request):
    request.session.flush() 
    logout(request)
    return redirect('user_login')
