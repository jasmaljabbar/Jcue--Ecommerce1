from django.urls import path

from . import views
from .views import BasketView
app_name = 'payment'

urlpatterns = [
    path('payment/address/', BasketView, name='basket_view'),
    path('order_placed/', views.order_placed, name='order_placed'),
    path('address/', views.address, name='address'),
    path('add_address/', views.add_address, name='add_address'),    
    path('edit_address/<int:aid>', views.edit_address, name='edit_address'),    
    path('edit_product_action', views.edit_product_action, name='edit_product_action'),    
    path('delete_address/<int:aid>', views.delete_address, name='delete_address'),    
]
 