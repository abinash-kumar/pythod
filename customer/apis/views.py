from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from product.models import ProductImage
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from customer.models import Customer, CustomerAddress, CustomerEmailVerify
from orders.models import Order
from django.utils.crypto import get_random_string
from notification.models import Notification
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.db import IntegrityError
import datetime
from datetime import datetime as dt
from django.shortcuts import render
from product.models import Cart, ComboProducts
from orders.models import Transaction
import uuid
from django.views.decorators.cache import never_cache
from customer.models import Coupon, Campaign, ABMoney
from auraai.models import UserFbLikes
from artist.models import ArtistDetail, ArtistCoupon, ProductArtistDesignMap
from django.shortcuts import get_object_or_404


def get_cart(request):
    user = request.user
    token = request.COOKIES.get('token', None)
    try:
        token = uuid.UUID(token)
    except (AttributeError, TypeError, ValueError) as e:
        token = None
    cart_obj = []
    if request.user.is_authenticated() and token:
        cart_obj = Cart.objects.filter(token=token, active=True)
        for obj in cart_obj:
            obj.user = user
            obj.save()
        cart_obj = Cart.objects.filter(user=user, active=True)
    elif request.user.is_authenticated():
        cart_obj = Cart.objects.filter(user=user, active=True)
    elif token:
        cart_obj = Cart.objects.filter(token=token, active=True)
    return cart_obj


@never_cache
@require_POST
def get_user_details(request):
    cart_count = len(get_cart(request))
    if request.user.is_authenticated():
        c = Customer.objects.get(customer=request.user)
        customer_address_list = []
        customer_address_obj = CustomerAddress.objects.filter(customer=c)
        is_artist = ArtistDetail.objects.filter(customer=c).count() == 1
        for i in customer_address_obj:
            customer_address_list.append({
                'address': i.address,
                'city': i.city,
                'state': i.state,
                'pincode': i.pin_code,
                'name': i.name,
                'mobile': i.mobile,
                'email': i.email,
            })
        customer_details = {
            'is_artist': is_artist,
            'dob': c.dob,
            'artist_type': c.artist_type,
            'mobile': c.mobile,
            'gender': c.gender,
            'points': c.points,
            'is_mobile_verified': c.is_mobile_verified,
            'is_email_verified': c.is_email_verified,
            'share_link': c.share_link,
            'customer_address_list': customer_address_list
        }
        orders = Order.objects.filter(user=c.customer)
        orders_list = []
        for i in orders:
            order = {}
            order['Order Placed On'] = i.order_placed_time
            order['product'] = i.product_id.name
            order['Quantity'] = i.quantity
            order['Status'] = i.order_status
            order['Details'] = i.order_other_detail
            if i.product_id.is_combo_product:
                combo_product = ComboProducts.objects.filter(
                    products=i.product_id)[0]
                order['photo'] = ProductImage.objects.filter(product__in=combo_product.products.all())[
                    0].get_thumbname_url()
            else:
                order['photo'] = ProductImage.objects.filter(product=i.product_id)[
                    0].get_thumbname_url()

            orders_list.append(order)

        fb_likes = UserFbLikes.objects.filter(user=request.user).exists()
        if not fb_likes:
            fb_link = '/aura/fb/request/'
            fb_text = 'Connect to Facebook'
        else:
            fb_link = '/aura/magic/search/'
            fb_text = 'Magic Search'
        context = {
            'user_full_name': c.customer.first_name + c.customer.last_name,
            'user_mobile': c.mobile,
            'user_email': c.customer.email,
            'user_photo': c.user_photo.url,
            'orders_list': orders_list,
            'customer_details': customer_details,
            'cart_count': cart_count,
            'fb_link': fb_link,
            'fb_text': fb_text,
        }
        return JsonResponse(context)
    else:
        context = {
            'is_authenticated': False,
            'cart_count': cart_count,
            'fb_link': '/login/',
            'fb_text': 'Log In',
        }
        return JsonResponse(context)


@require_POST
def send_otp(request):
    otp_timeout = 15 * 60
    mobile = request.POST.get('mobile', None)
    print mobile
    if not mobile:
        return JsonResponse({}, status=400)

    otp = get_random_string(6, allowed_chars='0123456789')
    print "OTP====>", otp
    n = Notification.objects.get(nid='otp_seller_registration')
    n.numbers = [mobile]
    if not settings.DEBUG:
        n.send_notification([otp])
    request.session['otp'] = otp
    request.session['expires'] = str(
        datetime.datetime.now() + datetime.timedelta(seconds=otp_timeout))
    return JsonResponse({'success': True})


