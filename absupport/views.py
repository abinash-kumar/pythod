import datetime
import itertools
import os
import re
import shutil
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection

from abutils.apex_apis import APEXApiIntegration
from abutils.telegram import send_message as telegram
from abutils.telegram import send_exception as telegram_exception
from artist.models import ArtistDesign, ArtistDetail, ProductArtistDesignMap
from auraai.models import ProductTagMap, Tag
from product.apis.views import set_product_cache
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.files import File
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from codeab.celery import app
from notification.models import Notification
from orders.models import Order, Transaction
from product.models import (Category, CategoryVarient, Discount, Product,
                            ProductImage, ProductVarientList, ComboProducts)
from seller.models import Seller, ShippingCharge
from product.offers import Offers
from customer.models import Campaign
from product import constant as product_constant
from abutils import utils
from abutils.reporting.ab_logging import ab_logger

from .models import DeliveryOrders, SellerPickupAddress
from django.db.models import Q


# Create your views here.

def dashboard(request):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return HttpResponseRedirect("/login/")
    else:
        seller_count = Seller.objects.all().count()
        user_count = User.objects.filter(is_staff=False).count()
        context = {
            'seller_count': seller_count,
            'user_count': user_count
        }
        return render(request, "dashboard.html", context)


def clear_cache(request):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return HttpResponseRedirect("/login/")
    cache.clear()
    return JsonResponse({'success': True})


def login_as(request):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    if "__impersonate" in request.POST:
        try:
            staff_user = request.user
            username = request.POST['__impersonate'].strip()
            u = User.objects.get(username=username)

            # If staff trying to access superuser account
            if not u.is_superuser or staff_user.is_superuser:
                auth_user = authenticate(
                    username=username, password="1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnmASDF")
                if auth_user:
                    login(request, auth_user)
                request.session['abstaff_user_id'] = staff_user.id
                return HttpResponseRedirect(reverse('profile'))
            else:
                return HttpResponseRedirect(reverse('absupport:login_as'))
        except (User.DoesNotExist):
            return HttpResponseRedirect(reverse('absupport:login_as'))
    else:
        template = 'login_as.html'
        return render(request, template, {})


def send_email(request):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return HttpResponseRedirect("/login/")
    else:
        not_objs = Notification.objects.all()
        drop_down_value = [{'nid': i.nid, 'id': i.id} for i in not_objs]
        context = {
            'drop_down_values': drop_down_value,
        }
        return render(request, "dashboard_email.html", context)


def initiate_email_sending(request, id):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return HttpResponse("/login/")
    else:
        notify_obj = Notification.objects.get(id=id)
        notify_obj.send_email([])
        return HttpResponse("<h2>Succussfully intiated email sending, check status from admin</h2>")


def initiate_sms_sending(request, id):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return HttpResponse("/login/")
    else:
        notify_obj = Notification.objects.get(id=id)
        notify_obj.send_sms([])
        return HttpResponse("<h2>Succussfully intiated SMS sending, check status from admin</h2>")


def seller_pickup_address_reg(request, id=None):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    seller = Seller.objects.all()
    if request.GET.get('id'):
        id = request.GET.get('id')

    if id and Seller.objects.filter(id=id).exists():
        seller_obj = Seller.objects.get(id=id)
        context = {'id': id,
                   'seller': seller,
                   "pincode": seller_obj.pickup_pin_code,
                   "mobile": seller_obj.mobile,
                   "seller_obj": seller_obj,
                   "address": seller_obj.pickup_address,
                   'first_name': seller_obj.seller.first_name,
                   'last_name': seller_obj.seller.last_name}
        return render(request, "seller_pickup_address_reg.html", context)
    else:
        all_address, random = APEXApiIntegration().get_all_address_status()
        context = {'id': "", 'seller': seller, 'all_address': all_address}
        return render(request, "seller_pickup_address_reg.html", context)


@require_POST
def seller_pickup_address_update(request):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")

    seller_id = request.POST.get('seller_id')
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    mob = request.POST.get('mob')
    address1 = request.POST.get('address1')
    address2 = request.POST.get('address2')
    pincode = request.POST.get('pincode')
    resp, resp_post = APEXApiIntegration().create_address(
        fname, lname, address1, address2, pincode, mob)
    address_id = ""
    status = ""
    try:
        address_id = resp[0]['address_id']
        status = resp[0]['status']
    except KeyError:
        address_id = "error"
        status = "error"
    seller = Seller.objects.get(id=seller_id)
    d = SellerPickupAddress(seller=seller,
                            request_data=resp_post,
                            response_json=resp,
                            psi=address_id,
                            status=status
                            )
    d.save()
    return HttpResponseRedirect('/ab/address/pickup/')


