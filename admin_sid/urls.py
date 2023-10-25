from django.urls import path
from . import views



urlpatterns = [
    
    path("admin_dsh",views.admin_dsh,name='admin_dsh'),
    path("show_prodect",views.show_prodect,name='show_prodect'),
    path("edit_prodect/<int:uid>",views.edit_prodect,name='edit_prodect'),
    path("view_prodect/<int:uid>",views.view_prodect,name='view_prodect'),
    path("add_prodect",views.add_prodect,name='add_prodect'),
    path("show_user",views.show_user,name='show_user'),
    path('customeraction/<int:uid>/', views.customeraction, name='customeraction'),
    path('add_prodect_action', views.add_prodect_action, name='add_prodect_action'),

   
]