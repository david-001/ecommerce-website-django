import csv
from django.db.models import Q
from django.shortcuts import render, redirect
from account.models import Retailer

from store.models import Product

from . forms import CreateUserForm, LoginForm, ProductForm, UpdateUserForm
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem, Status
from store.models import Category
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site

from . token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from . decorators import allowed_users
from django.core.files.storage import FileSystemStorage

import logging

# Create your views here.
# Refer to urls.py and templates/account


def register(request):
    return render(request, 'account/registration/register.html')


def register_action(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create(
                username=username, email=email, password='')
            user.set_password(password)
            user.is_active = False
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            user.save()
            # email verification setup
            current_site = get_current_site(request)
            subject = 'Account verification email'
            message = render_to_string(
                'account/registration/email-verification.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': user_tokenizer_generate.make_token(user),
                })
            user.email_user(subject=subject, message=message)
            messages.success(request, "User Added!")
            response = HttpResponse({'success': 'Successfully added user'})
            return response


def email_verification(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)
    # Success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')
    # Failed
    else:
        return redirect('email-verification-failed')


def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')


def email_verification_failed(request):
    return render(request, 'account/registration/email-verification-failed.html')


def my_login(request):
    return render(request, 'account/my-login.html')


def my_login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponse({'success': 'Successfully logged in'})


# Logout
def user_logout(request):
    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            else:
                del request.session[key]
    except KeyError:
        pass
        # auth.logout(request)
    messages.success(request, "Logout success")
    return redirect("store")


@login_required(login_url='my-login')
def dashboard(request):
    return render(request, 'account/dashboard.html')


@login_required(login_url='my-login')
def profile_management(request):
    return render(request, 'account/profile-management.html')


