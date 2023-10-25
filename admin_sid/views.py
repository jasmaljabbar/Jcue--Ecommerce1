from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User

# Create your views here.
def admin_dsh(request):
    if request.user.is_authenticated:
        return render(request,"admin/admin_dsh.html")
    else:
        return render(request,'app/home_all.html')
    
def show_prodect(request):
    prodects = Prodect.objects.all()
    return render(request,'admin/show_prodect.html',{'prodects':prodects})

def view_prodect(request,uid):
    prodects = Prodect.objects.get(id=uid)
    return render(request, 'admin/view_prodects.html',{'prodects':prodects})



def edit_prodect(request, uid):
    product = Prodect.objects.get(id=uid)
    category = Category.objects.all()
    brand = Brand.objects.all()
    return render(request,'admin/edit_prodect.html', {'product': product, 'category': category, 'brand':brand})

def edit_prodect_action(request,uid):
    return redirect('edit_prodect')

def add_prodect(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    context = {
        'category':category,
        'brand':brand
    }
    return render(request,'admin/add_prodect.html',context)

def add_prodect_action(request):
    if request.method == 'POST':
        title = request.POST['name']
        category = request.POST['category']
        brand = request.POST['brand']
        image1 = request.FILES['img1']
        image2 = request.FILES['img2']
        image3 = request.FILES['img3']
        image4 = request.FILES['img4']
        description = request.POST['description']
        price = request.POST ['price1']
        old_price = request.POST ['price2']
        stock = request.POST ['stock']
        p = Prodect.objects.create(title=title,
                               category_id=category,
                               brand_id=brand,
                               image1=image1,
                               image2=image2,
                               image3=image3,
                               image4=image4,
                               description=description,
                               price=price,
                               old_price=old_price,
                               stock=stock)
    print(p)
    return redirect('show_prodect')




def show_user(request):
    users= User.objects.all().exclude(is_superuser=True)
    return render(request,'admin/show_user.html',)



def customeraction(request, uid):
    print(uid)
    customer = User.objects.get(id=uid)
    print(customer.get_full_name)
    if customer.is_active:
        customer.is_active = False
        print(customer.is_active)
    else:
        customer.is_active = True
    customer.save()
    return redirect('show_user')

