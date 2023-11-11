from basket.basket import Basket
from payment.models import Address
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponseRedirect





def order_placed(request):
    return render(request, 'payment/orderplaced.html')




@login_required
def address(request):
    try:
        billing_address = Address.objects.filter(user=request.user)
    except billing_address.DoesNotExist:
        return render(request,'payment/home.html')  # Redirect to the login page
    
    if request.method == 'POST':
        basket = Basket(request)
        paymentmethod = request.POST.get('paymentMethod')
        if paymentmethod == 'cod':
            basket.clear()
            return render(request,'payment/orderplaced.html')

    return render(request, 'payment/address.html', {'billing_address': billing_address})

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
    if request.method == 'POST':
        custname = request.POST.get('custName', '')
        address1 = request.POST.get('custAdd', '')
        phone = request.POST.get('phone', '')
        state = request.POST.get('state', '')
        pincode = request.POST.get('pincode', '')
        

        # Ensure the user is properly authenticated
        if request.user.is_authenticated:
            user = request.user
            Address.objects.create(
                user=user,
                full_name=custname,
                address1=address1,
                phone=phone,
                city=state,
                post_code=pincode
            )
            billing_address = Address.objects.filter(user=request.user)
    return render(request, 'payment/address.html', {'billing_address': billing_address})



        






