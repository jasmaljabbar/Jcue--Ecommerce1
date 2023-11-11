from django.shortcuts import get_object_or_404
from basket.basket import Basket
from orders.models import Order, OrderItem
from payment.models import Address
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
import uuid
from datetime import datetime





def order_placed(request):
    return render(request, 'payment/orderplaced.html')

def generate_order_key():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4().hex)[:6]  # Use the first 6 characters of a UUID
    order_key = f"ORDER-{timestamp}-{unique_id}"
    return order_key


@login_required
def address(request):
    
    billing_address = get_object_or_404(Address, user=request.user, flag=True)
    if request.method == 'POST':
        basket = Basket(request)
        
 
        if billing_address:
            paymentmethod = request.POST.get('paymentMethod')
            total_paid=basket.get_total_price()
            order_key=generate_order_key()
        
            if paymentmethod == 'cod':

                order = Order.objects.create(
                    user=request.user,
                    full_name=billing_address.full_name,
                    address1=billing_address.address1,
                    address2=billing_address.address2,
                    city=billing_address.city,
                    phone=billing_address.phone,
                    post_code=billing_address.post_code,
                    total_paid=total_paid,
                    order_key=order_key,
                    billing_status=False  
                )
                
                order_id = order.pk

   
                for item in basket:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['qty']
                    )

                
                basket.clear()

                return render(request, 'payment/orderplaced.html')

    return render(request, 'payment/address.html')


def address_active(request,aid):
    billing_address = Address.objects.get(id=aid)
    act_address = Address.objects.filter(flag=True).first()
    if act_address:
        act_address.flag = False
        act_address.save()
    if billing_address: 
        billing_address.flag = True
        billing_address.save()
    
    messages.success(request, 'Address set to default')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_address(request):
    if request.user.is_authenticated:
        return render(request,'payment/home.html')
    else:
        return redirect('home')
    
def edit_address(request, aid):
    if request.user.is_authenticated:
        address = Address.objects.get(id=aid)
        return render(request,'payment/edit_address.html', {'address':address})
    else:
        return redirect('home')

def edit_product_action(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            id = request.POST.get('id')
            custname = request.POST.get('custName', '')
            address1 = request.POST.get('custAdd', '')
            phone = request.POST.get('phone', '')
            state = request.POST.get('state', '')
            pincode = request.POST.get('pincode', '')

            address = Address.objects.get(id=id)

            address.full_name = custname
            address.address1 = address1
            address.phone = phone
            address.city = state
            address.post_code = pincode

            # Save the updated product
            address.save()
            billing_address = Address.objects.filter(user=request.user)
            return render(request, 'payment/address.html', {'billing_address': billing_address})
            # return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return redirect('address')
    else:
        return redirect('home')
    
@login_required
def delete_address(request, aid):

    address = Address.objects.get(id=aid)
    if address.user != request.user:
        messages.error(request, "You don't have permission to delete this address.")
        return redirect('payment:address')
    address.delete()
    messages.success(request, "Address deleted successfully.")
    return redirect('payment:address')


@login_required
def BasketView(request):
    billing_address = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        custname = request.POST.get('custName', '')
        address1 = request.POST.get('custAdd', '')
        phone = request.POST.get('phone', '')
        state = request.POST.get('state', '')
        pincode = request.POST.get('pincode', '')
        addresses = Address.objects.all()
        if addresses:
            active_address = addresses.get(flag=True)
            active_address.flag = False
            active_address.save()

        # Ensure the user is properly authenticated
        if request.user.is_authenticated:
            user = request.user
            
            Address.objects.create(
                user=user,
                full_name=custname,
                address1=address1,
                phone=phone,
                city=state,
                post_code=pincode,
                flag=True
            )
            
    return render(request, 'payment/address.html', {'billing_address': billing_address})



        