def orders(request):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")

    status = request.GET.get('status', None)
    from_date = request.GET.get('from_date', None)
    to_date = request.GET.get('to_date', None)

    order_filter = Q()
    if status and status != 'ALL':
        order_filter = Q(order_status=status)
    if from_date and to_date:
        order_filter = order_filter and Q(order_placed_time__gte=datetime.datetime.strptime(from_date, '%Y-%m-%d')) and \
            Q(order_placed_time__lte=datetime.datetime.strptime(to_date, '%Y-%m-%d'))
    orders_objs = Order.objects.filter(order_filter).order_by('-id')
    options = ['ALL']
    order_details = []
    for obj in orders_objs:
        order_dict = {}
        order_dict['order_obj'] = obj
        order_details.append(order_dict)
    for order in Order.ORDER_STATUS_CHOICES:
        options.append(order[0])
    context = {'orders_details': order_details, "options": options}
    return render(request, "all_orders.html", context)


def order_transactions(request):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    p_status = request.GET.get('payment_status', 'ALL')
    p_mode = request.GET.get('payment_mode', 'ALL')
    tracsactions = Transaction.objects.all().order_by('-id')
    if not p_mode == 'ALL':
        tracsactions = tracsactions.filter(payment_mode=p_mode)
    if not p_status == 'ALL':
        tracsactions = tracsactions.filter(payment_status=p_status)

    if request.GET.get('from_date', None) and request.GET.get('to_date', None):
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        from_date_object = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        to_date_object = datetime.datetime.strptime(to_date, '%Y-%m-%d')
        tracsactions = tracsactions.filter(
            payment_on__range=(from_date_object, to_date_object))

    payment_mode = [x[0] for x in Transaction.PAYMENT_MODE_CHOICES]
    payment_status = [x[0] for x in Transaction.PAYMENT_STATUS_CHOICES]
    payment_mode.insert(0, 'ALL')
    payment_status.insert(0, 'ALL')
    context = {'transactions': tracsactions,
               'payment_mode': payment_mode,
               'p_mode': p_mode,
               'payment_status': payment_status,
               'p_status': p_status}
    return render(request, "all_orders_trasactions.html", context)


def order_detail(request, id):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    order = Order.objects.get(id=id)
    available_sellers = order.product_varient.sellers.all()
    delivery_partners, random = APEXApiIntegration().is_service_available(order.product_id.seller.pickup_pin_code,
                                                                          order.shipping_zipcode,
                                                                          'online',
                                                                          '0.5',
                                                                          'standard',
                                                                          'nondoc',
                                                                          'air',
                                                                          '1', '1', '1', '1')

    try:
        delivery_partners['errors']
        err = True
    except KeyError:
        err = False
    context = {'order': order, 'available_sellers': available_sellers,
               'delivery_partners': delivery_partners, 'error': err}
    return render(request, "order_detail.html", context)


@require_POST
def order_confirm(request):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")

    if request.POST.get('order') and request.POST.get('status'):
        order = request.POST.get('order')
        status = request.POST.get('status')
        order = Order.objects.get(id=order)
        seller = order.process_by_seller

        if status == 'CANCELLED':
            order.order_status = status
            order.save()
            return render(request, "order_conf_status.html", {'status': status, "success": False, "email": False})

        elif status == 'CONFIRMED':
            if seller == None:
                seller_id = request.POST.get('seller_id', None)
                if seller_id:
                    seller = Seller.objects.get(id=seller_id)
                    order.process_by_seller = seller
                    order.save()
                # confirm Order And send mail to Seller for order
            if seller.is_email_verified:
                email = seller.seller.email
                product_link = Site.objects.get_current().domain + '/product/' + \
                    order.product_id.slug + '/' + str(order.product_id.id)
                product_details = order.order_other_detail
                bill_no = str(order.id)
                design_link = ""
                product_design_maps = ProductArtistDesignMap.objects.filter(
                    product=order.product)
                if product_design_maps:
                    design_link = Site.objects.get_current().domain + \
                        product_design_maps[0].artist_design.design.url
                order_confirm_mail(email, product_link,
                                   product_details, bill_no, design_link)  # todo debug ???
                order.order_status = status
                order.save()
                context = {'status': status, "success": True, "email": True}
            else:
                context = {'status': status, "success": False, "email": False}

        elif status == 'SHIP_REQUEST':
            # set Order Status to ship req and send mail to seller and call api
            # to generate an pickup req
            seller_aipex = SellerPickupAddress.objects.get(seller=seller)
            date = None
            if request.POST.get('date'):
                date = request.POST.get('date')
            else:
                date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
            partner_id = request.POST.get('partner_id', None)
            if partner_id:
                success, ship_label = ship_order_aipex(
                    order, seller_aipex, date, 'Yes', '1', 'air', partner_id, '0.5', '10', '10', '10')
                if success:
                    order.order_status = status
                    order.save()
                    if seller.is_email_verified:
                        email = seller.seller.email
                        product_link = Site.objects.get_current().domain + '/product/' + \
                            order.product_id.slug + '/' + \
                            str(order.product_id.id)
                        product_details = order.order_other_detail
                        bill_no = str(order.id)
                        shipment_booking_mail(
                            email, product_link, product_details, bill_no, ship_label)  # todo debug ???
                context = {'status': status, "success": success,
                           "email": seller.is_email_verified}
            else:
                context = {'status': status, "success": False, "email": False}
        else:
            context = {'status': status, "success": False, "email": False}
    return render(request, "order_conf_status.html", context)


