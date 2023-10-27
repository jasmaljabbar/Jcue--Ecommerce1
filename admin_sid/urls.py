from django.urls import path
from . import views



urlpatterns = [
    
    path("admin_dsh",views.admin_dsh,name='admin_dsh'),
    path("show_category",views.show_category,name='show_category'),
    path("add_category",views.add_category,name='add_category'),
    path("add_category_action",views.add_category_action,name='add_category_action'),
    path("edit_category/<int:cid>",views.edit_category,name='edit_category'),
    path("edt_category_action",views.edt_category_action,name='edt_category_action'),
    path("dlt_category/<int:cid>",views.dlt_category,name='dlt_category'),
    path("show_brand",views.show_brand,name='show_brand'),
    path("add_brand",views.add_brand,name='add_brand'),
    path("add_brand_action",views.add_brand_action,name='add_brand_action'),
    path("edit_brand/<int:bid>",views.edit_brand,name='edit_brand'),
    path("edt_brand_action",views.edt_brand_action,name='edt_brand_action'),
    path("dlt_brand/<int:bid>",views.dlt_brand,name='dlt_brand'),
    path("show_prodect",views.show_prodect,name='show_prodect'),
    path("edit_prodect/<int:uid>",views.edit_prodect,name='edit_prodect'),
    path("edit_prodect_action",views.edit_prodect_action,name='edit_prodect_action'),
    path("delete_prodect/<int:uid>",views.delete_prodect,name='delete_prodect'),
    path("view_prodect/<int:uid>",views.view_prodect,name='view_prodect'),
    path("add_prodect",views.add_prodect,name='add_prodect'),
    path("show_user",views.show_user,name='show_user'),
    path('customeraction/<int:uid>/', views.customeraction, name='customeraction'),
    path('add_prodect_action', views.add_prodect_action, name='add_prodect_action'),
]