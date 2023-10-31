from django.urls import path
from cart.views import *


urlpatterns = [
    path('', cart, name='cart'),
    path('add_cart/<int:prodect_id', add_cart, name='add_cart'),

]