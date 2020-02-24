import json
import logging
import operator
import uuid
from orderedset import OrderedSet

import ast
from django.db.models import Q
from django.conf import settings
from django.core import serializers
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django_redis import get_redis_connection
from product.models import (Cart, Category, CategoryVarient, ComboProducts,
                            Discount, Product, ProductImage,
                            ProductVarientList)
from product.offers import Offers
from artist.models import ProductArtistDesignMap
from auraai.models import ProductTagMap
from product import constant as product_constant
from product import views as product_view

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@require_POST
def product_details_api(request):
    pid = int(request.POST.get('id'))
    product_details = get_product_from_cache(pid)
    if(product_details['combo_product']):
        return JsonResponse(combo_product_details_api(pid))
    context = {
        "combo_product": False,
        "product_id": pid,
        "product_name": product_details['name'],
        "product_price": int(product_details['price']),
        "product_images_url": product_details['images_url'],
        "all_varients": product_details['all_varients'],
        "discount_value": product_details['discount_value'],
        "discount_type": product_details['discount_type'],
        "product_main_description": product_details['description'],
        "is_discontinued": product_details['is_discontinued'],
        "size_chart_url": product_details['size_chart_url'],
        "artist_name": product_details['artist_name'],
        "artist_link": product_details['artist_link'],
        "offers": Offers.get_offer_on_product(str(pid)),
        "tags": product_details['tags'],
        "breadcrumb": [{'link': '/', 'value': 'Home'},
                       {'link': '/tshirt/', 'value': 'T-Shirts'},
                       {'link': '', 'value': product_details['name'].title()}]
    }
    return JsonResponse(context)


def combo_product_details_api(p):
    combo_products = ComboProducts.objects.filter(products=p)[0]
    all_products = combo_products.products.all()
    price = 0
    discount_value = 0
    is_discontinued = False
    discount_type = ""
    all_varients_values = []
    tags = []
    product_images_url = []
    for product in all_products:
        product_details = get_product_from_cache(product.id)
        product_images_url += product_details['images_url']
        price = price + int(product_details['price'])
        discount_value = discount_value + product_details['discount_value']
        discount_type = product_details['discount_type']
        is_discontinued = is_discontinued or product_details['is_discontinued']
        all_varients_values = all_varients_values + [{'title': product_details['name'], 'varient_values': product_details[
            'all_varients'][0]['varient_values'], 'product_id':product_details['id']}]
        tags += product_details['tags']
    size_chart_url = product_details['size_chart_url']
    artist = product_details['artist_name']
    artist_link = product_details['artist_link']

    context = {
        "combo_product": True,
        "product_id": p,
        "product_name": combo_products.title,
        "product_images_url": product_images_url,
        "product_main_description": combo_products.description,
        "product_price": int(price),
        "discount_value": discount_value,
        "discount_type": discount_type,
        "is_discontinued": is_discontinued,
        "all_varients": all_varients_values,
        "size_chart_url": size_chart_url,
        "artist_name": artist,
        "artist_link": artist_link,
        "tags": list(set(tags)),
        "offers": Offers.get_offer_on_product(p),
        "breadcrumb": [{'link': '/', 'value': 'Home'},
                       {'link': '/tshirt/', 'value': 'T-Shirts'},
                       {'link': '', 'value': combo_products.title.title()}]
    }
    return context


@require_POST
def similer_product(request):
    try:
        pid = int(request.POST.get('id'))
    except ValueError:
        return JsonResponse({"error": "Invalid product id"})
    count = 0
    try:
        count = int(request.POST.get('count'))
    except ValueError:
        count = 5
    except TypeError:
        count = 5

    pr = Product.objects.get(pk=pid)
    product_categories = pr.category.all()
    print product_categories
    print "----------------------------------------"
    mylist = []
    for obj in product_categories:
        product = Product.objects.filter(category=obj, active=True)
        print obj
        print product
        for p in product:
            product_image_obj = ProductImage.objects.filter(
                product=p).order_by('display_priority')[:1]
            images = [i.get_thumbname_url() for i in product_image_obj]
            mylist.append({"product_id": p.id, "name": p.name,
                           "price": p.price, "product_image": images})

    mylist = [i for n, i in enumerate(mylist) if i not in mylist[n + 1:]]
    context = {"product_list": mylist[:count]}
    return JsonResponse(context)