def ship_order_aipex(order_obj, seller, ship_date, insurance, no_of_packages, shipping_method, partner_id, package_weight, package_height, package_length, package_width):
    oa = DeliveryOrders()
    oa.order = order_obj
    oa.seller = seller
    # spiliting address1 and 2 into 3 parts
    address = re.sub(' +', ' ', (order_obj.shipping_address1 +
                                 ' ' + order_obj.shipping_address2))
    add_list = address.split(' ')
    l = len(add_list) / 3
    address_list = [' '.join(add_list[:l]), ' '.join(
        add_list[l:l * 2]), ' '.join(add_list[l * 2:])]

    payment_mode = "online"
    if order_obj.order_status == 'COD':
        payment_mode = "cod"

    if order_obj.email == "":
        email = order_obj.user.email
    else:
        email = order_obj.email

    if order_obj.shipping_lastname == "":
        last_name = order_obj.user.last_name
    else:
        last_name = order_obj.shipping_lastname
    if last_name == "":
        last_name = order_obj.shipping_firstname

    ORDER_DATA = [
        seller.psi,
        order_obj.shipping_zipcode,
        address_list[0],
        address_list[1],
        address_list[2],
        order_obj.shipping_firstname,
        last_name,
        email,
        #'Bond',
        #'shubhroshekhar@gmail.com',
        order_obj.phone,
        ship_date,
        seller.seller.seller.first_name + " " + seller.seller.seller.last_name,
        insurance,
        no_of_packages,
        'identical',
        '7',
        order_obj.price,
        shipping_method,
        'nondoc',
        payment_mode,
        'standard',
        partner_id,
        package_weight,
        package_height,
        package_length,
        package_width,
        '2079ABR']
    aipex_obj = APEXApiIntegration()
    resp_data, req_data = aipex_obj.create_order(ORDER_DATA)  # Not Checked
    oa.response_json = str(resp_data)
    oa.request_json = str(req_data)
    label = None
    if len(resp_data['errors']) == 0:
        oa.success = True
        oa.aipex_number = resp_data['success']['aipexnumber']
        oa.api_id = resp_data['success']['api_id']
        oa.address_id = resp_data['success']['address_id']
        oa.ship_label = label = resp_data['success']['ship_label']
        oa.cod_label = resp_data['success']['cod_label']
        oa.waybill_no = resp_data['success']['waybill_no']
    else:
        oa.success = False
    oa.save()
    return len(resp_data['errors']) == 0, label


def order_confirm_mail(email, product_link, product_details, bill_no, design_link=""):
    notification = Notification.objects.get(nid='order_confirm_details')
    notification.email_to = [email]
    notification.send_email(
        [product_link, product_details, bill_no, design_link])


def shipment_booking_mail(email, product_link, product_details, bill_no, shipping_label):
    notification = Notification.objects.get(nid='shipment_booking_details')
    notification.email_to = [email]
    notification.send_email(
        [product_link, product_details, bill_no, shipping_label])


@never_cache
def update_product_varient(request, id):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    product_obj = Product.objects.get(id=int(id))
    pvl = ProductVarientList.objects.filter(product=product_obj)
    available_cv = []
    for p in pvl:
        available_cv = available_cv + list(p.key.all())
    message = ""
    if pvl:
        message = "Product Varients Already Present in database"
    category_objs = product_obj.category.all()
    required_category_objs = []
    for i in category_objs:
        required_category_objs = required_category_objs + i.get_branch_nodes()
    varients = {}
    for i in set(required_category_objs):
        cv_objs = CategoryVarient.objects.filter(category=i)
        if cv_objs:
            for cv_obj in cv_objs:
                varients[cv_obj.varient_type] = varients.get(
                    cv_obj.varient_type, []) + [{cv_obj.value: cv_obj in available_cv}]

    product_image_obj = ProductImage.objects.filter(
        product=product_obj).order_by('display_priority')
    context = {
        'required_category_objs': set(required_category_objs),
        'varients': varients,
        'product_id': id,
        'message': message,
        'product_photo': [i.get_thumbname_url() for i in product_image_obj]
    }
    return render(request, "add_varient.html", context)


@never_cache
def update_price_quantity_generic(request):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    product = Product.objects.get(id=request.POST['product_id'])
    cat_obj = product.category.all()[0]
    all_cat_objs = cat_obj.get_branch_nodes()
    category_vairents = CategoryVarient.objects.none()
    for category_obj in all_cat_objs:
        category_vairents = category_vairents | CategoryVarient.objects.filter(
            category=category_obj)

    varient_types = category_vairents.order_by().values('varient_type').distinct()
    varients_list = []
    ProductVarientList.objects.filter(product=product).delete()
    for varient_type in varient_types:
        temp = request.POST.getlist(varient_type['varient_type'])
        temp2 = category_vairents.filter(
            varient_type=varient_type['varient_type'], value__in=temp)
        if len(temp2) > 0:
            varients_list.append(temp2)
    all_varients = list(itertools.product(*varients_list))
    for varients in all_varients:
        pvl = ProductVarientList.objects.create(product=product)
        pvl.key = list(varients)
        pvl.save()
    all_varients = ProductVarientList.objects.filter(product=product)
    sellers = Seller.objects.filter(is_active=True)
    sellers_list = []
    for seller in sellers:
        if ShippingCharge.objects.filter(seller=seller):
            sellers_list.append(seller)
    context = {'all_varients': all_varients, 'sellers': sellers_list}
    return render(request, "absupport/update_product_price_quantity.html", context)


