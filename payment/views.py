from django.shortcuts import render

from store.views import Product
from . models import ShippingAddress, Order, OrderItem, Status
from cart.cart import Cart
from django.http import JsonResponse
import logging

# Create your views here.


def checkout(request):
    # Users with accounts -- pre-filled the form
    if request.user.is_authenticated:
        try:
            # Authenticated users with shipping information
            shipping_address = ShippingAddress.objects.get(
                user=request.user.id)
            context = {'shipping': shipping_address}
            logging.warning(shipping_address)
            return render(request, 'payment/checkout.html', context=context)

        except:
            # Auntenticated users with no shipping information
            return render(request, 'payment/checkout.html')

    else:
        # Guest users
        return render(request, 'payment/checkout.html')


def complete_order(request):
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # All in one shipping address
        shipping_address = (address1 + "\n" + address2 +
                            "\n" + city + "\n" + state + "\n" + zipcode)

        # Shopping cart information
        cart = Cart(request)

        # get total price of items
        total_cost = cart.get_total()

        # 1) Create order ->Account users with and without shipping information
        if request.user.is_authenticated:
            order = Order.objects.create(
                # 1st parameter is from model, 2nd is from backend
                full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost, user=request.user)
            order_id = order.pk
            for item in cart:
                orderitem = OrderItem.objects.create(
                    order_id=order_id, product=item['product'], quantity=item['qty'], price=item['price'], total=item['total'], user=request.user, status=Status.objects.first())
                product = orderitem.product
                product.quantity = product.quantity-item['qty']
                logging.warning(product)
                product.save()
        # 2) Create order ->Guest users without an account
        else:
            order = Order.objects.create(
                # 1st parameter is from model, 2nd is from backend
                full_name=name, email=email, shipping_address=shipping_address, amount_paid=total_cost)
            order_id = order.pk
            for item in cart:
                orderitem = OrderItem.objects.create(
                    order_id=order_id, product=item['product'], quantity=item['qty'], price=item['price'], total=item['total'], status=Status.objects.first())
                product = orderitem.product
                product.quantity = product.quantity-item['qty']
                logging.warning(product)
                product.save()

        order_success = True
        response = JsonResponse({'success': order_success})
        return response


def payment_success(request):
    # clear shopping cart
    for key in list(request.session.keys()):
        if key == 'session_key':  # refer to cart.py 'session_key'
            del request.session[key]

    return render(request, 'payment/payment-success.html')


def payment_failed(request):
    return render(request, 'payment/payment-failed.html')
