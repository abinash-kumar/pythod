import json

from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.core.cache import cache
from codeab.celery import app
from auraai.models import Tag, ProductTagMap, TagBanner, UserFbLikes
from product.models import Product, ProductVarientList, CategoryVarient
from product.apis import views as product_view
from redisearch import Client, TextField, Suggestion, AutoCompleter, Query


@require_POST
def search_tags(request):
    search_key = request.POST.get('search_key', None)
    if search_key:
        tags = Tag.objects.filter(tag__icontains=search_key).distinct()
        data = []
        for tag in tags:
            data.append({'id': tag.id, 'tag': tag.tag})
        context = {'tags': data}
    else:
        context = {'tags': []}
    return JsonResponse(context)


@require_POST
def get_all_products_by_tag_name(request):
    # product = request.POST.get('product', None)
    tag = request.POST.get('tag', None)
    if cache.has_key('tB-' + tag):
        all_list = cache.get('tB-' + tag)
        all_list.update({'from_cache': True})
        return JsonResponse(all_list)
    tag = request.POST.get('tag', None)
    tags = tag.split(',')
    varients = request.POST.get('varients', None)
    varient_dict = json.loads(varients) if varients else {}
    if tag:
        banner_objs = TagBanner.objects.filter(slug__in=tags)
        tag_objs = Tag.objects.none()
        for banner in banner_objs:
            tag_objs = tag_objs | banner.tags.all()

        products = []
        for i in tag_objs.distinct():
            products = products + \
                [i.product.id for i in ProductTagMap.objects.filter(
                    tag=i, product__active=True)]
        product_list = product_view.cached_product_detail(list(set(products)))
        product_list.sort(key=lambda x: x['id'], reverse=True)
        context = {
            'success': True,
            "product_detail_list": product_list,
            'count': len(products),
            'total_number_of_products': len(products),
            'no_of_products': len(products),
            'subtypes': True,
            "page_title": "Addiction Bazaar - T-Shirts " + ', '.join([banner.banner_name for banner in banner_objs])
        }
    else:
        context = {'success': False, 'error': 'no products'}
    cache.set('tB-' + tag, context, timeout=None)
    return JsonResponse(context)


@require_POST
def get_tags_of_product(request):
    product_id = request.POST.get('product_id', None)
    if product_id:
        product = Product.objects.get(id=product_id)
        tag_maps = ProductTagMap.objects.filter(product=product)
        data = []
        for tag_map in tag_maps:
            data.append({'id': tag_map.tag.id, 'tag': tag_map.tag.tag})

        context = {'tags': data}
    else:
        context = {'tags': []}
    return JsonResponse(context)


@require_POST
def get_all_banners(request):
    banners = TagBanner.objects.filter(active=True)
    data = []
    for banner in banners:
        data.append({'id': banner.id,
                     'name': banner.banner_name,
                     'image': banner.banner_image.url,
                     'slug': banner.slug})

    context = {'banners': data}
    return JsonResponse(context)


@require_POST
def search_products_by_tag(request):
    search_key = request.POST.get('search_key', None)
    if search_key:
        tags = Tag.objects.filter(tag__icontains=search_key).distinct()
        products = ProductTagMap.objects.none()
        for tag in tags:
            products = products | ProductTagMap.objects.filter(tag=tag)
        products = products.distinct()
        data = []
        for product in products:
            data.append(product.product.id)

    context = {'product_id': data}
    return JsonResponse(context)


@require_POST
def get_products_by_banner(request):
    banner_id = request.POST.get('banner_id', None)
    if banner_id:
        banner = TagBanner.objects.get(id=banner_id)
        tags = banner.tags.all()
        products = ProductTagMap.objects.none()
        for tag in tags:
            products = products | ProductTagMap.objects.filter(tag=tag)
        products = products.distinct()
        data = []
        for product in products:
            data.append(product.product.id)
        data = list(set(data))
        context = {'success': True, 'products': data, 'count': len(
            data), 'banner_id': banner_id, 'banner_name': banner.banner_name, 'banner_image': banner.banner_image.url}
    else:
        context = {'success': False, 'error': 'invalid Banner Id'}

    return JsonResponse(context)


@require_POST
def product_search(request):
    search_key = request.POST.get('search_key', "").strip()
    if len(search_key) == 0:
        return JsonResponse({'product_detail_list': []})
    for t in ['tee', 't shirt', 't-shirt', 'tees', 't shirts', 't-shirts', 'tshirts']:
        search_key = 'tshirt' if search_key == t else search_key
    client = Client('productIndex')
    q = Query(search_key)
    q.paging(0, 60)
    product_id_list = []
    try:
        res = client.search(q)
        for data in res.docs:
            product_id_list.append(data.id)
    except Exception:
        index = create_product_search_index()
        create_product_autocompleter()
        res = client.search(q)
        for data in res.docs:
            product_id_list.append(data.id)
    if len(product_id_list) == 0:
        sk = search_key.split()
        for substr in sk:
            if len(substr) > 0:
                q._query_string = substr
                res = client.search(q)
                for data in res.docs:
                    product_id_list.append(data.id)
        product_id_list = list(set(product_id_list))
    product_detail_list = product_view.cached_product_detail(product_id_list)
    context = {'product_detail_list': product_detail_list,
               'total_number_of_products': len(product_detail_list),
               'no_of_products': len(product_detail_list),
               'subtypes': True, }
    return JsonResponse(context)


