
from django.urls import path

from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket_summary, name='basket_summary'),
    path('add/', views.basket_add, name='basket_add'),
    path('delete/', views.basket_delete, name='basket_delete'),
    path('update/', views.basket_update, name='basket_update'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:id>', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:id>', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('basket/update/', views.basket_update, name='basket_update'),
]
