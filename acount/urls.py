from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('signup_perform', views.signup_perform, name='signup_perform'),
    path('otp', views.otp, name='otp'),
    path('otp_perform', views.otp_perform, name='otp_perform'),
    path('user_login', views.user_login, name='user_login'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('for_otp', views.for_otp, name='for_otp'),
    path('forget_password_action', views.forget_password_action, name='forget_password_action'),
    path('forget_otp', views.forget_otp, name='forget_otp'),
    path('new_password', views.new_password, name='new_password'),
    path('category_search/<int:uid>', views.category_search, name='category_search'),
    path('search', views.search, name='search'),
    path('price_filter', views.price_filter, name='price_filter'),
    path('view_product/<int:pid>', views.view_product, name='view_product'),
    path('userprofile', views.userprofile, name='userprofile'),  # Updated URL pattern
    path('edit_profile', views.edit_profile, name='edit_profile'),  #  URL pattern
    path('edit_profileaction', views.edit_profileaction, name='edit_profileaction'), 
    path('log_out', views.log_out, name='log_out'),
    path('login_perform', views.login_perform, name='login_perform'),
]