@require_POST
def product_listing_api(request):
    post_category = request.POST.get('category', '')
    page = request.POST.get('page', None)
    varients = request.POST.get('varients', None)
    min_price = request.POST.get('min_price', None)
    max_price = request.POST.get('max_price', None)
    slug = request.POST.get('slug', None)
    # if cache.has_key('listing-' + '_'.join(post_category) + str(varients) + str(page) + (slug if slug else '')):
    #     all_list = cache.get('listing-' + '_'.join(post_category) +
    #                          str(varients) + str(page) + (slug if slug else ''))
    #     all_list.update({'from_cache': True})
    #     return JsonResponse(all_list)
    if page:
        try:
            page = int(request.POST.get('page'))
        except ValueError:
            page = 0
    else:
        page = 0
    no_of_products = 51
    if not slug:
        varient_dict = json.loads(varients) if varients else {}
        try:
            category_objs = Category.objects.filter(slug__in=ast.literal_eval(post_category))
        except ValueError:
            category_objs = Category.objects.filter(slug=post_category)
    else:
        category, varient_dict = product_view.get_category_and_varients_from_slug(
            slug)
        category_objs = Category.objects.filter(slug=category)
        post_category = [i.name for i in category_objs]
    product_detail_list = cached_list_product(post_category=category_objs,
                                              varient_dict=varient_dict,
                                              min_price=min_price,
                                              max_price=max_price)
    product_detail_list.sort(key=lambda x: x['id'], reverse=True)
    total_number_of_products = len(product_detail_list)
    product_detail_list = product_detail_list[
        page * no_of_products:((page + 1) * no_of_products)]

    page_title = get_page_title([cat.name.title()
                                 for cat in category_objs], varient_dict)
    heading = get_page_heading([cat.name.title()
                                for cat in category_objs], varient_dict)
    bread_crumb = get_breadcum([cat.name.title()
                                for cat in category_objs], dict(varient_dict))
    context = {"product_detail_list": product_detail_list,
               "no_of_products": len(product_detail_list),
               "total_number_of_products": total_number_of_products,
               "page": page,
               "page_title": page_title,
               "breadcrumb": bread_crumb,
               'heading': heading,
               'varients': get_product_varients([x.slug for x in category_objs]),
               'selected_varients': varient_dict,
               'categories': [x.slug for x in category_objs],
               'slug': slug
               }
    cache.set('listing-' + '_'.join(post_category) + str(varients) +
              str(page) + (slug if slug else ''), context, timeout=None)
    return JsonResponse(context)


def get_varients(category):
    branch_nodes = category.get_branch_nodes()
    varient_type = []
    varients_not_to_be_shown = product_constant.VARIENTS_NOT_TO_BE_SHOWN
    all_varients = CategoryVarient.objects.none()
    for branch_node in branch_nodes:
        obj = CategoryVarient.objects.filter(
            category=branch_node).order_by('varient_type')
        all_varients = all_varients | obj
    varient_type = all_varients.values('varient_type').distinct()
    data = {}
    for v in varient_type:
        if not {category.slug: v['varient_type']} in varients_not_to_be_shown:
            j = [str(x.value)
                 for x in all_varients.filter(varient_type=v['varient_type'])]
            data[v['varient_type']] = j
    return data, varient_type