@never_cache
def submit_product_varient_generic(request):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    product = Product.objects.get(id=request.POST.get('product_id', None))
    product_varient_list = ProductVarientList.objects.filter(product=product)
    for pvl in product_varient_list:
        price = request.POST.get('price_' + str(pvl.id), None)
        quantity = request.POST.get('quantity_' + str(pvl.id), None)
        pvl.price = int(price)
        pvl.quantity = int(quantity)
        sellers_id = request.POST.get('sellers_' + str(pvl.id), None)
        sellers = Seller.objects.filter(id__in=sellers_id)
        pvl.sellers = sellers
        pvl.save()

    return HttpResponseRedirect("/product/" + product.slug + "/" + str(product.id))


@never_cache
def list_products_without_varients(request):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    product_objs = Product.objects.filter(active=True)
    product_list = []
    for i in product_objs:
        product = {}
        if not ProductVarientList.objects.filter(product=i) and i.category.all():
            product['name'] = i.name
            product['category'] = i.category.all()[0]
            product['link'] = "/ab/product/update-varient/" + str(i.id) + "/"
            product_list.append(product)
    context = {
        "products": product_list,
    }
    return render(request, "add_product_without_varients.html", context)


def artist_stats(request):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    artist_obj = ArtistDetail.objects.all()
    artist_list = []
    for obj in artist_obj:
        artist = {}
        artist['name'] = obj.customer.customer.first_name + \
            " " + obj.customer.customer.last_name
        artist['all_design_count'] = ArtistDesign.objects.filter(
            customer=obj).count()
        artist['pending_design_count'] = ArtistDesign.objects.filter(
            customer=obj, status='PENDING').count()
        artist['approved_design_count'] = ArtistDesign.objects.filter(
            customer=obj, status='APPROVED').count()
        artist['rejected_design_count'] = ArtistDesign.objects.filter(
            customer=obj, status='REJECTED').count()
        artist['link'] = "/ab/product/create/" + str(obj.id) + "/"
        artist_list.append(artist)
    context = {
        'artist_list': artist_list,
    }
    return render(request, "ab_artist_dashboard.html", context)


def artist_design_list(request, id):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    artist_obj = get_object_or_404(ArtistDetail, id=int(id))
    design_obj = ArtistDesign.objects.filter(customer=artist_obj)
    design_list = []
    for i in design_obj:
        product_type_from_designed = [j.product_type for j in ProductArtistDesignMap.objects.filter(artist_design=i)]
        design = {}
        design['img'] = i.get_thumbname_url()
        design['id'] = i.id
        design['status'] = i.status
        design['category'] = {i: i in product_type_from_designed for i in product_constant.ALL_CATEGORIES_LIST}
        design_list.append(design)
    context = {
        'design_list': design_list,
    }
    return render(request, "create_product.html", context)


def make_product_from_design(request, slug, id):
    # import ipdb; ipdb.set_trace()

    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    slug = product_constant.SLUG_FOLDERNAME_MAP[slug]
    image_path = os.path.join(
        settings.BASE_DIR, "uploads/raw_products/" + slug + "/final/" + str(id))
    image_urls = []
    design_obj = ArtistDesign.objects.get(id=id)
    if not os.path.exists(image_path):
        if slug == 'tshirt':
            utils.create_tshirts_from_design.delay(design_obj.design.path, design_obj.id)
        elif slug == 'fullroundmentshirts':
            utils.create_fullroundmentshirts_from_design.delay(design_obj.design.path, design_obj.id)
        elif slug == 'fullroundwomentshirts':
            utils.create_fullroundwomentshirts_from_design.delay(design_obj.design.path, design_obj.id)
        elif slug == 'croptop':
            utils.create_croptop_from_design.delay(design_obj.design.path, design_obj.id)
        elif slug == 'halfroundwomentshirts':
            utils.create_halfroundwomentshirts_from_design.delay(design_obj.design.path, design_obj.id)
        elif slug == 'vest':
            utils.create_vest_from_design.delay(design_obj.design.path, design_obj.id)
        elif slug == 'tanktop':
            utils.create_tanktop_from_design.delay(design_obj.design.path, design_obj.id)
        return HttpResponse("<h2>Please refresh after few seconds, we are creating products for you</h2>")

    if slug in ['tshirt', 'fullroundmentshirts', 'fullroundwomentshirts', 'halfroundwomentshirts', 'halfroundwomentshirts']:
        category_objs = Category.objects.filter(name='tshirt')
    elif slug == 'croptop':
        category_objs = Category.objects.filter(name='croptop')
    elif slug == 'vest':
        category_objs = Category.objects.filter(name='vest')
    elif slug == 'tanktop':
        category_objs = Category.objects.filter(name='vest')
    else:
        category_objs = None
    if category_objs:
        for i in os.listdir(image_path):
            if settings.DEBUG:
                image_urls.append("http://" + request.get_host() + "/uploads/raw_products/" + slug + "/final/" + str(id) + "/" + i)
            else:
                image_urls.append("https://" + request.get_host() + "/uploads/raw_products/" + slug + "/final/" + str(id) + "/" + i)
        required_category_objs = []
        for i in category_objs:
            required_category_objs = required_category_objs + i.get_branch_nodes()
        varients = {}

        for i in set(required_category_objs):
            if i.name in ['tshirt', 'croptop', 'vest']:
                cv_objs = CategoryVarient.objects.filter(category=i, varient_type__in=['SIZE', 'FABRIC'])
                if cv_objs:
                    for cv_obj in cv_objs:
                        varients[cv_obj.varient_type] = varients.get(cv_obj.varient_type, []) + [{cv_obj.value: False}]
        context = {
            'category_obj': category_objs[0],
            'varients': varients,
            'name': design_obj.title,
            'description': design_obj.comment,
            'tags': design_obj.tags,
            'product_id': id,
            'product_photo': image_urls,
            'printable_product': slug,
        }
        return render(request, "add_varient_in_design.html", context)
    else:
        return HttpResponse("<h3>Error: Invalid Category/Slug</h3>")