@require_POST
def verify_otp(request):
    now = datetime.datetime.now()
    try:
        otp = request.POST.get('otp', '')
    except (KeyError, ValueError):
        return JsonResponse({}, status=400)
    else:
        invalid_time = datetime.datetime(0001, 01, 01)
        expiry = request.session.get('expires', '')
        sent_otp = request.session.get('otp', '')
        expiry = datetime.datetime.strptime(expiry, '%Y-%m-%d %H:%M:%S.%f')
        if not expiry or now > expiry or not sent_otp:
            request.session.pop('expires', invalid_time)
            request.session.pop('otp', '')
            return JsonResponse({'success': False, 'sent_otp': sent_otp})

        if sent_otp == otp:
            if request.user.is_authenticated():
                c = Customer.objects.get(customer=request.user)
                c.mobile = request.POST.get('mobile', c.mobile)
                c.is_mobile_verified = True
                c.save()
            else:
                mobile = request.POST.get('mobile', None)
                if mobile:
                    c = Customer.objects.filter(mobile=mobile)[0]
                    user_obj = c.customer
                    user = authenticate(
                        username=user_obj.username, password="1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnmASDF")
                    if user:
                        login(request, user)
                        c.is_mobile_verified = True
                        c.save()
                    else:
                        return JsonResponse({'success': False})
                else:
                    return JsonResponse({'success': False})
            request.session.pop('expires', invalid_time)
            request.session.pop('otp', '')
            return JsonResponse({'success': True})

        return JsonResponse({'success': False})


@require_POST
def add_new_address(request):
    if request.user.is_authenticated():
        c = Customer.objects.get(customer=request.user)
        name = request.POST.get('name', None)
        mobile = request.POST.get('mobile', None)
        address = request.POST.get('address', None)
        pin_code = request.POST.get('pincode', None)
        city = request.POST.get('city', None)
        state = request.POST.get('state', None)
        email = request.POST.get('email', None)
        if name and mobile and address and pin_code and city and state:
            CustomerAddress.objects.create(
                customer=c,
                name=name,
                mobile=mobile,
                address=address,
                pin_code=pin_code,
                city=city,
                state=state,
                email=email,
            )
            customer_address_list = []
            customer_address_obj = CustomerAddress.objects.filter(customer=c)
            for i in customer_address_obj:
                customer_address_list.append({
                    'address': i.address,
                    'city': i.city,
                    'state': i.state,
                    'pincode': i.pin_code,
                    'name': i.name,
                    'mobile': i.mobile,
                    'email': i.email,
                })
            customer_details = {
                'is_artist': c.is_artist,
                'dob': c.dob,
                'artist_type': c.artist_type,
                'mobile': c.mobile,
                'gender': c.gender,
                'points': c.points,
                'is_mobile_verified': c.is_mobile_verified,
                'is_email_verified': c.is_email_verified,
                'share_link': c.share_link,
                'customer_address_list': customer_address_list
            }
            context = {
                'customer_details': customer_details,
                'success': True
            }
            return JsonResponse(context)
        else:
            return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': False})