@login_required(login_url='my-login')
def profile_management_action(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        user = request.user
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Email already exists')
        else:
            user.username = username
            user.email = email
            user.save()
            messages.info(request, "Account updated")
            return redirect('dashboard')


@login_required(login_url='my-login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        messages.error(request, "Account deleted")
        return redirect('store')
    return render(request, 'account/delete-account.html')


# Shipping view
@login_required(login_url='my-login')
def manage_shipping(request):
    try:
        # Account user with shipment information
        shipping = ShippingAddress.objects.get(user=request.user.id)
    except ShippingAddress.DoesNotExist:
      # Account user with no shipment information
        shipping = None
    context = {'shipping': shipping}
    return render(request, 'account/manage-shipping.html', context)


def manage_shipping_action(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        user = request.user
        if ShippingAddress.objects.filter(user=user).exists():
            shippingaddress = ShippingAddress.objects.filter(user=user)
            shippingaddress.full_name = full_name
            shippingaddress.email = email
            shippingaddress.address1 = address1
            shippingaddress.address2 = address2
            shippingaddress.city = city
            shippingaddress.state = state
            shippingaddress.zipcode = zipcode
            shippingaddress.save()
        else:
            shippingaddress = ShippingAddress.objects.create(
                full_name=full_name, email=email, address1=address1, address2=address2, city=city, state=state, zipcode=zipcode, user=user)
            shippingaddress.save()
        messages.success(request, "Shipping address updated!")
        response = HttpResponse(
            {'success': 'Successfully updated shipping address'})
        return response


@login_required(login_url='my-login')
def track_orders(request):
    try:
        orders = OrderItem.objects.filter(user=request.user)
        context = {'orders': orders}
        return render(request, 'account/track-orders.html', context=context)
    except:
        return render(request, 'account/track-orders.html')


# Admin login
def admin_login(request):
    return render(request, 'account/admin-login.html')


def admin_login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponse({'success': 'Successfully logged in'})


# Admin logout
def admin_logout(request):
    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            else:
                del request.session[key]
    except KeyError:
        pass
        # auth.logout(request)
    messages.success(request, "Logout success")
    return redirect("admin-login")

# Admin dashboard


@allowed_users(allowed_roles=['admin'])
def admin_dashboard(request):
    orderitems = OrderItem.objects.all()
    customers = User.objects.filter(groups__name='customer')
    categories = Category.objects.all()
    products = Product.objects.all()
    retailers = User.objects.filter(groups__name='retailer')

    context = {'orderitems': orderitems, 'customers': customers, 'products': products,
               'categories': categories, 'retailers': retailers}

    return render(request, 'account/admin-dashboard.html', context)


# Admin customer profile
@allowed_users(allowed_roles=['admin'])
def admin_customer_profile(request, uid):
    user = User.objects.get(pk=uid)
    try:
        shipping = ShippingAddress.objects.get(user=user)
    except ShippingAddress.DoesNotExist:
        shipping = None
    context = {'shipping': shipping}
    return render(request, 'account/admin-customer-profile.html', context)


@allowed_users(allowed_roles=['admin'])
def admin_retailer_profile(request, uid):
    retailer = User.objects.get(pk=uid)
    products = Product.objects.filter(retailer=retailer)
    orderitems = OrderItem.objects.all()
    retailerorderitems = []
    for orderitem in orderitems:
        if orderitem.product.retailer == retailer:
            retailerorderitems.append(orderitem)
    try:
        details = Retailer.objects.get(user=retailer)
    except Retailer.DoesNotExist:
        details = None
    context = {'retailerorderitems': retailerorderitems,
               'products': products, 'details': details}
    return render(request, 'account/admin-retailer-profile.html', context)


@allowed_users(allowed_roles=['admin'])
def admin_download_orders(request):
    orderitems = OrderItem.objects.all()
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="orders.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Customer', 'Product', 'Retailer',
                    'Units Sold', 'Total Cost', 'Status', 'Date Ordered'])
    for orderitem in orderitems:
        writer.writerow(
            [orderitem.user.username, orderitem.product, orderitem.product.retailer, orderitem.quantity, orderitem.total, orderitem.status, orderitem.order.date_ordered])
    return response


# Admin delete category
@allowed_users(allowed_roles=['admin'])
def admin_delete_category(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.error(request, "Category deleted")
        return redirect('admin-dashboard')
    context = {'name': category.name}
    return render(request, 'account/admin-delete-category.html', context=context)


# Admin add category
@allowed_users(allowed_roles=['admin'])
def admin_add_category(request):
    name = request.POST.get('categoryname')
    logging.warning(name)
    category = Category.objects.create(name=name)
    category.save()
    messages.success(request, "Category added!")
    response = HttpResponse(
        {'success': 'Successfully added category'})
    return response


# Admin approve retailer
@allowed_users(allowed_roles=['admin'])
def admin_approve_retailer(request, pk):
    retailer = User.objects.get(pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        retailer.is_active = status
        retailer.save()
    statuses = [True, False]
    context = {'statuses': statuses, 'retailer': retailer}
    return render(request, 'account/admin-approve-retailer.html', context=context)


# Retailer register
def retailer_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create(
                username=username, email=email, password='')
            user.set_password(password)
            user.is_active = False
            group = Group.objects.get(name='retailer')
            user.groups.add(group)
            user.save()
            # email verification setup
            current_site = get_current_site(request)
            subject = 'Approve retailer account email'
            message = render_to_string(
                'account/registration/email-admin-approval.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': user_tokenizer_generate.make_token(user),
                })
            # Email to admin
            adminuser = User.objects.get(id=1)
            logging.warning(adminuser.email)
            adminuser.email_user(subject=subject, message=message)
            messages.success(request, "User Added!")
            response = HttpResponse({'success': 'Successfully added user'})
            return response
    return render(request, 'account/retailer-register.html')


# Retailer account approval
def email_admin_approval(request, uidb64, token):
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)
    # Success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-retailer-success')
    # Failed
    else:
        return redirect('email-retailer-failed')


def email_retailer_sent(request):
    return render(request, 'account/registration/email-retailer-sent.html')


def email_retailer_success(request):
    return render(request, 'account/registration/email-retailer-success.html')


def email_retailer_failed(request):
    return render(request, 'account/registration/email-retailer-failed.html')


def email_retailer_acl(request):
    return render(request, 'account/registration/email-await-approval.html')


def retailer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponse({'success': 'Successfully logged in'})
    return render(request, 'account/retailer-login.html')


# Retailer Logout
def retailer_logout(request):
    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            else:
                del request.session[key]
    except KeyError:
        pass
        # auth.logout(request)
    messages.success(request, "Logout success")
    return redirect("retailer-login")


@allowed_users(allowed_roles=['retailer'])
def retailer_dashboard(request):
    retailer = User.objects.get(id=request.user.id)
    products = Product.objects.filter(retailer=retailer)
    orderitems = OrderItem.objects.all()
    retailerorderitems = []
    for orderitem in orderitems:
        if orderitem.product.retailer == retailer:
            retailerorderitems.append(orderitem)
    try:
        details = Retailer.objects.get(user=retailer)
    except Retailer.DoesNotExist:
        details = None
    context = {'retailerorderitems': retailerorderitems,
               'products': products, 'details': details, 'retailer': retailer}
    return render(request, 'account/retailer-dashboard.html', context)


@allowed_users(allowed_roles=['retailer'])
def retailer_profile(request, uid):
    try:
        # Account retailer with product
        user = User.objects.get(pk=uid)

    except User.DoesNotExist:
        # Account retailer with no product
        user = None

    if Retailer.objects.filter(user=user).exists():
        retailer = Retailer.objects.get(user=user)
    else:
        retailer = None
    context = {'retailer': retailer, 'user': user}
    # logging.warning(retailer.address)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        open_time = request.POST.get('open_time')
        close_time = request.POST.get('close_time')
        address = request.POST.get('address')
        account_type = request.POST.get('account_type')
        account_number = request.POST.get('account_number')
        bank_name = request.POST.get('bank_name')
        if retailer == None:
            retailer = Retailer.objects.create(user=user, full_name=full_name, open_time=open_time, close_time=close_time,
                                               address=address, account_type=account_type, account_number=account_number, bank_name=bank_name)
        else:
            retailer.full_name = full_name
            retailer.open_time = open_time
            retailer.close_time = close_time
            retailer.address = address
            retailer.account_type = account_type
            retailer.account_number = account_number
            retailer.bank_name = bank_name
        retailer.save()
        messages.success(request, 'Successfully updated profile')
        response = HttpResponse(
            {'success': 'Successfully updated product'})
        return response
    return render(request, 'account/retailer-profile.html', context)


@allowed_users(allowed_roles=['retailer'])
def retailer_download_products(request, uid):
    products = Product.objects.filter(retailer=uid)
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="orders.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Category', 'Title', 'Description',
                    'Quantity', 'Unit Price'])
    for product in products:
        writer.writerow(
            [product.category, product.title, product.description, product.quantity, product.price])
    return response


