import json
from django.shortcuts import get_object_or_404
from admin_sid.models import Product
from basket.basket import Basket
from orders.models import Order, OrderItem
from payment.models import Address
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
import uuid
from datetime import datetime


def order_placed(request):
    return render(request, "payment/orderplaced.html")


def generate_order_key():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4().hex)[:6]  # Use the first 6 characters of a UUID
    order_key = f"ORDER-{timestamp}-{unique_id}"
    return order_key


@login_required
def address(request):
    billing_address = get_object_or_404(Address, user=request.user, flag=True)

    if request.method == "POST":
        basket = Basket(request)

        if billing_address:
            paymentmethod = request.POST.get("paymentMethod")
            total_paid = basket.get_total_price()
            order_key = generate_order_key()

            for item in basket.items:
                product = item.product
                if item.quantity > product.stock:
                    basket.clear()
                    billing_address = Address.objects.filter(user=request.user)
                    return render(
                        request,
                        "payment/address.html",
                        {
                            "message": f"Insufficient stock for {product.title}",
                            "billing_address": billing_address,
                        },
                    )

            if paymentmethod == "cod":
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
                    billing_status=paymentmethod,
                )

                order_id = order.pk

                for item in basket.items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.product.price,  # Update this line with the correct attribute
                        quantity=item.quantity,
                    )
                    product = item.product
                    product.stock -= item.quantity
                    product.save()

                basket.clear()

                return render(request, "payment/orderplaced.html")
            else:
                # Handle other payment methods if needed
                return render(request, "payment/UPI.html")

    billing_address = Address.objects.filter(user=request.user)
    return render(request, "payment/address.html", {"billing_address": billing_address})


def upi_paypal_com(request):
    billing_address = get_object_or_404(Address, user=request.user, flag=True)

    if request.method == "POST":
        basket = Basket(request)

        if billing_address:
            body = json.loads(request.body)
            paymentmethod = body.get("paymentmethod")
            print(paymentmethod)
            total_paid = basket.get_total_price()
            order_key = generate_order_key()

            for item in basket:
                product = item.product
                if item.quantity > product.stock:
                    basket.clear()
                    billing_address = Address.objects.filter(user=request.user)
                    return render(
                        request,
                        "payment/address.html",
                        {
                            "message": f"Insufficient stock for {product.title}",
                            "billing_address": billing_address,
                        },
                    )

            # Continue with the rest of your logic
            # ...

            # Continue with the rest of your logic
            # ...

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
                billing_status=paymentmethod,
            )

            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,  # Use item.product instead of item["product"]
                    price=item.subtotal_price,  # Adjust this if needed
                    quantity=item.quantity,  # Use item.quantity instead of item["qty"]
                )
                product = item.product
                product.stock -= item.quantity  # Use item.quantity instead of item["qty"]
                product.save()

            basket.clear()
    return JsonResponse("Payment completed", safe=False)



def address_active(request, aid):
    billing_address = Address.objects.get(id=aid)
    act_address = Address.objects.filter(flag=True).first()
    if act_address:
        act_address.flag = False
        act_address.save()
    if billing_address:
        billing_address.flag = True
        billing_address.save()

    messages.success(request, "Address set to default")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def add_address(request):
    if request.user.is_authenticated:
        return render(request, "payment/home.html")
    else:
        return redirect("home")


def edit_address(request, aid):
    if request.user.is_authenticated:
        address = Address.objects.get(id=aid)
        return render(request, "payment/edit_address.html", {"address": address})
    else:
        return redirect("home")


def edit_product_action(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            id = request.POST.get("id")
            custname = request.POST.get("custName", "")
            address1 = request.POST.get("custAdd", "")
            phone = request.POST.get("phone", "")
            state = request.POST.get("state", "")
            pincode = request.POST.get("pincode", "")

            address = Address.objects.get(id=id)

            address.full_name = custname
            address.address1 = address1
            address.phone = phone
            address.city = state
            address.post_code = pincode

            # Save the updated product
            address.save()
            billing_address = Address.objects.filter(user=request.user)
            return render(
                request, "payment/address.html", {"billing_address": billing_address}
            )
            # return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return redirect("address")
    else:
        return redirect("home")


@login_required
def delete_address(request, aid):
    address = Address.objects.get(id=aid)
    if address.user != request.user:
        messages.error(request, "You don't have permission to delete this address.")
        return redirect("payment:address")
    address.delete()
    messages.success(request, "Address deleted successfully.")

    return redirect("payment:BasketView")


@login_required
def BasketView(request):
    billing_address = Address.objects.filter(user=request.user)
    if request.method == "POST":
        custname = request.POST.get("custName", "")
        address1 = request.POST.get("custAdd", "")
        phone = request.POST.get("phone", "")
        state = request.POST.get("state", "")
        pincode = request.POST.get("pincode", "")
        addresses = Address.objects.all()
        if addresses:
            try:
                active_address = addresses.get(flag=True)
                active_address.flag = False
                active_address.save()
            except:
                pass

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
                flag=True,
            )

    return render(request, "payment/address.html", {"billing_address": billing_address})


# -----------------------------------------
def oreder_view(request):
    orders = Order.objects.filter(user=request.user)
    order_statuses = {order.id: order.status for order in orders}
    return render(
        request,
        "payment/orders.html",
        {"orders": orders, "order_statuses": order_statuses},
    )


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(
        request,
        "payment/order_detail.html",
        {"order": order, "order_items": order_items},
    )


def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order_items = order.items.all()

        for order_item in order_items:
            product = order_item.product
            product.stock += order_item.quantity
            product.save()

        order.status = "canceled"
        order.save()

        return render(request, "payment/order_detail.html", {"order": order})

    return render(request, "payment/order_detail.html", {"order": order})