@require_POST
def sign_up_user(request):
    name = request.POST.get('name')
    email = request.POST.get('email', "")
    mobile = request.POST.get('mobile', "")
    password = request.POST.get('password', "")
    code = request.POST.get('coupon')
    name_array = name.strip().rsplit(' ', 1)
    first_name, last_name = name_array if len(
        name_array) == 2 else [name_array[0], ' ']
    if len(email.strip()) < 5:
        return JsonResponse({'success': False, "msg": "invalid email"})
    if len(password) < 1:
        return JsonResponse({'success': False, "msg": "invalid password"})
    if len(mobile) != 0 and len(mobile) != 10:
        return JsonResponse({'success': False, "msg": "invalid mobile"})
    try:
        int(mobile)
    except ValueError:
        return JsonResponse({'success': False, "msg": "invalid mobile"})

    if(len(mobile) != 0):
        if(Customer.objects.filter(mobile=mobile).exists()):
            return JsonResponse({'success': False, "msg": "mobile number already exists"})
        if(User.objects.filter(username=mobile).exists()):
            return JsonResponse({'success': False, "msg": "mobile number already exists"})

    if(len(email) <= 30):
        un = email
    else:
        un = mobile
    try:
        u = User.objects.create_user(
            username=un, email=email, password=password, first_name=first_name, last_name=last_name)
    except IntegrityError:
        return JsonResponse({'success': False, "msg": "email already exists"})
    user = authenticate(username=un, password=password)
    if user is not None:
        login(request, user)
    c = Customer.objects.get(customer=u)
    c.mobile = mobile
    c.save()
    if code:
        try:
            coupon_obj = Coupon.objects.get(code=code)
            campaign_obj = Campaign.objects.get(coupon=coupon_obj)
            value = 0
            total_amount_used_by_users = [
                value + i.amount for i in ABMoney.objects.filter(campaign=campaign_obj)][0]
            coupon_code_used_by_all_user_count = ABMoney.objects.filter(
                campaign=campaign_obj).count()
            coupon_code_used_by_this_user_count = ABMoney.objects.filter(
                campaign=campaign_obj, customer=c).count()
            if (total_amount_used_by_users < campaign_obj.maximum_amount and
                    coupon_code_used_by_all_user_count < campaign_obj.total_applicability and
                    coupon_code_used_by_this_user_count < campaign_obj.each_user_applicability and
                    not campaign_obj.is_campaign_expired()):
                ABMoney.objects.create(
                    customer=coupon_obj.customer,
                    amount=campaign_obj.amount,
                    amount_type='PROMOTIONAL',
                    expiry=datetime.datetime.today() + datetime.timedelta(days=60),
                    particular='Earned by sharing signup link',
                    campaign=campaign_obj,
                )
        except ObjectDoesNotExist:
            print "missing code or campaign"

    is_artist = ArtistDetail.objects.filter(customer=c).count() == 1
    customer_address_list = []
    customer_address_obj = CustomerAddress.objects.filter(customer=c)
    for i in customer_address_obj:
        customer_address_list.append({
            'address': i.address,
            'city': i.city,
            'state': i.state,
            'pincode': i.pin_code,
            'name': i.name,
            'mobile': i.mobile,
            'email': i.email,
        })
    customer_details = {
        'is_artist': is_artist,
        'dob': c.dob,
        'artist_type': c.artist_type,
        'mobile': c.mobile,
        'gender': c.gender,
        'points': c.points,
        'is_mobile_verified': c.is_mobile_verified,
        'is_email_verified': c.is_email_verified,
        'share_link': c.share_link,
        'customer_address_list': customer_address_list
    }
    orders = Order.objects.filter(user=c.customer)
    orders_list = []
    for i in orders:
        order = {}
        order['Order Placed On'] = i.order_placed_time
        order['product'] = i.product_id.name
        order['Quantity'] = i.quantity
        order['Status'] = i.order_status
        order['Details'] = i.order_other_detail
        order['photo'] = ProductImage.objects.filter(product=i.product_id)[
            0].get_thumbname_url()
        orders_list.append(order)
    context = {
        'user_full_name': c.customer.first_name + c.customer.last_name,
        'user_mobile': c.mobile,
        'user_email': c.customer.email,
        'user_photo': c.user_photo.url,
        'orders_list': orders_list,
        'customer_details': customer_details,
        'success': True
    }
    user_signup_mail(email, name)
    return JsonResponse(context)


def user_signup_mail(email, name):
    notification = Notification.objects.get(nid='user_signup')
    notification.email_to = [email]
    notification.send_email([name, email])