@allowed_users(allowed_roles=['retailer'])
def retailer_product(request, pid):
    if Product.objects.filter(pk=pid).exists():
        product = Product.objects.get(pk=pid)
    else:
        product = None

    product_form = ProductForm(instance=product)
    if request.method == 'POST':
        product_form = ProductForm(
            request.POST, request.FILES, instance=product)
        logging.warning(request.user)
        # logging.warning(product_form)
        # product_form.retailer = request.user
        if product_form.is_valid():
            product_retailer = product_form.save(commit=False)
            product_retailer.retailer = request.user
            product_retailer.save()
            messages.success(request, "Product updated")
            return redirect('retailer-dashboard')

    context = {'form': product_form}
    return render(request, 'account/retailer-product.html', context)


# Retailer delete product
@allowed_users(allowed_roles=['retailer'])
def retailer_delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.error(request, "Product deleted")
        return redirect('retailer-dashboard')
    context = {'product': product}
    return render(request, 'account/retailer-delete-product.html', context=context)


@allowed_users(allowed_roles=['retailer'])
def retailer_update_delivery(request, oid):
    orderitem = OrderItem.objects.get(pk=oid)
    statuses = Status.objects.all()
    if request.method == 'POST':
        status = Status.objects.get(name=request.POST.get('status'))
        orderitem.status = status
        orderitem.save()
        messages.success(request, "Delivery status updated!")
        response = HttpResponse(
            {'success': 'Successfully updated delivery status'})
        return response
    context = {'orderitem': orderitem, 'statuses': statuses}
    return render(request, 'account/retailer-update-delivery.html', context=context)