def product_details(product_id_list):
    combo_id_list = []
    product_detail_list = []
    for obj in product_id_list:
        product_detail = {}
        product_detail['name'] = obj.name
        product_image_obj = ProductImage.objects.filter(
            product=obj).order_by('display_priority')[:1]

        product_detail['slug'] = obj.slug
        product_detail['price'] = float(obj.price)
        product_detail['id'] = obj.id
        product_detail['customizable'] = obj.is_customization_available
        product_detail['product_type'] = obj.product_type
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
        # Combo Product
        if obj.is_combo_product:
            combo_price = 0.0
            combo_price_after_discount = 0.0
            combo_product = ComboProducts.objects.filter(products=obj)[0]
            if combo_product.id in combo_id_list:
                continue
            else:
                combo_id_list.append(combo_product.id)
            product_detail['name'] = combo_product.title
            all_products = combo_product.products.all()
            product_image_obj = ProductImage.objects.filter(
                product__in=all_products).order_by('display_priority')[:1]
            for product in all_products:
                combo_price = combo_price + float(product.price)
                discount_obj = get_object_or_404(Discount, product=product)
                if discount_obj is not None:
                    if discount_obj.discount_type.lower() == "flat":
                        price_after_discount = product.price - discount_obj.discount
                    elif discount_obj.discount_type.lower() == "percentage":
                        price_after_discount = product.price - \
                            product.price * (discount_obj.discount / 100)
                    else:
                        price_after_discount = product.price
                combo_price_after_discount = combo_price_after_discount + \
                    float(price_after_discount)
            product_detail['price_after_discount'] = int(
                combo_price_after_discount)
            product_detail['price'] = combo_price
            product_detail['discount'] = [
                combo_price - combo_price_after_discount, discount_obj.discount_type]
        # Combo Product
        product_detail['product_photo_url'] = [i.get_thumbname_url()
                                               for i in product_image_obj]
        product_detail['product_tiny_photo_url'] = [i.get_tiny_image()
                                                    for i in product_image_obj]
        product_artist_map = ProductArtistDesignMap.objects.filter(product=obj)
        artist = ''
        if product_artist_map.exists():
            artist = product_artist_map[
                0].artist_design.customer.customer.customer.get_full_name()
        product_detail['artist'] = artist
        product_detail["offers"] = Offers.get_offer_on_product(obj.id),
        product_detail_list.append(product_detail)
    return product_detail_list


def list_of_products(category, varient_dict=None, min_price=None, max_price=None):
    # Not using Any Where Should be removed
    all_sub_categories = category.get_all_children()
    all_products = Product.objects.none()
    for i in all_sub_categories:
        all_products = all_products | Product.objects.filter(
            category=i, active=True)
    all_products = all_products.order_by('product_views').distinct()
    all_products_list = []
    combo_id_list = []
    for product in all_products:
        if product.is_combo_product:
            combo = ComboProducts.objects.filter(products=product)
            if combo:
                if combo[0].id in combo_id_list:
                    continue
                else:
                    combo_id_list.append(combo[0].id)
                    all_products_list.append(product)
            else:
                all_products_list.append(product)
        else:
            all_products_list.append(product)
    return filter_products(all_products_list, varient_dict, min_price, max_price)


def filter_products(products, varient_dict, min_price=None, max_price=None):
    # Not using Any Where Should be removed
    category_obj = products[0].category.first().get_main_parent()
    all_category_varients = CategoryVarient.objects.filter(
        category=category_obj)
    product_list = ProductVarientList.objects.filter(
        product__in=products).distinct()
    product_list.order_by('id')
    if min_price:
        product_list = product_list.filter(price__gte=min_price)
    if max_price:
        product_list = product_list.filter(price__lte=max_price)
    if varient_dict and len(varient_dict) > 0:
        varient_types = varient_dict.keys()
        for v in varient_types:
            if len(varient_dict[v]) > 0:
                cv_obj = all_category_varients.filter(
                    varient_type=v, value__in=varient_dict[v])
                product_list = product_list.filter(key__in=cv_obj)
    return list(set([i.product for i in product_list]) & set(products))


def all_sub_categories():
    # Not using Any Where Should be removed
    category = Category.objects.get(unique_name='tshirt')
    all_sub_categories = category.get_all_children()
    men = []
    for a in all_sub_categories:
        men.append({"name": a.name, "unique_name": a.unique_name})

    category = Category.objects.get(unique_name='tshirt')
    all_sub_categories = category.get_all_children()
    women = []
    for a in all_sub_categories:
        men.append({"name": a.name, "unique_name": a.unique_name})

    return {"men": men, "women": women}


def get_product_varients(category):
    if category and len(category) == 1:
        # if cache.has_key(category[0]):
        #     all_list = cache.get(category[0])
        #     return all_list
        category_obj = Category.objects.get(slug=category[0])
        all_varients, varient_type = get_varients(category_obj)
        cache.set(category[0], all_varients, timeout=None)
        return all_varients
    else:
        return None


