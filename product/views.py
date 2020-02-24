import itertools
import json
import logging
import re

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from product.models import (Cart, Category, CategoryVarient, ComboProducts,
                            Discount, Product, ProductImage, ProductVarientList)

from product import constant as product_constant

logging.basicConfig(filename='logic.log', level=logging.DEBUG)


def product_details(request, slug, id):
    if cache.has_key("product_detail_page_" + id):
        context = cache.get("product_detail_page_" + id)
        return render(request, "product_details.html", context)
    p = get_object_or_404(Product, pk=id)
    is_discontinued = False
    if not p.active:
        is_discontinued = True
    product_images = ProductImage.objects.filter(
        product=p).order_by('display_priority')
    product_images_url = [obj.product_photo.url for obj in product_images]
    product_main_description = p.description
    discount_obj = Discount.objects.get(product=p)
    discount_value = discount_obj.discount
    discount_type = discount_obj.discount_type
    keywords = '*s, * Buy in India, * Store, * Shopping, * Prices, *s in India'
    varients = CategoryVarient.objects.none()
    for pv in ProductVarientList.objects.filter(product=p):
        varients = varients | pv.key.all()
    varient_list = ','.join(
        [v.value.lower() for v in varients.distinct().order_by('varient_type')])
    context = {
        "product_id": id,
        "product_name": p.name,
        "product_price": int(p.price),
        "product_images_url": product_images_url,
        "discount_value": discount_value,
        "discount_type": discount_type,
        "product_main_description": product_main_description,
        "is_discontinued": is_discontinued,
        "title": get_product_detail_page_title(p),
        "meta_description": p.meta_description,
        "keywords": keywords.replace("*", p.category.all()[0].slug)
    }
    cache.set("product_detail_page_" + id, context, timeout=None)
    return render(request, "product_details.html", context)


def get_product_detail_page_title(product, varients=None):
    varients_title = ''
    if not varients:
        varients = CategoryVarient.objects.none()
    for pv in ProductVarientList.objects.filter(product=product):
        varients = varients | pv.key.all()
    if varients:
        color = varients.filter(varient_type='COLOR').distinct()
        fitting = varients.filter(varient_type='FITTING').distinct()
        neck = varients.filter(varient_type='NECK').distinct()
        sleeves = varients.filter(varient_type='SLEEVES').distinct()
        if color:
            if len(color) == 1:
                varients_title += color[0].value + ' '
            else:
                varients_title += 'Multiple Color '
        if fitting:
            if len(fitting) == 1:
                varients_title += fitting[0].value + ' '
            else:
                temp_list = [x.value for x in varients]
                last = temp_list.pop()
                varients_title += ', '.join(temp_list) + ' and ' + last + ' '
        if len(neck) == 1:
            varients_title += neck[0].value + ' '
        if len(sleeves) == 1:
            varients_title += sleeves[0].value + ' '

    return 'Buy ' + product.name.title() + ' - ' + varients_title + product.category.all()[0].name.title() + '@ AddictionBazaar.com'