@require_POST
def sign_in_user(request):
    username = request.POST.get('name')
    password = request.POST.get('password')
    user_obj = User.objects.filter(username=username)
    if not user_obj:
        user_obj = User.objects.filter(email=username)
    if not user_obj:
        cust_obj = Customer.objects.filter(mobile=username)
        user_obj = User.objects.filter(
            username=cust_obj[0].customer.username) if cust_obj else None
    if user_obj:
        user = authenticate(username=user_obj[0].username, password=password)
        if user is not None:
            login(request, user)
            c = Customer.objects.get(customer=user_obj[0])
            is_artist = ArtistDetail.objects.filter(customer=c).count() == 1
            customer_address_list = []
            customer_address_obj = CustomerAddress.objects.filter(customer=c)
            for i in customer_address_obj:
                customer_address_list.append({
                    'address': i.address,
                    'city': i.city,
                    'state': i.state,
                    'pincode': i.pin_code,
                    'name': i.name,
                    'mobile': i.mobile,
                    'email': i.email,
                })
            customer_details = {
                'is_artist': is_artist,
                'dob': c.dob,
                'artist_type': c.artist_type,
                'mobile': c.mobile,
                'gender': c.gender,
                'points': c.points,
                'is_mobile_verified': c.is_mobile_verified,
                'is_email_verified': c.is_email_verified,
                'share_link': c.share_link,
                'customer_address_list': customer_address_list
            }
            orders = Order.objects.filter(user=c.customer)
            orders_list = []
            for i in orders:
                order = {}
                order['Order Placed On'] = i.order_placed_time
                order['product'] = i.product_id.name
                order['Quantity'] = i.quantity
                order['Status'] = i.order_status
                order['Details'] = i.order_other_detail
                pis = ProductImage.objects.filter(product=i.product_id)
                if pis:
                    order['photo'] = pis[0].get_thumbname_url()
                else:
                    order['photo'] = ''
                orders_list.append(order)
            context = {
                'user_full_name': c.customer.first_name + c.customer.last_name,
                'user_mobile': c.mobile,
                'user_email': c.customer.email,
                'user_photo': c.user_photo.url,
                'orders_list': orders_list,
                'customer_details': customer_details,
                'success': True
            }
            return JsonResponse(context)
        else:
            error_text = "Username and Password doesn't match"
    else:
        error_text = "Please Sign Up, Entered Email/Mobile is not a registered user with us"
    context = {
        'error_text': error_text,
        'success': False,
    }
    return JsonResponse(context)


@require_POST
def check_mobile(request):
    mobile = request.POST.get('mobile', None)
    if mobile:
        c = Customer.objects.filter(mobile=mobile)
        c = c[0] if c else None
        if c:
            context = {
                'success': True
            }
        else:
            context = {
                'success': False,
                'error_text': "Sorry, Mobile Number doesn't exist on our system, please try Sign Up",
            }
    else:
        context = {
            'success': False,
            'error_text': "Where is mobile Number ???",
        }
    return JsonResponse(context)


@require_POST
def send_email_verification(request):
    if not request.user.is_authenticated():
        return JsonResponse({'success': False})
    else:
        customer = Customer.objects.get(customer=request.user)
        # Create Email Verification Link
        c = CustomerEmailVerify.objects.create(customer=customer)
        link = 'https://' + request.get_host() + '/user/apis/verify/email/' + str(c.link)

        n = Notification.objects.get(nid='user_email_verification')
        n.email_to = [customer.customer.email]
        n.send_email([link])
        return JsonResponse({'success': True})


def verify_email_verification(request, link):
    verify_obj = CustomerEmailVerify.objects.filter(link=link)
    if verify_obj:
        verify_obj[0].is_clicked = True
        customer_obj = verify_obj[0].customer
        customer_obj.is_email_verified = True
        verify_obj[0].save()
        customer_obj.save()
        context = {
            'success': True,
            'message': 'Your Email is verified'
        }
        return render(request, "email_verification.html", context)
    else:
        context = {
            'success': False,
            'message': 'Something Bad Happened...Link is broken'
        }
        return render(request, "email_verification.html", context)


@require_POST
def send_email_for_password_reset(request):
    email = request.POST.get('email', None)
    if email:
        try:
            user = User.objects.filter(email=email)
            if not user.exists():
                return JsonResponse({'success': False, 'msg': 'Email is not registered!!!'})
            user = user[0]
            customer = Customer.objects.get(customer=user)
            customer_email_verify_obj = CustomerEmailVerify.objects.create(
                customer=customer)
            link = 'https://' + request.get_host() + '/user/reset-password/verify/' + \
                str(customer_email_verify_obj.link) + '/'
            notification = Notification.objects.get(nid='user_password_reset')
            notification.email_to = [customer.customer.email]

            notification.send_email([link])
            return JsonResponse({'success': True, 'msg': 'Email has been sent please check your mail-box.'})
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'msg': 'Email is not registered!!!'})
    else:
        return JsonResponse({'success': False, 'msg': 'Email is mandetory'})