@require_POST
def add_cart(request):
    print "\nuser name => ", request.user
    print "\nuser is authenticated => ", request.user.is_authenticated()
    token = ""
    token = request.COOKIES.get('token', None)
    token = None if token == 'undefined' else token
    print "\ntoken value => ", token
    product_varient_ids = request.POST.getlist("productvarientids")
    product_varients = ProductVarientList.objects.filter(
        pk__in=product_varient_ids)
    listed_in = request.POST.get("update_in")

    if not (token or request.user.is_authenticated()):
        token_value = uuid.uuid4()
        for product_varient in product_varients:
            Cart.objects.create(product_varient=product_varient, token=token_value,
                                listed_type=listed_in, product=product_varient.product)

        return JsonResponse({'success': True, 'token': str(token_value)})
    elif request.user.is_authenticated():
        if len(Cart.objects.filter(user=request.user, product_varient__in=product_varients)) == 0:
            for product_varient in product_varients:
                Cart.objects.create(
                    product_varient=product_varient, listed_type=listed_in, user=request.user, product=product_varient.product)
            cart = serializers.serialize(
                'python', Cart.objects.filter(user=request.user))
            return JsonResponse({'success': True, 'cart': cart})
    else:
        token = uuid.UUID(token)
        if len(Cart.objects.filter(token=token, product_varient__in=product_varients)) == 0:
            for product_varient in product_varients:
                Cart.objects.create(
                    product_varient=product_varient, listed_type=listed_in, token=token, product=product_varient.product)
            cart = serializers.serialize(
                'python', Cart.objects.filter(token=token))
            return JsonResponse({'success': True, 'token': str(token), 'cart': cart})
    return JsonResponse({'success': False, 'token': str(token)})


@require_POST
def tshirt_varients(request):
    pid = int(request.POST.get('id'))
    if cache.has_key("tshirt_varient" + str(pid)):
        all_list = cache.get("tshirt_varient" + str(pid))
        all_list.update({'from_cache': True})
        return JsonResponse(all_list)
    product = Product.objects.get(id=pid)
    if product.is_combo_product:
        context = combo_product_details_api(product)['all_varients']
        cache.set("tshirt_varient" + str(pid), context, timeout=None)
        return JsonResponse(context)


@require_POST
def tshirt_varient_price(request):
    pid = int(request.POST.get('id'))
    varients = request.POST.get('varients', None)
    product = Product.objects.get(id=pid)
    product_varients = []
    varient_dict = json.loads(varients) if varients else {}
    varient = None
    for pv in ProductVarientList.objects.filter(product=product):
        flag = True
        for varient_type in varient_dict.keys():
            if not pv.key.filter(varient_type=varient_type, value=varient_dict[varient_type]):
                flag = False
                break
        if flag:
            varient = pv
            break
    if varient:
        context = {
            'product_id': product.id,
            'product_varient_id': varient.id,
            'price': varient.price,
            'count': 1,
        }
        return JsonResponse(context)
    else:
        return JsonResponse({"error": 'invalid input'})


def cached_list_product(post_category, varient_dict={}, min_price=0, max_price=10000):
    varient_dict = dict(varient_dict)
    all_products_ids = []
    filter_product_ids = []
    if varient_dict.get('combo_type', None):
        combo_type = [x.upper() for x in varient_dict.get('combo_type', None)]
        for combo_product in ComboProducts.objects.filter(combo_type__in=combo_type):
            for product in combo_product.products.filter(category__in=post_category):
                set_product_cache(product)
            all_products_ids.append(str(product.id))
        del varient_dict['combo_type']
    else:
        for product in Product.objects.filter(category__in=post_category, active=True, is_combo_product=False).order_by('-id'):
            set_product_cache(product)
            all_products_ids.append(str(product.id))
    if varient_dict and not dict_is_empty(varient_dict):
        for v in varient_dict.keys():
            temp_list = []
            if varient_dict[v]:
                cvs = CategoryVarient.objects.filter(
                    Q(category__in=post_category), Q(varient_type=v), Q(value__in=varient_dict[v]) | Q(name__in=varient_dict[v]))
            else:
                cvs = CategoryVarient.objects.filter(
                    category__in=post_category, varient_type=v)

            for cv in cvs:
                if get_product_category_varient(cv):
                    temp_list = temp_list + get_product_category_varient(cv)
            if filter_product_ids:
                filter_product_ids = list(
                    set(filter_product_ids).intersection(list(set(temp_list))))
                if not filter_product_ids:
                    break
            else:
                filter_product_ids = temp_list

    else:
        filter_product_ids = all_products_ids
    detail_list = cached_product_detail(
        list(set(all_products_ids).intersection(list(set(filter_product_ids)))))
    return detail_list