def product_listing(request, slug, id):
    return HttpResponseRedirect('/')
    this_category = Category.objects.get(pk=id)
    category_description = this_category.description
    category_image = this_category.category_photo
    breadcum_details = this_category.unique_id

    breadcum_details = breadcum_details.split('-')
    breadcum_list = []
    for i in breadcum_details:
        breadcum = {}
        category = Category.objects.get(pk=i)
        breadcum['slug'] = category.slug
        breadcum['id'] = category.pk
        breadcum['name'] = category.name
        breadcum_list.append(breadcum)

    sub_categories_obj = Category.objects.filter(parent=id, active=True)
    sub_categories_list = []
    for obj in sub_categories_obj:
        sub_category = {}
        sub_category['id'] = obj.pk
        sub_category['slug'] = obj.slug
        sub_category['name'] = obj.name
        sub_categories_list.append(sub_category)
    all_cat_obj = Category.get_all_children(this_category)
    all_products = [Product.objects.filter(
        category=obj, active=True) for obj in all_cat_obj]
    products_obj = set(itertools.chain.from_iterable(all_products))

    product_detail_list = []
    for obj in products_obj:
        product_detail = {}
        product_detail['name'] = obj.name

        product_image_obj = ProductImage.objects.filter(
            product=obj).order_by('display_priority')[:1]
        product_detail['product_photo_url'] = [i.get_thumbname_url()
                                               for i in product_image_obj]

        product_detail['slug'] = obj.slug
        product_detail['price'] = int(obj.price)
        product_detail['id'] = obj.id

        logging.info("====================")
        logging.info(obj.name)
        discount_obj = get_object_or_404(Discount, product=obj)

        # calculate discounted price
        if discount_obj is not None:
            if discount_obj.discount_type.lower() == "flat":
                price_after_discount = obj.price - discount_obj.discount
            elif discount_obj.discount_type.lower() == "percentage":
                price_after_discount = obj.price - \
                    obj.price * (discount_obj.discount / 100)
            else:
                price_after_discount = obj.price
        product_detail['price_after_discount'] = int(price_after_discount)
        product_detail['discount'] = [
            discount_obj.discount, discount_obj.discount_type]
        product_detail_list.append(product_detail)

    paginator = Paginator(product_detail_list, 12)
    page = request.GET.get('page')
    try:
        product_detail_pager_list = paginator.page(page)
    except PageNotAnInteger:
        product_detail_pager_list = paginator.page(1)
    except EmptyPage:
        product_detail_pager_list = paginator.page(paginator.num_pages)

    context = {
        "category": this_category,
        "sub_categories_list": sub_categories_list,
        "category_description": category_description,
        "category_image": category_image,
        "product_detail_list": product_detail_pager_list,
        "breadcum_list": breadcum_list,
        'page': page
    }
    return render(request, "products_001.html", context)


def cust(request):
    context = {

    }
    return render(request, "cust.html", context)


@require_POST
def delete_cart(request):
    print "\nuser name => ", request.POST.get("cart_id")
    cart_id = request.POST.get("cart_id")
    this_cart = Cart.objects.get(pk=cart_id)
    if this_cart.product.is_combo_product:
        if request.user.is_authenticated():
            carts = Cart.objects.filter(user=this_cart.user)
        else:
            carts = Cart.objects.filter(token=this_cart.token)

        combo_products = ComboProducts.objects.filter(
            products=this_cart.product)[0]
        for cart in carts:
            if cart.product in combo_products.products.all():
                cart.delete()
    else:
        this_cart.delete()
    return JsonResponse({'success': True})


@require_POST
def update_cart_count(request):
    print "\nuser name => ", request.POST.get("cart_id")
    cart_id = request.POST.get("cart_id")
    qty = request.POST.get("qty")
    if (qty and int(qty) > 0):
        this_cart = Cart.objects.get(pk=cart_id)
        if this_cart.product.is_combo_product:
            if request.user.is_authenticated():
                carts = Cart.objects.filter(user=this_cart.user)
            else:
                carts = Cart.objects.filter(token=this_cart.token)
            combo_products = ComboProducts.objects.filter(
                products=this_cart.product)[0]
            for cart in carts:
                if cart.product in combo_products.products.all():
                    cart.quantity = qty
                    cart.save()
        else:
            this_cart.quantity = qty
            this_cart.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def sub_category_listing(request, slug):
    return render(request, 'product_tshirt_sub_cat.html', {})


def products(request, slug):
    category, varients = get_category_and_varients_from_slug(slug)
    content = get_page_content(slug)
    content_title = "dssds"
    context = {'category': json.dumps([category]),
               'varients': json.dumps(varients),
               'content': content,
               'content_title': content_title,
               }
    return render(request, 'product_tshirt.html', context)