@require_POST
def verify_email_existence(request):
    usermail = request.POST.get('usermail', None)
    if User.objects.filter(email=usermail).exists():
        context = {
            'success': True,
            'message': 'Email Exist'
        }
    else:
        context = {
            'success': False,
            'message': 'Email Does Not Exist'
        }
    return JsonResponse(context)


@require_POST
def customer_details(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    customer = Customer.objects.get(customer=user)
    first_name = user.first_name
    last_name = user.last_name
    user_photo = customer.user_photo.url
    mobile = customer.mobile
    email = user.email
    dob = customer.dob
    gender = customer.gender
    context = {'first_name': first_name,
               'last_name': last_name,
               'user_photo': user_photo,
               'mobile': mobile,
               'email': email,
               'dob': dob,
               'share_link': customer.share_link,
               'code': Coupon.objects.get(user=customer).code,
               'gender': gender,
               'is_mobile_verified': customer.is_mobile_verified,
               'is_email_verified': customer.is_email_verified, }
    try:
        artist = ArtistDetail.objects.get(customer=customer)
        context.update({'link': '/artist/profile/' +
                        str(artist.id) + '/' + str(artist.slug) + '/'})
    except ObjectDoesNotExist:
        context.update({'link': ""})
    return JsonResponse(context)


@require_POST
def edit_customer_details(request):
    first_name = request.POST.get('first_name', None)
    last_name = request.POST.get('last_name', None)
    gender = request.POST.get('gender', None)
    dob = request.POST.get('dob', None)
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    customer = Customer.objects.get(customer=user)

    if first_name and first_name.strip() != "":
        user.first_name = first_name
        user.save()

    if last_name and last_name.strip() != "":
        user.last_name = last_name
        user.save()

    if gender and gender.strip() != "":
        customer.gender = gender
        customer.save()
    if dob and dob.strip() != "":
        try:
            valid_datetime = dt.strptime(dob, '%Y-%m-%d')
            customer.dob = valid_datetime
            customer.save()
        except ValueError:
            print "dob Value Error" + dob

    context = {'success': True}
    return JsonResponse(context)


@require_POST
def get_wallet_data(request):
    if request.user.is_authenticated():
        customer_obj = Customer.objects.get(customer=request.user)
        money_obj = ABMoney.objects.filter(
            customer=customer_obj).order_by('-created_on')
        money_obj_last = ABMoney.objects.filter(customer=customer_obj).last()
        closing_promotional_money = money_obj_last.closing_promotional_money if money_obj_last else 0
        closing_cash_money = money_obj_last.closing_cash_money if money_obj_last else 0
        money_list = []
        for m in money_obj:
            money = {}
            money['amount'] = m.amount
            money['amount_type'] = m.amount_type
            money['expiry'] = m.expiry.strftime(
                '%d %b, %Y') if m.expiry else '-'
            money['particular'] = m.particular
            money['closing_money'] = m._closing_cash_money + \
                m._closing_promotional_money
            money['created_on'] = m.created_on.strftime('%d %b, %Y')
            money_list.append(money)
        context = {
            'money_list': money_list,
            'closing_promotional_money': closing_promotional_money,
            'closing_cash_money': closing_cash_money,
            'success': True,
        }
        return JsonResponse(context)
    else:
        return JsonResponse({'success': False})


def check_for_artist_coupon(request, code, redeem_type):
    obj = ArtistCoupon.objects.filter(code=code).first()
    if obj:
        cart_objs = get_cart(request)
        product_objs = [i.product for i in cart_objs]
        artist_design_products = [i.product for i in ProductArtistDesignMap.objects.filter(artist_design__customer=obj.artist)]
        applicable_products = set(artist_design_products).intersection(set(product_objs))
        return False if applicable_products else 'This coupon code is not applicable with products on your cart'
    else:
        return False


@require_POST
def redeem_coupon(request):
    from myhome.views import get_offer_discount
    offer, offer_discount = get_offer_discount(request)
    if offer_discount:
        return JsonResponse({'error': True, 'errorText': "Sorry, coupon code not eligible with existing offer"})
    code = request.POST.get('code').upper() if request.POST.get('code', None) else None
    redeem_type = request.POST.get('type').upper() if request.POST.get('type', None) else None

    error_text = ''

    if not request.user.is_authenticated():
        error_text = "Please <a href='/login/?next=/my-cart/'>login</a> to apply coupon"
    elif Coupon.objects.get(user=Customer.objects.get(customer=request.user)).code.upper() == code.upper():
        error_text = 'You can not apply your own coupon code'
    
    if error_text:
        return JsonResponse({'error': True, 'errorText': error_text})

    error_text = check_for_artist_coupon(request, code, redeem_type)

    if code and not error_text:
        customer_obj = Customer.objects.get(customer=request.user)
        coupon_obj = Coupon.objects.filter(code=code, active=True)
        if coupon_obj and coupon_obj[0].redeem_amount_type == "PROMOTIONAL":
            campaign_obj = Campaign.objects.get(
                coupon=coupon_obj[0], active=True)
            if not campaign_obj.is_campaign_expired():
                coupon_code_used_by_all_user_count = ABMoney.objects.filter(
                    campaign=campaign_obj).count()
                coupon_code_used_by_this_user_count = ABMoney.objects.filter(
                    campaign=campaign_obj, customer=customer_obj).count()
                if (campaign_obj.get_total_amount_used_by_users() < campaign_obj.maximum_amount and
                        coupon_code_used_by_all_user_count < campaign_obj.total_applicability and
                        coupon_code_used_by_this_user_count < campaign_obj.each_user_applicability):
                    expiry = datetime.datetime.today(
                    ) + datetime.timedelta(days=campaign_obj.promotional_money_expiry)
                    m = ABMoney.objects.create(
                        customer=customer_obj,
                        amount=coupon_obj[0].redeem_amount,
                        amount_type='PROMOTIONAL',
                        expiry=expiry,
                        particular='Added by Using Coupon Code',
                        campaign=campaign_obj,
                    )
                    ABMoney.objects.create(
                        customer=coupon_obj[0].user,
                        amount=campaign_obj.amount,
                        amount_type='PROMOTIONAL',
                        expiry=datetime.datetime.today() + datetime.timedelta(days=60),
                        particular='Earned by sharing SignUp Code',
                        campaign=campaign_obj,
                    )
                    money = {}
                    money['amount'] = m.amount
                    money['amount_type'] = m.amount_type
                    money['expiry'] = m.expiry.strftime('%d %b, %Y')
                    money['particular'] = m.particular
                    money['closing_money'] = m._closing_cash_money + \
                        m._closing_promotional_money
                    money['created_on'] = m.created_on.strftime('%d %b, %Y')
                    context = {
                        'error': False,
                        'money_list': [money],
                    }
                    return JsonResponse(context)
                else:
                    error_text = 'Sorry, this coupon code is expired'
            else:
                error_text = "this coupon code is expired, please try another one"

        elif coupon_obj and coupon_obj[0].redeem_amount_type == redeem_type == 'TRANSACTIONAL':
            t = Transaction.objects.create(coupon_applied=coupon_obj[0].code)
            campaign_obj = Campaign.objects.get(
                coupon=coupon_obj[0], active=True)
            if not campaign_obj.is_campaign_expired():
                coupon_code_used_by_all_user_count = ABMoney.objects.filter(
                    campaign=campaign_obj).count()
                coupon_code_used_by_this_user_count = ABMoney.objects.filter(
                    campaign=campaign_obj, customer=customer_obj).count()
                if (campaign_obj.get_total_amount_used_by_users() < campaign_obj.maximum_amount and
                        coupon_code_used_by_all_user_count < campaign_obj.total_applicability and
                        coupon_code_used_by_this_user_count < campaign_obj.each_user_applicability):
                    context = {
                        'txn_id': str(t.payment_id),
                    }
                    return JsonResponse(context)
                else:
                    error_text = 'this coupon code is expired.'
            else:
                error_text = "this coupon code is expired"

        elif coupon_obj and coupon_obj[0].redeem_amount_type == 'TRANSACTIONAL' and redeem_type == 'PROMOTIONAL':
            error_text = "Sorry, not applicable here, use this code at the time of purchase."
        else:
            error_text = "Invalid Code, Please enter another code."
    else:
        error_text = error_text if error_text else 'Invalid Code, Please try with another code' 
    return JsonResponse({'error': True, 'errorText': error_text})