def cached_product_detail(all_products_ids):
    product_list = []
    combo_id_list = []
    for product_id in all_products_ids:
        detail = get_product_from_cache(product_id)
        if detail:
            product_detail = {}
            product_detail['name'] = detail['name']
            product_detail['slug'] = detail['slug']
            product_detail['price'] = float(detail['price'])
            product_detail['id'] = detail['id']
            if detail['all_varients']:
                product_detail['colors'] = detail['all_varients'][0]['varient_values'].get(
                    'COLOR', [])
            else:
                product_detail['colors'] = []
            # product_detail['colors'] = []
            product_detail['price_after_discount'] = int(
                detail['price_after_discount'])
            product_detail['discount'] = [
                detail['discount_value'], detail['discount_type']]
            if detail['images_url']:
                product_detail['product_photo_url'] = [
                    detail['images_url'][0]['url']]
            else:
                product_detail['product_photo_url'] = []
            product_detail['artist'] = detail['artist_name']
            product_detail["offers"] = Offers.get_offer_on_product(
                str(product_id))
            product_detail['sub_type'] = get_product_subtype(product_id)
            # Combo Product
            if detail['combo_product']:
                combo_price = 0.0
                combo_price_after_discount = 0.0
                combo_product = ComboProducts.objects.filter(
                    products=product_id)[0]
                if combo_product.id in combo_id_list:
                    continue
                else:
                    combo_id_list.append(combo_product.id)
                product_detail['name'] = combo_product.title
                all_products = combo_product.products.all()
                product_image_obj = ProductImage.objects.filter(
                    product__in=all_products).order_by('display_priority')[:1]
                if not product_detail['product_photo_url']:
                    product_detail['product_photo_url'] = [
                        product_image_obj[0].get_thumbname_url()]
                for product in all_products:
                    combo_price = combo_price + float(product.price)
                    discount_obj = get_object_or_404(Discount, product=product)
                    if discount_obj is not None:
                        if discount_obj.discount_type.lower() == "flat":
                            price_after_discount = product.price - discount_obj.discount
                        elif discount_obj.discount_type.lower() == "percentage":
                            price_after_discount = product.price - \
                                product.price * (discount_obj.discount / 100)
                        else:
                            price_after_discount = product.price
                    combo_price_after_discount = combo_price_after_discount + \
                        float(price_after_discount)
                product_detail['price_after_discount'] = int(
                    combo_price_after_discount)
                product_detail['price'] = combo_price
                product_detail['discount'] = [
                    combo_price - combo_price_after_discount, discount_obj.discount_type]
            # Combo Product
            product_list.append(product_detail)
    return product_list


def dict_is_empty(varient_dict):
    for v in varient_dict.keys():
        if varient_dict[v]:
            return False
    return True