def submit_art_product(request):
    # import ipdb; ipdb.set_trace()

    # Authentication
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    # collecting Data from reuest
    cat_obj = Category.objects.get(slug=request.POST['category_slug'])
    name = request.POST['name']
    description = request.POST['description']
    price = request.POST['price']
    tag = request.POST['tags']
    design_id = request.POST['design_id']
    printable_product = request.POST['printable_product']
    images = request.POST.getlist('images')
    cover_images = request.POST.getlist('cover-images')

    # creating Product
    product = Product.objects.create(name=name,
                                     description=description,
                                     price=float(int(price)),
                                     wholesale_price=float(int(price)),
                                     active=True,
                                     seller=Seller.objects.get(seller__username='codeab'))
    product.category.add(cat_obj)
    product.save()
    image_path = os.path.join(
        settings.BASE_DIR, "uploads/raw_products/" + printable_product + "/final/" + str(design_id))
    design_obj = ArtistDesign.objects.get(id=design_id)

    # creating and mappng tags
    for i in tag.split(','):
        tag_objs = Tag.objects.filter(category=cat_obj, tag=i.strip())
        if tag_objs:
            tag_obj = tag_objs[0]
        else:
            tag_obj = Tag.objects.create(category=cat_obj, tag=i.strip())
        ProductTagMap.objects.create(product=product, tag=tag_obj)

    # approving design and map design with product
    design_obj.status = "APPROVED"
    design_obj.save()
    product_type_slug = [i for i, j in product_constant.SLUG_FOLDERNAME_MAP.items() if j == printable_product]
    ProductArtistDesignMap.objects.create(product=product, artist_design=design_obj, product_type=product_type_slug[0])

    # creating varients
    all_cat_objs = cat_obj.get_branch_nodes()
    category_vairents = CategoryVarient.objects.none()
    for category_obj in all_cat_objs:
        category_vairents = category_vairents | CategoryVarient.objects.filter(
            category=category_obj)

    varient_types = category_vairents.order_by().values('varient_type').distinct()
    varients_list = []
    ProductVarientList.objects.filter(product=product).delete()
    for varient_type in varient_types:
        temp = request.POST.getlist(varient_type['varient_type'])
        temp2 = category_vairents.filter(
            varient_type=varient_type['varient_type'], value__in=temp)
        if len(temp2) > 0:
            varients_list.append(temp2)
    all_varients = list(itertools.product(*varients_list))

    # Creating Product images and discounts
    Discount.objects.create(product=product, discount=0, discount_type='flat')
    update_images_in_varient_objects(
        images, image_path, cat_obj, all_varients, product, cover_images)
    all_varients = ProductVarientList.objects.filter(product=product)
    sellers = Seller.objects.filter(is_active=True)
    sellers_list = []
    for seller in sellers:
        if ShippingCharge.objects.filter(seller=seller):
            sellers_list.append(seller)
    shutil.rmtree(image_path)  # remove images
    context = {'all_varients': all_varients, 'sellers': sellers_list}
    return render(request, "absupport/update_product_price_quantity.html", context)


