from django.shortcuts import render, redirect

from orders.models import Order, OrderItem
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
        return redirect('home')
@never_cache
def show_category(request):
    if request.user.is_authenticated:
        category = Category.objects.all()
        return render(request,'admin/show_category.html',{'category':category})
    else:
        return redirect('home')
    
@never_cache
def add_category(request):
    if request.user.is_authenticated:
        return render(request,'admin/add_category.html')
    else:
        return redirect('home')


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

@never_cache
def edit_category(request,cid):
    if request.user.is_authenticated:
        category = Category.objects.get(id=cid)
        return render(request,'admin/edit_category.html', {'category':category})
    else:
        return redirect ('home')

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
    


@never_cache
def show_brand(request):
    if request.user.is_authenticated:
        brand = Brand.objects.all()
        return render(request,'admin/show_brand.html',{'brand':brand})
    else:
        return redirect('home')
    
@never_cache
def add_brand(request):
    if request.user.is_authenticated:
        return render(request,'admin/add_brand.html')
    else:
        return redirect('home')


def add_brand_action(request):
    if request.method == 'POST':
        new_brand = request.POST.get('new_brand')
        existing_brand = Brand.objects.filter(title=new_brand)

        if existing_brand.exists():
            messages.error(request, 'Brand already exists')
            return redirect('add_brand')
        else:
            brand = Brand(title=new_brand)
            brand.save()
    return redirect('show_brand')

@never_cache
def edit_brand(request,bid):
    if request.user.is_authenticated:
        brand = Brand.objects.get(id=bid)
        return render(request,'admin/edit_brand.html', {'brand':brand})
    else:
        return redirect('home')

def edt_brand_action(request):
    if request.method== 'POST':
        id = request.POST.get('id')
        name = request.POST.get('editbrand')
        existing_brand = Brand.objects.filter(title=name)
        if existing_brand.exists():
            messages.error(request, 'Brand already exists')
            return redirect('edit_brand')
        else:
            brand = Brand.objects.get(id=id)
            brand.title = name
            brand.save()
            return redirect('show_brand')




@never_cache 
def show_product(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        return render(request,'admin/show_product.html',{'products':products})
    else:
        return redirect('home')
    
@never_cache
def admin_view_product(request,uid):
    if request.user.is_authenticated:
        products = Product.objects.get(id=uid)
        return render(request, 'admin/view_products.html',{'products':products})
    else:
        return redirect('home')


@never_cache
def edit_product(request, uid):
    if request.user.is_authenticated:
        product = Product.objects.get(id=uid)
        category = Category.objects.all()
        brand = Brand.objects.all()
        return render(request,'admin/edit_product.html', {'product': product, 'category': category, 'brand':brand})
    else:
        return redirect('home')

def edit_product_action(request):
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


            product = Product.objects.get(id=id)

            product.name = name
            product.description = description
            product.stock = stock
            try:
                price_float = float(price1)
                if price_float >= 0:
                    product.price = price_float
            except ValueError:
                # Handle invalid input for price1
                pass

            try:
                old_price_float = float(price2)
                if old_price_float >= 0:
                    product.old_price = old_price_float
            except ValueError:
                # Handle invalid input for price2
                pass
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
            return redirect('show_product')
        else:
            return redirect('show_product')
    else:
        return redirect('home')

@never_cache
def add_product(request):
    if request.user.is_authenticated:
        category = Category.objects.all()
        brand = Brand.objects.all()
        context = {
            'category':category,
            'brand':brand
        }
        return render(request,'admin/add_product.html',context)
    else:
        return redirect('home')

def add_product_action(request):
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
            product = Product(title=name,brand_id=brand,category_id=category,price=price,old_price =old_price, stock=stock,description=description,image1=img1,image2=img2,image3=img3,image4=img4)
            product.save()
            return redirect('show_product')
        else:
            return redirect('show_product')
    else:
        return redirect('home')





# def block_product(request, uid):
#     product = Product.objects.get(id=uid)
#     if product.active:
#         product.active = False
#     else:
#         product.active = True
#     product.save()
#     return redirect('admproduct')


@never_cache
def show_user(request):
    if request.user.is_authenticated:
        users= User.objects.all().exclude(is_superuser=True)
        return render(request,'admin/show_user.html',{'users':users})
    else:
        return redirect('home')



def customeraction(request, uid):
    if request.user.is_authenticated:
        customer = User.objects.get(id=uid)
        if customer.is_active:
            customer.is_active = False
            print(customer.is_active)
        else:
            customer.is_active = True
        customer.save()
        return redirect('show_user')
    else:
        return redirect('home')
    
def product_action(request, uid):
    product = Product.objects.get(id=uid)
    if product.active:
        product.active = False
    else:
        product.active = True
    product.save()
    return redirect('show_product')


def category_action(request, cid):
    category = Category.objects.get(id=cid)
    if category.active:
        category.active = False
    else:
        category.active = True
    category.save()
    return redirect('show_category')


def brand_action(request, bid):
    brand = Brand.objects.get(id=bid)
    if brand.active:
        brand.active = False
    else:
        brand.active = True
    brand.save()
    return redirect('show_brand')

def order(request):

    
    orders= OrderItem.objects.all()
    
    
    return render(request, 'admin/admin_order.html', {'orders': orders})