def set_product_cache(product_obj):
    # Cashing
    redis = get_redis_connection(settings.REDIS_CLIENT)
    if not redis.hgetall("product:" + str(product_obj.id)):
        # Images
        product_images = ProductImage.objects.filter(
            product=product_obj).order_by('display_priority')
        try:
            product_images_url = [
                {'url': str(pimg.get_thumbname_url()), 'id': product_obj.id,
                 'varients': [{'COLOR': ProductVarientList.objects.filter(product_image=pimg)[0].key.filter(varient_type='COLOR')[0].value}]} for pimg in product_images]
        except:
            product_images_url = [{'url': str(pimg.get_thumbname_url()), 'varients': [
            ]} for pimg in product_images]
        # Varients
        product_varients = ProductVarientList.objects.filter(
            product=product_obj)
        cate = CategoryVarient.objects.none()
        for pv in product_varients:
            cate = cate | pv.key.all()
        all_varients = cate.distinct()
        for av in all_varients:
            set_product_category_varient(av, product_obj.id)
        varient_type = all_varients.values('varient_type').distinct()
        varient_values = {}
        for v in varient_type:
            j = [str(x.value)
                 for x in all_varients.filter(varient_type=v['varient_type']).order_by('-id')]
            varient_values[v['varient_type']] = j
        # discount
        try:
            discount_obj = Discount.objects.get(product=product_obj)
            discount_value = discount_obj.discount
            discount_type = discount_obj.discount_type

            if discount_type.lower() == "flat":
                price_after_discount = product_obj.price - discount_obj.discount
            elif discount_obj.discount_type.lower() == "percentage":
                price_after_discount = product_obj.price - \
                    product_obj.price * (discount_obj.discount / 100)
            else:
                price_after_discount = obj.price
        except ObjectDoesNotExist:
            discount_value = 0
            discount_type = 'FLAT'
            price_after_discount = product_obj.price

        # size Chart
        try:
            size_chart_url = product_obj.category.all()[0].size_chart_url.url
        except Exception:
            size_chart_url = ''
        # artist
        product_artist_map = ProductArtistDesignMap.objects.filter(
            product=product_obj)
        artist = ''
        artist_link = ''
        if product_artist_map.exists():
            artist = product_artist_map[
                0].artist_design.customer.customer.customer.get_full_name()
            artist_link = '/artist/profile/' + str(product_artist_map[0].artist_design.customer.id) + '/' + str(
                product_artist_map[0].artist_design.customer.slug) + '/'
            product_artist_map[0].artist_design.customer.id
            product_images_url.append(
                {'url': product_artist_map[0].artist_design.get_thumbname_url(), 'varients': {}})
        # tags
        tags = [product_tag.tag.tag for product_tag in ProductTagMap.objects.filter(
            product=product_obj)]
        context = {
            "category": product_obj.category.all()[0].slug,
            "combo_product": product_obj.is_combo_product,
            "views": product_obj.product_views,
            "id": product_obj.id,
            "slug": product_obj.slug,
            "name": product_obj.name,
            "price": int(product_obj.price),
            "images_url": product_images_url,
            "all_varients": [{'varient_values': varient_values, 'product_id': product_obj.id, 'title': ""}],
            "discount_value": int(discount_value),
            "discount_type": discount_type,
            "price_after_discount": int(price_after_discount),
            "description": product_obj.description,
            "is_discontinued": not product_obj.active,
            "title": "",
            "size_chart_url": size_chart_url,
            "artist_name": artist,
            "artist_link": artist_link,
            "offers": Offers.get_offer_on_product(str(product_obj.id)),
            "tags": tags,
        }
        redis.hset("product:" + str(product_obj.id), "detail", context)


def set_product_category_varient(category_varient, product_id):
    key = "cv_" + category_varient.category.slug + \
        category_varient.varient_type + category_varient.value
    if cache.has_key(key):
        product_list = cache.get(key)
        product_list.append(str(product_id))
        cache.set(key, list(set(product_list)), timeout=None)
    else:
        cache.set(key, [str(product_id)], timeout=None)
    return True


def get_product_category_varient(category_varient):
    key = "cv_" + category_varient.category.slug + \
        category_varient.varient_type + category_varient.value
    if cache.has_key(key):
        return cache.get(key)
    return None


def get_product_from_cache(product_id):
    redis = get_redis_connection(settings.REDIS_CLIENT)
    if redis.hgetall("product:" + str(product_id)):
        detail = redis.hget("product:" + str(product_id), "detail")
        if detail:
            return ast.literal_eval(detail)
    try:
        product = Product.objects.get(id=product_id)
        set_product_cache(product)
        return get_product_from_cache(product.id)
    except ObjectDoesNotExist:
        return None


