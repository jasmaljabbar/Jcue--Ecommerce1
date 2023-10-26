from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Category
from django.contrib import messages

# Create your views here.
@never_cache
def admin_dsh(request):
    if request.user.is_authenticated:
        return render(request,"admin/admin_dsh.html")
    else:
        return render(request,'app/home_all.html')

def show_category(request):
    category = Category.objects.all()
    return render(request,'admin/show_category.html',{'category':category})

def add_category(request):
    return render(request,'admin/add_category.html')


def add_category_action(request):
    if request.method == 'POST':
        new_category = request.POST.get('new_category')
        existing_category = Category.objects.filter(title=new_category)

        if existing_category.exists():
            messages.error(request, 'Category already exists')
            return redirect('add_category')
        else:
            category = Category(title=new_category)
            category.save()

    return redirect('show_category')


def edit_category(request,cid):
    if request.user.is_authenticated:
        category = Category.objects.get(id=cid)
        return render(request,'admin/edit_category.html', {'category':category})
    else:
        return render(request,'app/home_all.html')

def edt_category_action(request):
    if request.method== 'POST':
        id = request.POST.get('id')
        name = request.POST.get('newcategory')
        existing_category = Category.objects.filter(title=name)
        if existing_category.exists():
            messages.error(request, 'Category already exists')
            return redirect('add_category')
        else:
            category = Category.objects.get(id=id)
            category.title = name
            category.save()
            return redirect('show_category')
    
def dlt_category(request,cid):
    category =Category.objects.get(id=cid)
    category.delete()
    return redirect('show_category')
    
   
def show_prodect(request):
    if request.user.is_authenticated:
        prodects = Prodect.objects.all()
        return render(request,'admin/show_prodect.html',{'prodects':prodects})
    else:
        return render(request,'app/home_all.html')
    

def view_prodect(request,uid):
    if request.user.is_authenticated:
        prodects = Prodect.objects.get(id=uid)
        return render(request, 'admin/view_prodects.html',{'prodects':prodects})
    else:
        return render(request,'app/home_all.html')



def edit_prodect(request, uid):
    if request.user.is_authenticated:
        product = Prodect.objects.get(id=uid)
        category = Category.objects.all()
        brand = Brand.objects.all()
        return render(request,'admin/edit_prodect.html', {'product': product, 'category': category, 'brand':brand})
    else:
        return render(request,'app/home_all.html')

def edit_prodect_action(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            id = request.POST.get('id')
            name = request.POST.get('name')
            description = request.POST.get('description')
            category = request.POST.get('category')
            brand = request.POST.get('brand')
            stock = request.POST.get('stock')
            price1 = request.POST.get('price1')
            price2 = request.POST.get('price2') 
            img1 = request.FILES.get('img1')
            img2 = request.FILES.get('img2')
            img3 = request.FILES.get('img3')
            img4 = request.FILES.get('img4')


            product = Prodect.objects.get(id=id)

            product.name = name
            product.description = description
            product.stock = stock
            product.price = price1
            product.old_price = price2
            product.category_id = category
            product.brand_id = brand

            if img1 is not None:
                product.image1 = img1
            if img2 is not None:
                product.image2 = img2
            if img3 is not None:
                product.image3 = img3
            if img4 is not None:
                product.image4 = img4

            # Save the updated product
            product.save()
            return redirect('show_prodect')
        else:
            return redirect('show_prodect')
    else:
        return render(request,'app/home_all.html')

def add_prodect(request):
    if request.user.is_authenticated:
        category = Category.objects.all()
        brand = Brand.objects.all()
        context = {
            'category':category,
            'brand':brand
        }
        return render(request,'admin/add_prodect.html',context)
    else:
        return render(request,'app/home_all.html')

def add_prodect_action(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name')
            description = request.POST.get('description')
            brand = request.POST.get('brand')
            category = request.POST.get('category')
            stock = request.POST.get('stock')
            price = request.POST.get('price1')
            old_price = request.POST.get('price2')
            img1 = request.FILES.get('img1')
            img2 = request.FILES.get('img2')
            img3 = request.FILES.get('img3')
            img4 = request.FILES.get('img4')
            product = Prodect(title=name,brand_id=brand,category_id=category,price=price,old_price =old_price, stock=stock,description=description,image1=img1,image2=img2,image3=img3,image4=img4)
            product.save()
            return redirect('show_prodect')
        else:
            return redirect('show_prodect')
    else:
        return render(request,'app/home_all.html')



def delete_prodect(request,uid):
    if request.user.is_authenticated:
        prodect = Prodect.objects.get(id=uid)
        prodect.delete()
        return redirect ('show_prodect')
    else:
        return render(request,'app/home_all.html')



def show_user(request):
    if request.user.is_authenticated:
        users= User.objects.all().exclude(is_superuser=True)
        return render(request,'admin/show_user.html',{'users':users})
    else:
        return render(request,'app/home_all.html')



def customeraction(request, uid):
    if request.user.is_authenticated:
        customer = User.objects.get(id=uid)
        print(customer.get_full_name)
        if customer.is_active:
            customer.is_active = False
            print(customer.is_active)
        else:
            customer.is_active = True
        customer.save()
        return redirect('show_user')
    else:
        return render(request,'app/home_all.html')
    


