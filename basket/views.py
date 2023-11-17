from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from admin_sid.models import Product
from basket.models import CartItem, WishItem


from .basket import Basket


def basket_summary(request):
    # Assuming the user is authenticated
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    context = {
        "cart_items": cart_items,
    }
    return render(request, "basket/summary.html", context)

def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        if product.stock >= product_qty:
            basket.add(product=product, qty=product_qty)
            basketqty = basket.__len__()
            response = JsonResponse({"qty": basketqty})
            return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        basket.delete(product=product_id)
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({"qty": basketqty, "subtotal": baskettotal})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        if product.stock >= product_qty:
            basket.update(product=product_id, qty=product_qty)

            basketqty = basket.__len__()
            basketsubtotal = basket.get_subtotal_price()
            basket_total = basket.get_total_price()
            productquantity = product_qty
            response = JsonResponse(
                {
                    "qty": basketqty,
                    "total": basket_total,
                    "subtotal": basketsubtotal,
                    "productquantity": productquantity,
                    "productStock": product.stock,
                }
            )
            return response


def add_to_wishlist(request, id):
    product = Product.objects.get(id=id)
    wish_item, created = WishItem.objects.get_or_create(
        user=request.user, product=product
    )
    if created:
        return redirect("home")
    else:
        return redirect("wishlist")


def wishlist(request):
    basket = Basket
    product = Product.objects.all()
    wish_items = WishItem.objects.filter(user=request.user)
    context = {
        "wish_items": wish_items,
        "product": product,
        "basket": basket,
    }
    return render(request, "basket/wishlist.html", context)


def remove_from_wishlist(request, id):
    try:
        item_to_remove = WishItem.objects.get(id=id)
        item_to_remove.delete()
        return redirect("basket:wishlist")
    except WishItem.DoesNotExist:
        return redirect("basket:wishlist")