@require_POST
def product_autocomplete(request):
    autocomplete_key = request.POST.get('autocomplete_key', "").strip()
    if len(autocomplete_key) == 0:
        return JsonResponse({'autocomplete_values': []})
    auto_completer = AutoCompleter('productAutocompleter')
    autocomplete_values = []
    if auto_completer.len() == 0:
        create_product_autocompleter()
    res = auto_completer.get_suggestions(autocomplete_key, fuzzy=True)

    for acv in res:
        autocomplete_values.append(str(acv))
    context = {'autocomplete_values': autocomplete_values}
    return JsonResponse(context)


def create_product_search_index():
    create_product_search_index_async.delay()


@app.task
def create_product_search_index_async():
    print 'Creating Search Index'
    client = Client('productIndex')
    client.create_index([TextField('title', weight=5.0),
                         TextField('description'),
                         TextField('tags'),
                         TextField('category')])
    products = Product.objects.filter(active=True)
    cache.set('Search_index_total', len(products), timeout=None)
    index = 0
    for product in products:
        title = product.name
        description = product.description
        category = ','.join([cat.name for cat in product.category.all()])
        tag = product.tags
        tag_maps = ProductTagMap.objects.filter(product=product)
        for tag_map in tag_maps:
            tag = tag + tag_map.tag.tag + ' '
        category_varients = []
        for pv in ProductVarientList.objects.filter(product=product):
            for cv in pv.key.all():
                category_varients.append(cv.value)
        tag += ' '.join(list(set(category_varients)))
        client.add_document(str(product.id),
                            title=title,
                            description=description,
                            tags=tag,
                            category=category)
        cache.set('Search_index_index', index, timeout=None)
        index += 1
    return True


def create_product_autocompleter():
    auto_completer = AutoCompleter('productAutocompleter')
    products = Product.objects.filter(active=True)
    for product in products:
        title = product.name
        category = product.category.name
        auto_completer.add_suggestions(Suggestion(
            title, 5.0), Suggestion(category, 3.0))
    for tag in Tag.objects.all():
        auto_completer.add_suggestions(Suggestion(tag.tag, 5.0))

    for cv in CategoryVarient.objects.all():
        auto_completer.add_suggestions(Suggestion(cv.value, 2.0))
    return True


def refresh_search_keys(request):
    if (request.user.is_authenticated() and request.user.is_staff):
        client = Client('productIndex')
        total_old_docts = client.info()['num_docs']
        delete_status = client.drop_index()
        new_index = False
        if delete_status == 'OK':
            new_index = create_product_search_index()
        auto_completer = AutoCompleter('productAutocompleter')
        auto_completer_old_count = auto_completer.len()
        create_product_autocompleter()
        auto_completer_new_count = auto_completer.len()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def refresh_search_status(request):
    if cache.has_key('Search_index_total'):
        total = cache.get('Search_index_total')
    else:
        total = 0

    if cache.has_key('Search_index_index'):
        indexed = cache.get('Search_index_index')
        indexed += 1
    else:
        indexed = 0
    context = {'total': total, 'indexed': indexed}
    return JsonResponse(context)


@require_POST
def magic_fb_search(request):
    if not request.user.is_authenticated():
        return JsonResponse({'product_detail_list': []})
    user = request.user
    client = Client('productIndex')
    try:
        # if search indes is not there it will create a search index
        res = client.search('test')
    except Exception:
        index = create_product_search_index()
        create_product_autocompleter()  # up to here

    fb_likes = UserFbLikes.objects.filter(user=user)
    likes_product_map = {}

    for fb_like in fb_likes:
        try:
            res = client.search(fb_like.fb_page)
            for data in res.docs:
                likes_product_map.update(
                    {str(data.id): likes_product_map.get(str(data.id), []) + [fb_like.fb_page]})
        except Exception:
            print fb_like.fb_page
    product_list = Product.objects.filter(
        id__in=likes_product_map.keys()).order_by('-id')
    product_detail_list = product_view.product_details(product_list)
    for i in range(len(product_detail_list)):
        product_id = str(product_detail_list[i].get('id'))
        likes = likes_product_map.get(product_id)
        product_detail_list[i].update({'fb_likes': list(set(likes))})

    context = {'product_detail_list': product_detail_list}
    return JsonResponse(context)
