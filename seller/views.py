import datetime
import json

from abutils.mailers import AbMailUtils
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import login
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.http.response import (HttpResponse, HttpResponseBadRequest,
                                  HttpResponseForbidden,
                                  HttpResponseNotAllowed, JsonResponse)
from django.shortcuts import get_object_or_404, render
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, ListView
from models import Seller, SellerOnboardingHistory
from notification.models import Notification
from product.models import (Category, CategoryVarient,
                            CategoryWiseDescripionGroup,
                            CategoryWiseProductDescriptionKeys, Discount,
                            Product, ProductDescription, ProductImage,
                            ProductVarientList)
from customer.models import Customer
from .response import JSONResponse, response_mimetype
from .serialize import serialize


# Create your views here.


def dashboard(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    else:
        seller = Seller.objects.get(seller=request.user)
        if not seller.is_active and request.GET.get('skipped', '') != "true":
            # return HttpResponseRedirect("/openshop/")
            return HttpResponseRedirect("/thanks/")
        else:
            context = {

            }
            return render(request, "seller_allproduct.html", context)


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/myhome/")
    else:
        context = {
        }
        return render(request, "sellerhome.html", context)


def seller_form(request):
    context = {
    }
    return render(request, "seller_detailed_form.html", context)


def seller_thanku_for_register(request):
    context = {

    }
    return render(request, "seller_thanku_for_register.html", context)


@require_POST
def create_seller(request):
    name = request.session['name'].strip()
    email = request.session['email'].strip()
    mobile = request.session['mobile'].strip()
    password = request.POST.get('password', '')

    if len(mobile) != 0 and len(mobile) != 10:
         return JsonResponse({'success':False,"msg":"invalid mobile"})
    try:
        int(mobile)
    except ValueError:
        return JsonResponse({'success':False,"msg":"invalid mobile"})

    if(len(mobile) != 0):
        if(Customer.objects.filter(mobile=mobile).exists()):
            return JsonResponse({'success':False})
        if(User.objects.filter(username=mobile).exists()):
            return JsonResponse({'success':False})
    
    if len(User.objects.filter(email=email)) > 0:
        return JsonResponse({'success': False})

    first_name = name.rsplit(' ', 1)[0]
    try:
        last_name = name.rsplit(' ', 1)[1]
    except IndexError:
        last_name = ""
    new_user = User.objects.create(
        email=email, username=mobile, first_name=first_name, last_name=last_name)
    new_user.set_password(password)
    new_user.save()
    g = Group.objects.get(name='seller')
    g.user_set.add(new_user)
    g.save()
    seller_obj = Seller.objects.create(seller=new_user, mobile=mobile)
    SellerOnboardingHistory.objects.create(
        seller=seller_obj, status="REGISTERED")
    return JsonResponse({'success': True})


def set_password(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/myhome/")
    else:
        name = request.session['name']
        email = request.session['email']
        mobile = request.session['mobile']
        context = {
        }
        return render(request, "set_password.html", context)


def add_product(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    print request.COOKIES.get("productID")
    if not (request.COOKIES.get("productID") == "" or request.COOKIES.get("productID") == None):
        product_id = request.COOKIES.get("productID")
        product = get_object_or_404(Product, pk=product_id)
        category = product.category.first()
        data = []
        groups = CategoryWiseDescripionGroup.objects.filter(category=category)
        for g in groups:
            d = {}
            d['name'] = str(g.group)
            d['priority'] = str(g.group_priority)
            keys = CategoryWiseProductDescriptionKeys.objects.filter(group=g)
            mykey = {}
            for k in keys:
                mykey[k.product_desc_key] = ''
            d['keys'] = mykey
            data.append(d)
        data = json.dumps(data)
        context = {
            'data': data,
        }
        return render(request, "seller_addproduct.html", context)
    else:
        category = Category.objects.all()
        cat_lists = []
        data = {}
        for i in category:
            cat_lists.append(str(i.unique_name))
        context = {
            'category': cat_lists,
            'data': data,
        }
        return render(request, "seller_addproduct.html", context)


def all_product(request):
    user = User.objects.get(username=request.user)
    seller = Seller.objects.get(seller=user)
    t = Category.objects.get(name='tshirt')
    all_products = Product.objects.filter(seller=seller, category=t)
    product_list = []
    for product in all_products:
        product_dict = {}
        is_varient = ProductVarientList.objects.filter(product=product).count() > 0
        product_dict['name'] = product.name
        product_dict['slug'] = product.slug
        product_dict['id'] = product.id
        product_dict['is_varient'] = is_varient
        product_dict['price'] = product.price
        product_dict['category'] = product.category.first().unique_name if product.category.first() else "--NO CATEGORY--"
        product_dict['added_on'] = product.added_on
        product_dict['quantity'] = 1
        product_dict['active'] = product.active
        product_dict['missing_data'] = is_varient and not is_missing_vareint_for_product(product)
        product_list.append(product_dict)
    all_cat_obj = Category.objects.all()
    all_categories = [i.name for i in all_cat_obj]
    context = {
        'product_list': product_list,
        'all_categories': all_categories
    }
    return render(request, "seller_allproduct.html", context)


def is_missing_vareint_for_product(product):
    cat = product.category.all()[0]
    cv = CategoryVarient.objects.filter(category=cat)
    all_varient_types = cv.order_by().values('varient_type').distinct()
    produt_varients = ProductVarientList.objects.filter(product=product)
    for pv in produt_varients:
        keys = pv.key.all()
        if len(keys) == len(all_varient_types):
            for vt in all_varient_types:
                s = keys.filter(varient_type=vt['varient_type'])
                if len(s) != 1:
                    return False
        else:
            return False
    return True


@require_POST
def add_product_post(request):
    print "cookies --->>> ", request.COOKIES
    name = request.POST['name']
    price = request.POST['price']
    wholesale_price = request.POST['wholesale_price']
    desc = request.POST['desc']
    category = request.POST['category']
    varient = request.POST['varient']
    varient = json.loads(varient)
    varient_name = request.POST['varientname']
    if varient_name == None or varient_name == "":
        return JsonResponse({'success': False})
    varient_name = varient_name.strip().upper()
    discount = request.POST['discount']
    discount_type = request.POST['discountType']
    category = Category.objects.get(unique_name=category)
    user = User.objects.get(username=request.user)
    seller = Seller.objects.get(seller=user)
    p = Product.objects.create(seller=seller, name=name, description=desc,
                               price=price, wholesale_price=wholesale_price)
    p.category.add(category)
    if p.pk:
        request.session['product_id'] = p.pk
        data = []
        groups = CategoryWiseDescripionGroup.objects.filter(category=category)
        for g in groups:
            d = {}
            d['name'] = g.group
            d['priority'] = str(g.group_priority)
            keys = CategoryWiseProductDescriptionKeys.objects.filter(group=g)
            mykey = {}
            for k in keys:
                mykey[k.product_desc_key] = ''
            d['keys'] = mykey
            data.append(d)
        Discount.objects.create(product=p,
                                discount=discount,
                                discount_type=discount_type)

        for v in varient:
            value = v['varientText'].strip().upper()
            quantity = v['quantityValue'].strip()
            category_varient = CategoryVarient.objects.filter(
                category=category, varient_type=varient_name, value=value)
            if len(category_varient) > 0:
                pv = ProductVarientList.objects.create(
                    product=p, quantity=quantity, price=price)
                pv.key.add(category_varient[0])
                pv.save()
            else:
                p.delete()
                return JsonResponse({'success': False})

        return JsonResponse({'success': True, 'productId': p.pk, 'data': data})
    else:
        return JsonResponse({'success': False})


@require_POST
def add_product_details(request):
    data = request.POST['data']
    data = json.loads(data)
    pid = request.session['product_id']
    p = Product.objects.get(pk=pid)
    c = p.category.first()
    for d in data:
        if d['gname'] != "" and str(d['gp']) != "" and len(d['desc']) > 0 and d['desc'][0]['key1'] != "":
            all_groups = CategoryWiseDescripionGroup.objects.filter(
                category=c, group=d['gname'])
            if len(all_groups) == 0:
                group_id = CategoryWiseDescripionGroup.objects.create(category=c,
                                                                      group=d['gname'], group_priority=d['gp']).pk
            else:
                group_id = all_groups[0].pk
            group = get_object_or_404(CategoryWiseDescripionGroup, pk=group_id)

            for availble_key in d['desc']:
                if availble_key['key1'] != "":
                    keys = CategoryWiseProductDescriptionKeys.objects.filter(
                        group=group, product_desc_key=availble_key['key1'])
                    if len(keys) == 0:
                        CategoryWiseProductDescriptionKeys.objects.create(
                            group=group, product_desc_key=availble_key['key1'])
                    key = CategoryWiseProductDescriptionKeys.objects.filter(
                        group=group, product_desc_key=availble_key['key1'])[0]
                if availble_key['value1'].strip().upper() != "NA":
                    ProductDescription.objects.create(
                        product=p, product_desc_key=key, product_desc_value=availble_key['value1'])
    return JsonResponse({'success': True})


@require_POST
def get_child_category(request):
    parent_id = request.POST.get('parent')
    parent = get_object_or_404(Category, pk=parent_id)
    category = Category.objects.filter(parent=parent)

    categories = {}
    for i in category:
        categories[i.pk] = Category.objects.get(pk=i.pk).unique_name
    print categories
    return JsonResponse({'success': True, 'childs': categories})


@require_POST
def check_existing_mobile(request):
    mobile = request.POST.get('mobile') 
    if len(Customer.objects.filter(mobile=mobile)) > 0:
        print "fail"
        return JsonResponse({'success': False})
    obj = Seller.objects.filter(mobile=mobile)
    if len(obj) > 0:
        print "fail"
        return JsonResponse({'success': False})
    else:
        print "pass"
        return JsonResponse({'success': True})


@require_POST
def check_existing_email(request):
    email = request.POST.get('email')
    obj = User.objects.filter(email=email)
    if len(obj) > 0:
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def upload_image(request):
    # product_id = request.POST['productId']
    # form = ImageUploadForm(request.POST['productImage[file]'])
    # product = Product.objects.get(pk=int(product_id))
    # ob = ProductImage.objects.create(product=product)
    # if form.is_valid():
    #     print form.cleaned_data.values()
    #     # ob.product_photo=form.cleaned_data['product_photo']
    #     # ob.save()
    # return JsonResponse({'success': True })
    print "product id is --->>> ", request.session['product_id']
    product_id = request.session['product_id']
    product = Product.objects.get(pk=int(product_id))
    ob = ProductImage.objects.create(product=product)
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            ob.product_photo = form.cleaned_data['image']
            ob.save()
            return JsonResponse({'success': True})


def add_category(request):
    category = Category.objects.all()
    category_unique_ids = []
    for c in category:
        cid = c.unique_id.split('-', 1)[0]
        category_unique_ids.append(cid)
    category_unique_ids = set(category_unique_ids)
    categories = {}
    for i in category_unique_ids:
        categories[i] = Category.objects.get(pk=i).unique_name
    context = {
        'category': categories,
    }
    return render(request, "seller_addcategory.html", context)


@require_POST
def send_otp(request):
    if not request.is_ajax():
        return HttpResponseForbidden()
    otp_timeout = 15 * 60
    mobile = request.POST['mobile']
    to_email = request.POST['email']
    print mobile
    if not mobile:
        return JsonResponse({}, status=400)

    otp = get_random_string(6, allowed_chars='0123456789')
    print "OTP====>", otp
    if to_email != None or to_email != "":
        n = Notification.objects.get(nid='otp_seller_registration')
        n.email_to = [to_email]
        n.numbers = [mobile]
        n.send_notification([otp])
        # AbMailUtils.send_email(to_email,otp)
    request.session['otp'] = otp
    request.session['expires'] = str(
        datetime.datetime.now() + datetime.timedelta(seconds=otp_timeout))
    return JsonResponse({'success': True})


@require_POST
def verify_otp(request):
    now = datetime.datetime.now()
    if not request.is_ajax():
        return HttpResponseForbidden()

    try:
        otp = json.loads(request.POST['data'])['otp']
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
            request.session['name'] = json.loads(request.POST['data'])['name']
            request.session['email'] = json.loads(
                request.POST['data'])['email']
            request.session['mobile'] = json.loads(
                request.POST['data'])['mobile']
            request.session.pop('expires', invalid_time)
            request.session.pop('otp', '')
            return JsonResponse({'success': True})

        return JsonResponse({'success': False})


# ==========================================

class PictureCreateView(CreateView):
    model = ProductImage
    fields = ('product', 'product_photo',)

    def form_valid(self, form):
        # print "cookies --->>> ",self.request.COOKIES
        product_id = self.request.session['product_id']
        # print product_id
        product = Product.objects.get(pk=int(product_id))
        # pi = ProductImage.objects.create(product=product)
        form.fields['product'] = product
        # print form.fields['product'].name
        self.object = form.save()
        # print "================="
        # print self.object.product.name
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
        # return HttpResponse(status=200)

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class BasicPlusVersionCreateView(PictureCreateView):
    template_name_suffix = '_basicplus_form'


def update_category(request):
    product_id = request.POST.get('productId', None)
    category = request.POST.get('category', None)
    product_obj = Product.objects.get(id=int(product_id))
    cat_obj = Category.objects.get(name=category)

    # delete all varient
    if not(category in product_obj.category.all()):
        ProductVarientList.objects.filter(product=product_obj).delete()  # TODO - may effect user cart

    # Change Category
    product_obj.category.clear()
    product_obj.category.add(cat_obj)
    return JsonResponse({"success": True})