def update_images_in_varient_objects(images, image_path, cat_obj, all_varients, product, cover_images):

    for i in os.listdir(image_path):
        fullpath = image_path + "/" + i
        for selected_img in images:
            if i in selected_img:
                if cat_obj.name == 'tshirt':
                    color, neck, fitting, sleeves, gender = re.split("[_.]+", fullpath)[-6:-1]
                    try:
                        category_varients_color = CategoryVarient.objects.get(category=cat_obj, varient_type='COLOR', value__iexact=str(color).replace('-', ' '))
                        category_varients_neck = CategoryVarient.objects.get(
                            category=cat_obj, varient_type='NECK', value__icontains=str(neck))
                        category_varients_fitting = CategoryVarient.objects.get(
                            category=cat_obj, varient_type='FITTING', value__icontains=str(fitting))
                        category_varients_sleeves = CategoryVarient.objects.get(
                            category=cat_obj, varient_type='SLEEVES', value__icontains=str(sleeves))
                        category_varients_gender = CategoryVarient.objects.get(
                            category=cat_obj, varient_type='GENDER', value__iexact=str(gender))
                    except ObjectDoesNotExist:
                        print "Add Category Varient object first, then create product, for - " + str(fullpath)
                        raise Exception(
                            "Add Category Varient object first, then create product, for - " + str(fullpath))
                    else:
                        all_category_varient_list = set([category_varients_color,
                                                         category_varients_neck,
                                                         category_varients_fitting,
                                                         category_varients_sleeves,
                                                         category_varients_gender])

                        display_priority = 0
                        if selected_img in cover_images:
                            display_priority = 100
                        img_obj = ProductImage.objects.create(product=product, product_photo=File(
                            open(fullpath)), display_priority=display_priority)
                        for varients in all_varients:
                            pvl = ProductVarientList.objects.create(
                                product=product)
                            pvl.key = list(varients) + \
                                list(all_category_varient_list)
                            pvl.product_image = img_obj
                            pvl.save()

                elif cat_obj.name == 'vest':
                    color, neck, fitting, gender = re.split("[_.]+", fullpath)[-5:-1]
                    try:
                        category_varients_color = CategoryVarient.objects.get(
                            category=cat_obj, varient_type='COLOR', value__iexact=str(color).replace('-', ' '))

                        category_varients_neck = CategoryVarient.objects.get(
                            category=cat_obj, varient_type='NECK', value__icontains=str(neck))
                        category_varients_fitting = CategoryVarient.objects.get(
                            category=cat_obj, varient_type='FITTING', value__icontains=str(fitting))
                        category_varients_gender = CategoryVarient.objects.get(
                            category=cat_obj, varient_type='GENDER', value__iexact=str(gender))
        
                    except ObjectDoesNotExist:
                        print "Add Category Varient object first, then create product, for - " + str(fullpath)
                        raise Exception(
                            "Add Category Varient object first, then create product, for - " + str(fullpath))
                    else:
                        all_category_varient_list = set([category_varients_color,
                                                         category_varients_neck,
                                                         category_varients_fitting,
                                                         category_varients_gender])
                        display_priority = 0
                        if selected_img in cover_images:
                            display_priority = 100
                        img_obj = ProductImage.objects.create(product=product, product_photo=File(
                            open(fullpath)), display_priority=display_priority)
                        for varients in all_varients:
                            pvl = ProductVarientList.objects.create(
                                product=product)
                            pvl.key = list(varients) + \
                                list(all_category_varient_list)
                            pvl.product_image = img_obj
                            pvl.save()

                elif cat_obj.name == 'croptop':
                    color, neck, fitting, sleeves, gender = re.split(
                        "[_.]+", fullpath)[-6:-1]
                    try:
                        category_varients_color = CategoryVarient.objects.get(
                            category=cat_obj, varient_type='COLOR', value__iexact=str(color).replace('-', ' '))
                        print 'Color-' + color
                        category_varients_neck = CategoryVarient.objects.get(
                            category=cat_obj, varient_type='NECK', value__icontains=str(neck))
                        print 'neck-' + neck
                        category_varients_fitting = CategoryVarient.objects.get(
                            category=cat_obj, varient_type='FITTING', value__icontains=str(fitting))
                        print 'fitting-' + fitting
                        category_varients_sleeves = CategoryVarient.objects.get(
                            category=cat_obj, varient_type='SLEEVES', value__icontains=str(sleeves))
                        print 'sleeves-' + sleeves
                    except ObjectDoesNotExist:
                        print "Add Category Varient object first, then create product, for - " + str(fullpath)
                        raise Exception(
                            "Add Category Varient object first, then create product, for - " + str(fullpath))
                    else:
                        all_category_varient_list = set([category_varients_color,
                                                         category_varients_neck,
                                                         category_varients_fitting,
                                                         category_varients_sleeves])

                        display_priority = 0
                        if selected_img in cover_images:
                            display_priority = 100
                        img_obj = ProductImage.objects.create(product=product, product_photo=File(
                            open(fullpath)), display_priority=display_priority)
                        for varients in all_varients:
                            pvl = ProductVarientList.objects.create(
                                product=product)
                            pvl.key = list(varients) + \
                                list(all_category_varient_list)
                            pvl.product_image = img_obj
                            pvl.save()


def refresh_offers(request=None):
    obj = Offers()
    obj.refresh_offers_on_products()
    return HttpResponse("<h3>Offer has been updated in all products</h3>")


@csrf_exempt
def alert(request):
    ab_logger.debug("================")
    ab_logger.debug(request.__dict__)
    telegram_exception("New Changes in Addiction Bazaar")
    return JsonResponse({'success': True})


