import datetime
import logging
import uuid
import json
import requests

import utils
from abutils.mailers import AbMailUtils
from customer.models import Customer
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import Http404, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order, Transaction
from product.business_calculation import ProductOrderCalculation
from product.models import (Cart, ProductImage, ComboProducts)
from product.models import ProductOffer
from customer.models import ABMoney, Coupon, Campaign
from notification.models import Notification
from abutils.telegram import send_message as telegram
from product.offers import Offers
from customer.apis.views import get_cart
from django.contrib.sitemaps import views as sitemap_views

from abutils import paytm_checksum


logger = logging.getLogger('django')


def home(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        developing = False
    else:
        developing = settings.MAINTAINANCE
    domain = Site.objects.get_current().domain

    context = {
        'domain': domain,
        'user': request.user,
        'request': request,
        'developing': developing
    }
    return render(request, "new_home.html", context)


def home_designer_wear(request):
    context = {

    }
    return render(request, 'designer/home_designer.html', context)


def login_authentication(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is None:
            user_obj = User.objects.filter(email=username)
            user = authenticate(
                username=user_obj[0].username, password=password) if user_obj else None
        if user is None:
            customer = Customer.objects.filter(mobile=username)
            if customer.exists():
                user = authenticate(
                    username=customer[0].customer.username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'success': True})
    return render_to_response('login.html', context_instance=RequestContext(request))


def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    new_user = False
    if request.GET.get('new', False):
        new_user = True
        print "this is a new user hahahaha"
    context = {
        "new_user": new_user
    }
    return render(request, "login.html", context)


def register_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    context = {

    }
    return render(request, "register.html", context)


def registeruser(request):
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    mobile = request.POST.get('mobile', '')
    password = request.POST.get('password', '')

    u = User.objects.create_user(
        username=email, email=email, password=password)
    name_array = name.strip().rsplit(' ', 1)
    first_name, last_name = name_array if len(
        name_array) == 2 else [name_array[0], ' ']
    u.first_name = first_name
    u.last_name = last_name
    u.save()
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
    c = Customer.objects.get(customer=u)
    c.mobile = mobile
    c.save()
    return JsonResponse({'success': True})


@never_cache
def my_cart(request):
    cart = get_cart(request)
    order_list = []
    for obj in cart:
        order = {}
        order['name'] = obj.product.name
        order['product_link'] = '/product/' + \
            obj.product.slug + '/' + str(obj.product.id) + '/'

        if obj.product.is_combo_product:
            combo_product = ComboProducts.objects.filter(
                products=obj.product)[0]
            order['name'] = combo_product.title + '(' + obj.product.name + ')'
            order['image'] = ProductImage.objects.filter(
                product__in=combo_product.products.all())[0].product_photo
        else:
            order['image'] = ProductImage.objects.filter(
                product=obj.product)[0].product_photo

        order['quantity'] = obj.quantity
        order['cart_id'] = obj.id

        product_varients_key = obj.product_varient.key.all()
        product_varient = []
        for cv in product_varients_key:
            if cv.varient_type == 'SIZE' or cv.varient_type == 'COLOR':
                product_varient.append(str(cv))
        order['product_varient'] = product_varient
        # discount_obj = Discount.objects.get(product=obj.product)
        order['unit_price'] = ProductOrderCalculation.calculate_unit_price(
            obj.product
        )
        price = ProductOrderCalculation.calculate_price(
            obj.product,
            obj.quantity
        )
        if obj.varient != "NA":
            order['varient'] = obj.product_varient_id
        order['price_without_shipping_charge'] = price
        order['seller_id'] = obj.product.seller
        order_list.append(order)

    order_list = ProductOrderCalculation.calculate_individual_shipping_charge(
        order_list)

    order_subtotal = 0
    for i in order_list:
        order_subtotal = order_subtotal + i['price']
    txn_id = request.COOKIES.get("txn_id")
    t = Transaction.objects.filter(payment_id=txn_id)
    coupon_code = t[0].coupon_applied if t else None

    offer, offer_discount, coupon_discount, ab_cash, order_subtotal = get_discount(
        request, order_subtotal, coupon_code)
    tax = ProductOrderCalculation.calculate_tax(order_subtotal)
    final_price = int(order_subtotal + tax -
                      (0 if coupon_discount < 0 else coupon_discount))
    payble_price = final_price - ab_cash
    total_shipping_charge = 0
    no_of_items = len(order_list)
    context = {
        'no_of_items': no_of_items,
        'order_list': order_list,
        'order_subtotal': order_subtotal,
        'tax': tax,
        'final_price': final_price,
        'total_shipping_charge': total_shipping_charge,
        'discount': coupon_discount,
        'payble_price': payble_price,
        'ab_cash': ab_cash,
        'offer': offer,
        'offer_discount': offer_discount,
        'coupon_code': coupon_code,
    }
    return render(request, "cart.html", context)


def get_coupon_discount(request, sub_total, coupon_code):
    if not request.user.is_authenticated():
        return 0, 0
    discount = -1
    ab_cash = 0
    coupon_obj = Coupon.objects.filter(code=coupon_code)
    customer_obj = Customer.objects.get(customer=request.user)
    money_obj_last = ABMoney.objects.filter(customer=customer_obj).last()
    closing_promotional_money = money_obj_last.closing_promotional_money if money_obj_last else 0
    ab_cash = money_obj_last.closing_cash_money if money_obj_last else 0
    if coupon_code and coupon_obj[0].redeem_amount_type == 'TRANSACTIONAL':
        discount = coupon_obj[0].calculate_redeem_amount(sub_total)
    else:
        ELIGIBLE_DISCOUNT = int((15 * sub_total) / 100)
        if ELIGIBLE_DISCOUNT < closing_promotional_money:
            discount = ELIGIBLE_DISCOUNT
        else:
            discount = closing_promotional_money
    return discount, ab_cash


def get_offer_discount(request):
    cart_objs = get_cart(request)
    products = {str(i.product_varient.id): i.quantity for i in cart_objs}
    obj = Offers()
    offer, offer_discount = obj.get_discount_for_products(products)
    offer_name = ''
    if offer_discount:
        offer_name = ProductOffer.objects.get(rule=offer).name
    return offer_name, offer_discount


def eligible_for_coupon_discount(request, revised_sub_total, sub_total, coupon_code):
    return revised_sub_total == sub_total


def get_discount(request, sub_total, coupon_code):
    offer, offer_discount = get_offer_discount(request)
    revised_sub_total = sub_total - offer_discount
    discount, ab_cash = 0, 0
    if eligible_for_coupon_discount(request, revised_sub_total, sub_total, coupon_code):
        discount, ab_cash = get_coupon_discount(
            request, revised_sub_total, coupon_code)
    return offer, offer_discount, discount, ab_cash, revised_sub_total


@require_POST
def review_order_api(request):
    mobile = request.POST.get('mobile', '')
    email = request.POST.get('email', '')
    if not email:
        email = request.user.email
    name_array = request.POST.get('name', '').strip().rsplit(' ', 1)
    first_name, last_name = name_array if len(
        name_array) == 2 else [name_array[0], ' ']
    address_array = request.POST.get('address', '').strip().rsplit(' ', 1)
    address1, address2 = address_array if len(address_array) == 2 else [
        address_array[0], ' ']
    if request.user.is_authenticated():
        cart = Cart.objects.filter(user=request.user, listed_type="CART")
    else:
        try:
            token = uuid.UUID(request.COOKIES.get("token"))
            cart = Cart.objects.filter(token=token, listed_type="CART")
        except TypeError:
            cart = []
    order_obj_list = []
    order_list = []
    # TODO take price from varient
    for obj in cart:
        discount = (obj.product.price * obj.quantity) - ProductOrderCalculation.calculate_price(
            obj.product,
            obj.quantity,
        )
        # Take porduct varient list id and update details**********************

        product_varients = obj.product_varient.key.all()
        s = ''
        for pv in product_varients:
            s = s + pv.varient_type + '-' + pv.value + '  '

        order = Order.objects.create(
            user=request.user,
            product_id=obj.product,
            quantity=obj.quantity,
            price=obj.product.price,
            discount=discount,
            product_varient=obj.product_varient,
            order_status='PENDING',
            phone=mobile,
            email=email,
            shipping_firstname=first_name,
            shipping_lastname=last_name,
            shipping_address1=address1,
            shipping_address2=address2,
            shipping_city=request.POST.get('city', ''),
            shipping_state=request.POST.get('state', ''),
            shipping_country=request.POST.get('country', 'India'),
            shipping_zipcode=request.POST.get('pincode', ''),
            order_other_detail=s
        )
        if request.user.is_authenticated():
            order.user = request.user
            order.save()

        order_dict = {}
        order_dict['order_id'] = order.id
        order_dict['name'] = order.product_id.name
        if order.product_id.is_combo_product:
            combo_product = ComboProducts.objects.filter(products=order.product_id)[0]
            order_dict['name'] = combo_product.title + '(' + order.product_id.name + ')'
            order_dict['image'] = ProductImage.objects.filter(product__in=combo_product.products.all())[0].get_thumbname_url()
        else:
            order_dict['image'] = ProductImage.objects.filter(
                product=order.product_id)[0].get_thumbname_url()

        order_dict['quantity'] = order.quantity
        order_dict['unit_price'] = ProductOrderCalculation.calculate_unit_price(
            order.product_id
        )
        price = ProductOrderCalculation.calculate_price(order.product_id, order.quantity)
        order_dict['discount'] = order.discount
        order_dict['coupon_discount'] = order.coupon_discount
        order_dict['price_without_shipping_charge'] = price
        order_dict['seller_id'] = order.product_id.seller.pk
        order_list.append(order_dict)
        order_obj_list.append(order)

    order_list = ProductOrderCalculation.calculate_individual_shipping_charge(order_list)

    # order sub total
    sub_total, shipping_charge = ProductOrderCalculation.calculate_order_subtotal(order_list)

    logger.warning("""
        sub_total - {} \n
        shipping_charge - {} \n
        order_list - {} \n
        """.format(sub_total, shipping_charge, str(order_list)))

    # order taxes
    taxes = ProductOrderCalculation.calculate_tax(sub_total + shipping_charge)

    # cod charges
    cod_charges = ProductOrderCalculation.calculate_cod_charges(order_obj_list)

    # transaction amount
    txn_id = request.COOKIES.get("txn_id")
    t = Transaction.objects.filter(payment_id=txn_id)
    txn_obj = t[0] if t else Transaction.objects.create()

    offer, offer_discount, coupon_discount, ab_cash, sub_total = get_discount(request, sub_total, txn_obj.coupon_applied)

    logger.warning("""
        Transaction Id - {} \n
        offer - {} \n
        offer_discount - {} \n
        coupon_discount - {} \n
        ab_cash - {} \n
        sub_total - {} \n
        """.format(txn_id, offer, offer_discount, coupon_discount, ab_cash, sub_total))
    order_total_amount = (sub_total + shipping_charge - (0 if coupon_discount < 0 else coupon_discount)) - taxes
    transaction_amount = order_total_amount - ab_cash

    txn_obj.payment_id = uuid.uuid4()
    txn_obj.payment_amount = transaction_amount
    txn_obj.discount = coupon_discount
    txn_obj.payment_from_abmoney = ab_cash
    txn_obj.taxes = taxes
    txn_obj.shipping_charge = shipping_charge
    txn_obj.payment_status = 'PENDING'
    txn_obj.payment_mode = 'ONLINE'
    
    for i in order_obj_list:
        txn_obj.order.add(i)
    txn_obj.save()

    address_name = order.shipping_firstname + " " + order.shipping_lastname
    full_address = str(order.shipping_address1) + " " + str(order.shipping_address2) + ", " + \
        str(order.shipping_city) + ", " + str(order.shipping_state) + \
        ", " + str(order.shipping_zipcode)
    context = {
        'order_list': order_list,
        'order_subtotal': sub_total,
        'tax': taxes,
        'discount': coupon_discount,
        'final_price': int(transaction_amount),
        'total_shipping_charge': shipping_charge,
        'txid': str(txn_obj.payment_id),
        'address_name': address_name,
        'full_address': full_address,
        'order_total_amount': order_total_amount,
        'cod_charges': cod_charges,
    }
    return JsonResponse(context)


def process_payment(request, transaction_id):
    txid = uuid.UUID(transaction_id)
    tx_obj = Transaction.objects.get(payment_id=txid)
    order_obj = tx_obj.order.all()[0]

    if tx_obj.payment_mode == 'ONLINE':
        first_name = order_obj.shipping_firstname
        purl = settings.PAYU_INFO['payment_url']
        surl = settings.PAYU_INFO['surl']
        key = settings.PAYU_INFO['merchant_key']
        curl = settings.PAYU_INFO['curl']
        furl = settings.PAYU_INFO['furl']
        cleaned_data = {
            'key': key,
            'txnid': txid,
            'amount': tx_obj.payment_amount,
            'productinfo': order_obj.product_id,
            'firstname': first_name,
            'email': order_obj.email,
            'udf1': '',
            'udf2': '',
            'udf3': '',
            'udf4': '',
            'udf5': '',
            'udf6': '',
            'udf7': '',
            'udf8': '',
            'udf9': '',
            'udf10': ''
        }

        """ the generate_hash funtion is use for genarating hash
         value from cleaned_data"""
        hash_o = utils.generate_hash(cleaned_data)
        context = {
            'firstname': first_name,
            'purl': purl,
            'surl': surl,
            'phone': order_obj.phone,
            'key': key,
            'hash': hash_o,
            'curl': curl,
            'furl': furl,
            'txnid': str(txid),
            'productinfo': order_obj.product_id,
            'amount': tx_obj.payment_amount,
            'email': order_obj.email,
        }
        print context
        transaction_raw = tx_obj.__dict__.copy()
        transaction_raw.update(
            {'order': o.__dict__ for o in tx_obj.order.all()})
        transaction_raw.update(context)
        transaction_raw = {k: str(v) if type(
            v) != str else v for k, v in transaction_raw.items()}
        tx_obj.payment_request = str(transaction_raw)
        tx_obj.save()
        return render(request, "process-payment.html", context)

    else:
        total_item = 0
        if request.user.is_authenticated():
            cart_obj = Cart.objects.filter(
                user=request.user, listed_type="CART")
            products = [obj.product for obj in cart_obj]
            total_item = len(products)
            for i in cart_obj:
                i.active = False
                i.save()
        else:
            try:
                token = uuid.UUID(request.COOKIES.get("token"))
                cart_obj = Cart.objects.filter(token=token, listed_type="CART")
                products = [obj.product for obj in cart_obj]
                total_item = len(products)
                for i in cart_obj:
                    i.active = False
                    i.save()
            except TypeError:
                cart = []

        if total_item > 0:
            AbMailUtils.send_email_of_order(request.user, products)

        context = {

        }
        return render(request, "offline-page-orderpaced.html", context)


def process_cod(request, transaction_id):
    txid = uuid.UUID(transaction_id)
    tx_obj = Transaction.objects.get(payment_id=txid)
    if tx_obj.payment_mode == 'COD':
        return render(request, "order/cod_order_conf.html", {})
    order_obj = tx_obj.order.all()
    for order in order_obj:
        order.order_status = 'COD'
        order.save()
        telegram("New Order Booked\nOrder id = " + str(order.id) +
                 "\nPayment Mode = COD" + "\nTranction id = " + str(tx_obj.id))
    cod_charges = ProductOrderCalculation.calculate_cod_charges(order_obj)
    tx_obj.payment_mode = 'COD'
    tx_obj.payment_amount = tx_obj.payment_amount + cod_charges
    tx_obj.save()
    handle_abmoney_after_transaction(tx_obj)
    notification_on_order(tx_obj)
    # delete cart
    total_item = 0
    if request.user.is_authenticated():
        cart_obj = Cart.objects.filter(
            user=request.user, listed_type="CART")
        products = [obj.product for obj in cart_obj]
        total_item = len(products)
        cart_obj.delete()
    else:
        try:
            token = uuid.UUID(request.COOKIES.get("token"))
            cart_obj = Cart.objects.filter(
                token=token, listed_type="CART")
            products = [obj.product for obj in cart_obj]
            total_item = len(products)
            cart_obj.delete()
        except TypeError:
            cart = []
    if total_item > 0:
        AbMailUtils.send_email_of_order(request.user, products)

    return render(request, "order/cod_order_conf.html", {})


def deduct_money_from_customer(customer, coupon_obj, promotional_money, loyality_money, transactional_discount, order_no):
    if promotional_money:
        ABMoney.objects.create(
            customer=customer,
            amount=promotional_money * (-1),
            amount_type='PROMOTIONAL',
            particular='order ' + order_no,
        )
    if loyality_money:
        ABMoney.objects.create(
            customer=customer,
            amount=loyality_money * (-1),
            amount_type='CASH',
            particular='order ' + order_no,
        )
    # need to fix
    if transactional_discount:
        ABMoney.objects.create(
            customer=customer,
            amount=transactional_discount,
            amount_type='TRANSACTIONAL',
            particular='Added by Using Coupon Code',
            campaign=Campaign.objects.get(coupon=coupon_obj),
        )
        ABMoney.objects.create(
            customer=customer,
            amount=transactional_discount * (-1),
            amount_type='TRANSACTIONAL',
            particular='order ' + order_no,
        )


def add_money_to_advetisor(user, customer_name, money):
    ABMoney.objects.create(
        customer=user,
        amount=money,
        amount_type='CASH',
        particular='Earned from user successfull order of ' + customer_name,
    )


def handle_abmoney_after_transaction(tx_obj):
    user = tx_obj.order.last().user
    txn_amount = float(tx_obj.payment_amount) + \
        float(tx_obj.payment_from_abmoney)
    coupon_code = tx_obj.coupon_applied
    coupon_obj = Coupon.objects.get(code=coupon_code) if coupon_code else None
    order_no = " & ".join(['#' + str(i.id)for i in tx_obj.order.all()])
    promotional_money = tx_obj.discount if coupon_obj and coupon_obj.redeem_amount_type == 'PROMOTIONAL' else 0
    transactional_discount = tx_obj.discount if coupon_obj and coupon_obj.redeem_amount_type == 'TRANSACTIONAL' else 0
    loyality_amount = tx_obj.payment_from_abmoney
    customer_obj = Customer.objects.get(customer=user)
    deduct_money_from_customer(customer_obj, coupon_obj, promotional_money,
                               loyality_amount, transactional_discount, order_no)
    if coupon_code:
        coupon_obj = Coupon.objects.get(code=coupon_code)
        campaign_obj = Campaign.objects.get(coupon=coupon_obj)
        if campaign_obj.campaign_type == 'ADVERTISER':
            money = campaign_obj.amount if campaign_obj.amount_in == 'FLAT' else txn_amount * \
                (campaign_obj.amount / 100)
            add_money_to_advetisor(
                coupon_obj.user, customer_obj.customer.first_name, money)


def update_transaction(transaction_id, payment_token, request, payment_mode, status="COMPLETED"):
    txnid = uuid.UUID(transaction_id)
    tx_obj = Transaction.objects.get(payment_id=txnid)
    tx_obj.payment_token = payment_token
    tx_obj.payment_on = datetime.datetime.now()
    tx_obj.payment_status = status
    tx_obj.payment_mode = payment_mode
    tx_obj.payment_response = str({k: v[0] for k, v in dict(
                                  request.POST.iterlists()).iteritems()})
    tx_obj.save()
    if status == "COMPLETED":
        handle_abmoney_after_transaction(tx_obj)
        notification_on_order(tx_obj)
        # Update order
        for orders in tx_obj.order.all():
            orders.order_status = "PAYMENT_DONE"
            orders.save()
            telegram("New Order Booked\nOrder id = " + str(orders.id) +
                     "\nPayment Mode = " + payment_mode + "\nTranction id = " + str(tx_obj.id))

        # delete cart
        total_item = 0
        if request.user.is_authenticated():
            cart_obj = Cart.objects.filter(
                user=request.user, listed_type="CART")
            products = [obj.product for obj in cart_obj]
            total_item = len(products)
            cart_obj.delete()
        else:
            try:
                token = uuid.UUID(request.COOKIES.get("token"))
                cart_obj = Cart.objects.filter(
                    token=token, listed_type="CART")
                products = [obj.product for obj in cart_obj]
                total_item = len(products)
                cart_obj.delete()
            except TypeError:
                cart = []
        if total_item > 0:
            AbMailUtils.send_email_of_order(request.user, products)


@csrf_exempt
def success(request):
    print "payment requests data----->", request.POST.items()
    if request.method == 'POST':
        if not utils.verify_hash(request.POST):
            logger.warning("Response data for order (txnid: %s) has been "
                           "tampered. Confirm payment with PayU." %
                           request.POST.get('txnid'))
            txnid = request.POST.get('txnid', '')
            update_transaction(txnid, "NA", request, "ONLINE", "TAMPERED")
            return HttpResponseRedirect('order.failure')
        else:
            logger.warning("Payment for order (txnid: %s) succeeded at PayU" %
                           request.POST.get('txnid'))

            # update transaction
            txnid = request.POST.get('txnid', '')
            payment_token = request.POST.get('mihpayid', '')
            update_transaction(txnid, payment_token, request, "ONLINE")
            return render(request, 'success.html')
    else:
        raise Http404


def failure(request):
    if request.method == 'POST':
        txnid = request.POST.get('txnid', '')
        txnid = uuid.UUID(txnid)
        tx_obj = Transaction.objects.get(payment_id=txnid)
        tx_obj.payment_response = {k: v[0] for k, v in dict(
            request.POST.iterlists()).iteritems()}
        tx_obj.payment_status = "FAILED"
        tx_obj.save()
        return render(request, 'failure.html', {'txid': txnid})
    else:
        raise Http404


def cancel(request):
    if request.method == 'POST':
        txnid = request.POST.get('txnid', '')
        txnid = uuid.UUID(txnid)
        tx_obj = Transaction.objects.get(payment_id=txnid)
        tx_obj.payment_response = {k: v[0] for k, v in dict(
            request.POST.iterlists()).iteritems()}
        tx_obj.payment_status = "CANCELLED"
        tx_obj.save()
        return render(request, 'cancel.html', {'txid': txnid})
    else:
        raise Http404


def checkout(request):
    context = {
    }
    return render(request, "checkoutaddress.html", context)


def process_offline(request):
    total_item = 0
    if request.user.is_authenticated():
        cart_obj = Cart.objects.filter(user=request.user, listed_type="CART")
        products = [obj.product for obj in cart_obj]
        total_item = len(products)
        cart_obj.delete()
    else:
        try:
            token = uuid.UUID(request.COOKIES.get("token"))
            cart_obj = Cart.objects.filter(token=token, listed_type="CART")
            products = [obj.product for obj in cart_obj]
            total_item = len(products)
            cart_obj.delete()
        except TypeError:
            cart = []
    if total_item > 0:
        AbMailUtils.send_email_of_order(request.user, products)

    context = {

    }
    return render(request, "offline-page-orderpaced.html", context)


def paytm_payment(request, transaction_id):
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    CALLBACK_URL = settings.PAYTM_CALLBACK_URL
    # Generating unique temporary ids
    order_id = transaction_id.replace('-', '')
    trans_obj = Transaction.objects.get(payment_id=transaction_id)
    trans_obj.payment_token = order_id
    trans_obj.payment_mode = 'PAYTM'
    bill_amount = str(trans_obj.payment_amount)
    if bill_amount:
        data_dict = {
            'REQUEST_TYPE': "DEFAULT",
            'MID': MERCHANT_ID,
            'ORDER_ID': order_id,
            'TXN_AMOUNT': bill_amount,
            'CUST_ID': trans_obj.order.last().phone,
            'INDUSTRY_TYPE_ID': 'Retail109',
            'WEBSITE': 'VhaBazWEB',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': CALLBACK_URL,
            'MOBILE_NO': trans_obj.order.last().phone,
            'EMAIL': trans_obj.order.last().email,
        }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = paytm_checksum.generate_checksum(
            data_dict, MERCHANT_KEY)
        trans_obj.payment_request = str(param_dict)
        trans_obj.save()
        return render(request, "paytm_payment.html", {'paytmdict': param_dict})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")


@login_required
@csrf_exempt
def paytm_response(request):
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        transaction_id = request.POST['ORDERID']
        payment_token = request.POST['TXNID']
        data_dict = {}
        for key in request.POST:
            data_dict[key] = request.POST[key]
        verify = paytm_checksum.verify_checksum(
            data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        is_payment_completed = paytm_status(transaction_id)
        if verify and is_payment_completed:
            update_transaction(transaction_id, payment_token, request, "PAYTM", "COMPLETED")
            return render(request, "success.html", {"paytm": data_dict})
        elif verify:
            update_transaction(transaction_id, payment_token, request, "PAYTM", "TAMPERED")
            return HttpResponseRedirect('order.failure')
        else:
            update_transaction(transaction_id, payment_token, request, "PAYTM", "FAILED")
            return HttpResponseRedirect('order.failure')
    return HttpResponse(status=200)


def paytm_status(transaction_id):
    URL = 'https://secure.paytm.in/oltp/HANDLER_INTERNAL/getTxnStatus'
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    post_data = {}
    post_data['ORDERID'] = str(transaction_id).replace('-', '')
    post_data['MID'] = MERCHANT_ID
    post_data['CHECKSUMHASH'] = paytm_checksum.generate_checksum(post_data, MERCHANT_KEY)
    r = requests.get(URL + "?JsonData=" + str(json.dumps(post_data)).replace(" ", ''))
    try:
        if json.loads(r.text)['STATUS'] == str('TXN_SUCCESS'):
            return True
    except KeyError:
        return False


def notification_on_order(tx_obj):
    order = tx_obj.order.last()
    email = order.email
    if email and len(email) > 4:
        email_to = email
    else:
        email_to = order.user.email
    payment_mode = tx_obj.payment_mode
    payment_amount = tx_obj.payment_amount
    if email_to and len(email_to) > 4:
        if payment_mode == 'COD':
            notification = Notification.objects.get(nid='cod_order')
            notification.email_to = [email_to]
            notification.send_email([payment_amount])
        elif payment_mode == 'ONLINE' or payment_mode == 'PAYTM':
            notification = Notification.objects.get(nid='payment_done')
            notification.email_to = [email_to]
            notification.send_email([payment_amount])


def update_sheet(request):
    name = request.POST.get("name")
    mobile = request.POST.get("mobile")
    email = request.POST.get("email")
    message = request.POST.get("message")
    message = """ Get in touch
        name : """ + name + """
        mobile : """ + mobile + """
        email : """ + email + """
        message : """ + message + """
    """
    telegram(message)


from codeab.site_maps import ProductDetailSitemap

def render_sitemap(request, sitemap_name=0, sitemap_param=0):
    if (sitemap_name == sitemap_param == 0):
        return sitemap_views.sitemap(request, { sitemap_name: ProductDetailSitemap(0, 100) }, None, 'sitemap.xml')
    initial = 0  if int(sitemap_param) == 1 else ((int(sitemap_param) - 1) * 50)
    final = 50  if int(sitemap_param) == 1 else (int(sitemap_param) * 50 )
    return sitemap_views.sitemap(request, { sitemap_name: ProductDetailSitemap(initial, final) }, None, 'sitemap.xml')