def get_product_subtype(product_id):
    type_list = ['All']
    product_details = get_product_from_cache(product_id)
    # define subtype conditions here
    key = "cv_" + 'tshirt' + 'SLEEVES' + 'FULL SLEEVES'
    if cache.has_key(key):
        if str(product_id) in cache.get(key):
            type_list.append('FULL SLEEVES')
    key = "cv_" + 'tshirt' + 'SLEEVES' + 'HALF SLEEVES'
    if cache.has_key(key):
        if str(product_id) in cache.get(key):
            type_list.append('HALF SLEEVES')
    return type_list


size_const = {'S': '(Small)',
              'M': '(Medium)',
              'L': '(Large)',
              'XL': '(Extra Large)',
              'XXL': '(Extra Extra Large)',
              'XS': '(Extra Small)',
              '3XL': '(Plus Size)',
              '4XL': '(Plus Size)',
              '5XL': '(Plus Size)'}


def get_page_title(categories, varients):
    title = ""
    local_var = dict(varients)
    if categories and len(categories) == 1:
        for varients in list(OrderedSet(product_constant.VARIENT_PREFRENCE[categories[0].lower()]) & set(local_var.keys())):
            title = title + ','.join(local_var[varients]) + ' '
        return (title + categories[0]).title() + ' - Addiction Bazzar'
    elif local_var.get('GENDER', None) and local_var['GENDER'] == 'MEN':
        return "Men's Clothing" + ' - Addiction Bazzar'
    elif local_var.get('GENDER', None) and local_var['GENDER'] == 'WOMEN':
        return "Women's Clothing" + ' - Addiction Bazzar'
    else:
        return "Addiction Bazaar - Customize Clothing Online"


def get_page_heading(categories, varients):
    local_var = dict(varients)
    category = "Products"
    heading = ""
    head = "Couple's  "
    if categories and len(categories) == 1:    # discount = request.POST.get("discount", None)
        category = categories[0].title() + 's '

    if local_var.get('GENDER', None) and len(local_var['GENDER']) == 1 and local_var['GENDER'][0] == 'MALE':
        heading += "Men's "
    elif local_var.get('GENDER', None) and len(local_var['GENDER']) == 1 and local_var['GENDER'][0] == 'FEMALE':
        heading += "Women's "
    if local_var.get('TYPE', None) and len(local_var['TYPE']) == 1 and local_var['TYPE'][0] == 'PLAIN':
        heading += "Plain "
    elif local_var.get('TYPE', None) and len(local_var['TYPE']) == 1 and local_var['TYPE'][0] == 'PRINTED':
        heading += "Printed "
    if local_var.get('SLEEVES', None) and len(local_var['SLEEVES']) == 1 and local_var['SLEEVES'][0] == 'HALF SLEEVES':
        heading += "Half "
    elif local_var.get('SLEEVES', None) and len(local_var['SLEEVES']) == 1 and local_var['SLEEVES'][0] == 'FULL SLEEVES':
        heading += "Full "

    if local_var.get('COLOR', None) and len(local_var['COLOR']) == 1:
        heading += local_var['COLOR'][0].title() + ' '

    return heading + category


def get_breadcum(categories, varients):
    bread_crumb = []
    bread_crumb_page_title = ''
    bread_crumb.append({'link': '/', 'value': 'Home'})
    gender_in_varients = varients.get('GENDER', None)
    if gender_in_varients:
        if gender_in_varients[0] == 'MALE':
            bread_crumb.append(
                {'link': '/mens-clothing/', 'value': "Men's Clothing"})
        elif gender_in_varients == 'FEMALE':
            bread_crumb.append({'link': '/womens-clothing/',
                                'value': "Women's Clothing"})
        del varients['GENDER']
    if len(categories) == 1:
        bread_crumb.append({'link': '/products/' + categories[0].lower() +
                            '/', 'value': categories[0].lower()})
        p_title = categories[0]
    else:
        p_title = "Products"
    if varients:
        for v in varients.values():
            bread_crumb_page_title += ','.join(v).title()
            bread_crumb_page_title += ' '
        bread_crumb.append(
            {'link': '', 'value': bread_crumb_page_title + p_title})
    return bread_crumb