def product_image_mapping(request):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    category = Category.objects.get(slug='tshirt')
    category_varient = CategoryVarient.objects.filter(
        category=category, varient_type='COLOR')
    if request.POST.get('submit', None):
        product_images = ProductImage.objects.filter(
            product__category=category, category_varient=None)
        for id in request.POST.keys():
            try:
                p_id = int(id)
                pi = product_images.filter(id=p_id)
                if pi:
                    pi[0].category_varient = category_varient.filter(
                        id__in=request.POST.getlist(id))
                    if str(pi[0].id) in request.POST.getlist('cover_image'):
                        pi[0].display_priority = 15
                    pi[0].save()
            except Exception:
                print 'error in ' + id
    category = Category.objects.get(slug='tshirt')
    category_varient = CategoryVarient.objects.filter(
        category=category, varient_type='COLOR')
    product_images = ProductImage.objects.filter(
        product__category=category, category_varient=None).order_by('-id')[:30]
    context = {"category_varient": category_varient,
               "product_images": product_images}
    return render(request, "absupport/product_image_mapping.html", context)


def refresh_products(request):
    if not (request.user.is_authenticated() or request.user.is_staff):
        return HttpResponseRedirect("/login/")
    cat_slug = request.POST.get('category', 'all')
    refresh_products_async.delay(cat_slug)
    return JsonResponse({'success': True})


@app.task
def refresh_products_async(cat_slug):
    print 'refreshing products'
    if cat_slug == 'all':
        products = Product.objects.filter(
            category__in=Category.objects.all(), active=True).order_by('-id')
    else:
        category = Category.objects.get(slug=cat_slug)
        products = Product.objects.filter(
            category=category, active=True).order_by('-id')

    cache.set('Product_index_total', len(products), timeout=1000)
    index = 0
    for product in products:
        set_product_cache(product)
        cache.set('Product_index_index', index, timeout=1000)
        index += 1
    refresh_offers()
    return True


def refresh_products_page(request):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return HttpResponseRedirect("/login/")
    category = Category.objects.all()
    redis = get_redis_connection(settings.REDIS_CLIENT)
    all_keys = redis.keys()
    all_keys.sort()
    return render(request, 'absupport/refresh_products_page.html', {'category': category, 'all_keys': all_keys})


def refresh_products_status(request):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return JsonResponse({'total': 1, 'indexed': 1})
    if cache.has_key('Product_index_total'):
        total = cache.get('Product_index_total')
    else:
        total = 0

    if cache.has_key('Product_index_index'):
        indexed = cache.get('Product_index_index')
        indexed += 1
    else:
        indexed = 0
    context = {'total': total, 'indexed': indexed}
    return JsonResponse(context)


def delete_cache_key(request):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return JsonResponse({'success': False})
    cacheKeys = request.POST.getlist('cacheKeys[]')
    if cacheKeys:
        redis = get_redis_connection(settings.REDIS_CLIENT)
        for k in cacheKeys:
            redis.delete(k)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def test_template(request):
    return render(request, "cfblog/query_product.html", {})


def is_page_cached(path):
    # return False
    from absupport.models import PageCacheForSEO
    page_obj = PageCacheForSEO.objects.filter(path=path)
    return len(page_obj) > 0


def cached_data(path, request):
    from absupport.models import PageCacheForSEO
    page_obj = PageCacheForSEO.objects.get(path=path)
    if ('Android' in request.META['HTTP_USER_AGENT'] or 'iPhone' in request.META['HTTP_USER_AGENT']):
        content = open(os.path.join(settings.BASE_DIR, 'templates', 'cached', page_obj.file_name_mobile), 'r')
        template = page_obj.file_name_mobile
    else:
        content = open(os.path.join(settings.BASE_DIR, 'templates', 'cached', page_obj.file_name), 'r')
        template = page_obj.file_name
    return render(request, "cached/" + template, {})


def create_combo_page(request):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return HttpResponseRedirect("/login/")
    products = []
    for product in Product.objects.filter(active=True, is_combo_product=False).order_by('-id'):
        data = {}
        data['id'] = product.id
        data['name'] = product.name
        product_images = ProductImage.objects.filter(product=product)
        if product_images:
            data['image'] = product_images[0].get_thumbname_url()
        else:
            data['image'] = ''
        products.append(data)
    context = {'products': products}
    return render(request, "absupport/create_combo_page.html", context)


def create_combo_product(request):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return HttpResponseRedirect("/login/")
    products = request.POST.getlist('selectedProducts', [])
    combo_name = request.POST.get('comboName', None)
    combo_description = request.POST.get('comboDescription', '')
    combo_quantity = request.POST.get('comboQuantity', None)
    if products and combo_name and combo_quantity:
        product_objs = Product.objects.filter(id__in=products)
        if not (len(product_objs) == len(products)):
            return HttpResponse("<h3>Error: Invalid Product ID</h3>")
        try:
            quantity = int(combo_quantity)
        except ValueError:
            return HttpResponse("<h3>Error: Invalid Price Or Quantity</h3>")
        else:
            product_objs = list(product_objs)
            for product in product_objs:
                for pv in ProductVarientList.objects.filter(product=product):
                    pv.quantity = quantity
                    pv.save()
            cp = ComboProducts.objects.create(
                title=combo_name, description=combo_description)
            # Set Combo Type ************
            cp.products = product_objs
            cp.save()
    return HttpResponseRedirect("/ab/create-combo-page/")