def get_page_content(slug):
    return ""


def mens_products(request):
    mens_category = product_constant.MENS_CATEGORY
    varients = {'GENDER': ['MALE']}
    content = get_page_content('mens-clothing')
    content_title = "Men's Clothing"
    context = {
        # 'category': ['tshirt', 'hoodie', 'vest'],
        'category': ['tshirt'],
        'varients': json.dumps(varients),
        'mainCategory': json.dumps(mens_category),
        'content': content,
        'content_title': content_title,
    }
    return render(request, 'product_tshirt.html', context)


def women_products(request):
    womens_category = product_constant.WOMENS_CATEGORY
    varients = {'GENDER': ['FEMALE']}
    content = get_page_content('womens-clothing')
    content_title = "Women's Clothing"
    context = {
        'category': ['tshirt', 'hoodie', 'croptop'],
        'varients': json.dumps(varients),
        'mainCategory': json.dumps(womens_category),
        'content': content,
        'content_title': content_title,
    }
    return render(request, 'product_tshirt.html', context)


def couple_products(request):
    couple_category = product_constant.COUPLE_CATEGORY
    varients = {'combo_type': ['COUPLE']}
    content = get_page_content('couple-clothing')
    content_title = "Couple Clothing"
    context = {
        'category': ['tshirt', 'hoodie', 'croptop'],
        'varients': json.dumps(varients),
        'mainCategory': json.dumps(couple_category),
        'content': content,
        'content_title': content_title,
    }
    return render(request, 'product_tshirt.html', context)


def tshirt(request):
    couple_category = product_constant.COUPLE_CATEGORY
    content = get_page_content('tshirt')
    content_title = "Tshirts"
    context = {
        'category': ['tshirt'],
        'varients': json.dumps({}),
        'mainCategory': json.dumps({}),
        'content': content,
        'content_title': content_title,
    }
    return render(request, 'product_tshirt.html', context)


def buy_varient_wise(request, category, varient):
    title = "Buy " + varient.replace('--', ',') + \
        " " + category + '  at addictionbazaar.com'
    return render(request, 'buy_varient_wise_listing.html', {'title': title.title()})


def get_category_and_varients_from_slug(slug):
    # import ipdb; ipdb.set_trace()
    category = None
    try:
        slug, category = slug.rsplit('-', 1)
    except ValueError:
        try:
            category = category or slug
            category_obj = Category.objects.get(name=category)
        except ObjectDoesNotExist:
            return False, False
        else:
            return category_obj.name, {}
    else:
        varients = filter(None, [i.upper().strip() for i in re.split(
            "color|sleeves|size|neck|fit|-", slug.replace('--', ' '))])
        varient_dict = {}
        for varient in varients:
            try:
                category_varient_obj = CategoryVarient.objects.get(
                    category__name=category, name=varient)
            except ObjectDoesNotExist:
                print 'Invalid Varient - ' + varient
            else:
                if category_varient_obj.varient_type in varient_dict.keys():
                    varient_dict[str(category_varient_obj.varient_type)].append(
                        str(category_varient_obj.value))
                else:
                    varient_dict[str(category_varient_obj.varient_type)] = [
                        str(category_varient_obj.value)]
        return category, varient_dict


def slug_validator(slug):
    slug_list = slug.upper().split('-')
    for slug_key in slug_list:
        if not check_slug_key(slug_key.lower()):
            return False
    else:
        return True


def check_slug_key(slug_key):
    key = 'SLUG_KEYS'
    all_keys = []
    if cache.has_key(key):
        all_keys = cache.get(key)
    else:
        for cv in CategoryVarient.objects.all():
            all_keys += cv.varient_type.lower().split(' ') + cv.value.lower().split(' ')
        for cat in Category.objects.all():
            all_keys.append(cat.slug)
        cache.set(key, list(set(all_keys)), timeout=None)
    if slug_key in all_keys:
        return True
    else:
        return False
