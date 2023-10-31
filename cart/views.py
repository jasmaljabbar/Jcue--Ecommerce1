from django.shortcuts import render
from cart.cart import Cart
from admin_sid.models import Product

# Create your views here.

def cart(request):
    return render(request,'cart/cart.html')

def add_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return render(request,'cart/manu_cart.html' )