def refresh_artist_design(request):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return HttpResponseRedirect("/login/")
    designId = request.POST.get('designId', None)
    artist_design = ArtistDesign.objects.filter(id=designId)
    if artist_design:
        artist_design[0].create_thumbnail()
        utils.create_products(
            artist_design[0].design.path, artist_design[0].id)
    return HttpResponseRedirect("/ab/dashboard/")


def Campaigns_and_Coupons(request):
    campaign_obj = Campaign.objects.filter(campaign_type__in=['ADVERTISER', 'AB'])

    all_campaign = []

    for cam in campaign_obj:
        campaign = {}
        campaign['expired']= cam.is_campaign_expired()
        campaign['expired_in']= cam.campaign_expired_in()
        campaign['obj'] = cam
        campaign['no_of_times_coupon_applied']= Transaction.objects.filter(coupon_applied=cam.coupon.code).count()
        all_campaign.append(campaign)

        context = {
            'all_campaign': all_campaign,
        }
    return render(request, "absupport/Campaigns-and-Coupons.html", context)


def offline_orders(request):

    #  send payment mode
    #  send payment status
    context = {
        'payment_mode': [ 'ONLINE','COD','PAYTM'],
        'payment_status': ['DRAFT','PENDING','DROP','FAILED','TAMPERED','CANCELLED','COMPLETED',]
    }
    return render(request, "absupport/offline-orders.html", context)


def offline_orders_detail(request):
    order_line_item = request.POST.get('order_line_item', None)
    payment_on = request.POST.get('payment_date', None)
    payment_amount = request.POST.get('payment_amount', None)
    payment_mode = request.POST.get('payment_mode', None)
    payment_status = request.POST.get('payment_status', None)
    discount = request.POST.get('discount', None)
    taxes = request.POST.get('taxes', None)
    shipping_charge = request.POST.get('shipping_charge', None)

    #  capture other details also


    #  create a transaction object with the above captured details
    # T = [ order_line_item,payment_on,payment_amount,payment_mode,payment_status,discount,taxes,shipping_charge ]

    transaction_obj = Transaction.objects.create(
        
        payment_on = payment_on,
        payment_amount = payment_amount,
        payment_mode = payment_mode,
        payment_status = payment_status,
        discount = discount,
        taxes = taxes,
        shipping_charge = shipping_charge,
        )
    # transaction_obj = Transaction(order_line_item,payment_on,payment_amount,payment_mode,payment_status,discount,taxes,shipping_charge )
    transaction_obj.save()
    # create context 


    context = {
        'transaction_obj': transaction_obj,
        'order_line_item': range(int(order_line_item)),
        'order_status': ['DRAFT','PENDING','PAYMENT_DONE','COD','CONFIRMED','SHIP_REQUEST','SHIPPED', 'DELIVERED','RETURNED','CANCELLED']
    }

    return render(request, "absupport/offline-orders-details.html", context)


def offline_orders_submit(request):
    order_line_item = request.POST.get('order_line_item', None)
    transaction_id = request.POST.get('transaction_id', None)
    transaction_obj =  Transaction.objects.get(id=int(transaction_id))
    # order_line_item_id = request.POST.get('order_line_item_id', None)
    # order_line_item =  Transaction.objects.get(id=int(order_line_item_id))
    for i in range(int(order_line_item)):
        quantity = request.POST.get('quantity-' , + i )
        product_id = request.POST.get('product_id')
        price = request.POST.get('price')
        comment = request.POST.get('comment')
        order_other_detail = request.POST.get('order_other_detail')
        phone = request.POST.get('phone', None)
        email = request.POST.get('email', None)
        shipping_firstname = request.POST.get('shipping_firstname', None)
        shipping_lastname = request.POST.get('shipping_firstname', None)
        shipping_address1 = request.POST.get('shipping_address1', None)
        shipping_address2 = request.POST.get('shipping_address2', None)
        shipping_city = request.POST.get('shipping_city', None)
        shipping_state = request.POST.get('shipping_state', None)
        shipping_country = request.POST.get('shipping_country', None)
        shipping_zipcode = request.POST.get('shipping_zipcode', None)
        order_status = request.POST.get('order_status', None)

   #  take all other values 
    # for i in order_line_item:
        order_obj = Order.objects.create( 
            quantity = quantity, 
            product_id = product_id, 
            price = price, 
            comment = comment, 
            order_other_detail = order_other_detail, 
            phone = phone, 
            email = email, 
            shipping_firstname = shipping_firstname, 
            shipping_lastname = shipping_lastname, 
            shipping_address1 = shipping_address1 ,
            shipping_address2 = shipping_address2 ,
            shipping_city = shipping_city,
            shipping_state = shipping_state, 
            shipping_country = shipping_country,
            shipping_zipcode = shipping_zipcode, 
            order_status = order_status,
            )
        transaction_obj.order.add(order_obj)
    #  Create order objects - equal to line items 
    context = {
        'order_obj':order_obj,
        'transaction_obj':transaction_obj,
        'order_line_item': range(int(order_line_item))


    }
    return render(request, "absupport/offline-orders-submit.html", context) # make this html template