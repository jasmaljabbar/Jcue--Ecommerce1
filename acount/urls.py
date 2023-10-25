from django.urls import path
from . import views



urlpatterns = [
    path("",views.home_all),
    path("home",views.home,name='home'),
    path("sign_up",views.sign_up, name='sign_up'),
    path("signup_perform",views.signup_perform, name='signup_perform'),
    path("otp",views.otp, name='otp'),
    path("otp_perform",views.otp_perform, name='otp_perform'),
    path("user_login",views.user_login, name='user_login'),
    path("log_out",views.log_out, name='log_out'),
    path("login_perform",views.login_perform, name='login_perform'),


   
]