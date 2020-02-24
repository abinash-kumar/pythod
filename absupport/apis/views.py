from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from abutils.apex_apis import APEXApiIntegration
from absupport.models import Pincode
from product.models import Category
from product.models import CategoryVarient
from product.models import Product
from product.models import (Cart, Category, CategoryVarient, ComboProducts,
                            Discount, Product, ProductImage,
                            ProductVarientList, Seller)
from auraai.models import (ProductTagMap, Tag)
import requests
import yaml
import ast
from product import constant

# from django.db import models
from django.contrib.auth.models import User
import itertools
import json
from absupport.forms import ProductImageForm
from django.shortcuts import get_object_or_404, render



# Url = http://127.0.0.1:8000/ab/apis/bank/ifsc/?ifsc=SBIN0015282

def dashboard_new(request):
    if False and not (request.user.is_authenticated() and request.user.is_staff):
        return HttpResponseRedirect("/login/")
    else:
        context = {}
        return render(request, "absupport/dashboardnew.html", context)


@require_POST
def bank_ifsc(request):
    req_url = "https://ifsc.razorpay.com/"
    ifsc = request.POST.get("ifsc", None)
    return JsonResponse({'success': False, 'error': 'ifsc mandetory'})
    if ifsc:
        try:
            resp = requests.get(req_url + ifsc)
            data = yaml.load(resp.content)
            if data == 'Not Found':
                return JsonResponse({'success': False, 'error': 'invalid ifsc'})
            for key in data.keys():
                if data[key]:
                    data.update(
                        {key: data[key].encode('ascii', errors='ignore')})
            data.update({'success': True})
            return JsonResponse(data)
        except TypeError:
            return JsonResponse({'success': False, 'error': 'invalid ifsc'})
    else:
        return JsonResponse({'success': False, 'error': 'ifsc mandetory'})


@require_POST
def check_payment_modes_pincode(request):
    # Temporary method from pincode id hard coded to mumbai(dimention label)
    pincode = request.POST.get("pincode", None)
    if pincode:
        context = {}
        data_cod, random = APEXApiIntegration().is_service_available('400049',
                                                                     pincode,
                                                                     'cod',
                                                                     '0.5',
                                                                     'standard',
                                                                     'nondoc',
                                                                     'air',
                                                                     '1', '1', '1', '1')
        partners = data_cod.get('apilist', None)
        if partners and len(partners) > 0:
            context.update(
                {'cod': True, 'delivery_partners_cod_no': len(partners)})
        else:
            context.update(
                {'cod': False, 'error_cod': 'no delivery partners avelable'})

        data_online, random = APEXApiIntegration().is_service_available('400049',
                                                                        pincode,
                                                                        'online',
                                                                        '0.5',
                                                                        'standard',
                                                                        'nondoc',
                                                                        'air',
                                                                        '1', '1', '1', '1')
        partners = data_online.get('apilist', None)
        if partners and len(partners) > 0:
            context.update(
                {'online': True, 'delivery_partners_online_no': len(partners)})
        else:
            context.update(
                {'online': False, 'error_online': 'no delivery partners avelable'})

    else:
        context = {'succcess': False, 'error': 'pincode mandetory'}

    context.update({'pincode': pincode})
    return JsonResponse({'cod': True, 'online': True,'succcess': False})
    # return JsonResponse(context)


@require_POST
def check_pincode(request):
    pincode = request.POST.get("pincode", None)
    if pincode:
        pincode_obj = Pincode.objects.filter(pincode=pincode)
        if pincode_obj:
            return JsonResponse({'success': True, 'city': pincode_obj[0].city, 'state': pincode_obj[0].state})
    return JsonResponse({'success': False, 'city': '', 'state': ''})


@csrf_exempt
@require_POST
def add_category(request):
    new_category_name = request.POST.get("category_name", None)
    new_url = request.POST.get("size_chart_url", None)

    # user_object = User.objects.get(id=request.user.id)
    cat_obj = Category.objects.create(
            name=new_category_name,
            publisher="user_object.first_name + " " + user_object.last_name",
        )
    cat_obj.size_chart_url = new_url
    cat_obj.save()

    return JsonResponse({"success": "true"})

@csrf_exempt
@require_POST
def add_category_varient(request):
    # new_category_varient = request.POST.get("", None)
    category = request.POST.get("category", None)
    cat_obj = Category.objects.get(name=category)
    try:
        varient_type = request.POST.get("varient_type", None)
    except Exception:
        return JsonResponse({"error": "Repeated varient_type"})

    value = request.POST.get("value", None)
    try:
        name = request.POST.get("name", None)
    except Exception:
        return JsonResponse({"error": "Repeated varient_type"})

    # import ipdb; ipdb.set_trace()
    catvar_obj = CategoryVarient.objects.create(
        category= cat_obj,
        varient_type=varient_type,
        value=value,
        name=name,
        )


    




    return JsonResponse({'success': "true"})


@csrf_exempt
def get_category(request):


    active_obj = Category.objects.filter(active="True")
    all_categories = []
    for cat in active_obj:
        all_categories.append(cat.name)
    return JsonResponse({'all_categories': all_categories})

    

@require_POST
@csrf_exempt
def get_category_varient(request):

    cat = request.POST.get("cat", None)

    # cat_var = CategoryVarient.objects.all60
    d = []
    c = CategoryVarient.objects.all()
    var = constant.PRODUCT_VARIENTS
    d = var[cat]

    # return JsonResponse({'category_varients_type , value , name ': d , 'name ': g,'value ': f,'varient_type ': e})
    return JsonResponse({'category_varients': d})


@csrf_exempt
@require_POST
def add_product(request):
    seller = request.POST.get("seller", None)
    seller_obj = Seller.objects.get(seller__id=int(seller))
    name = request.POST.get("name", None)
    description = request.POST.get("description", None)
    price = request.POST.get("price", None)
    category = request.POST.get("category", None)
    cat_obj = Category.objects.get(name=category)
    active = request.POST.get("active", None)
    is_feature_product = request.POST.get("is_feature_product", None)
    is_customization_available = request.POST.get("is_customization_available", None)
    customization_details = request.POST.get("customization_details", None)
    obj = Product.objects.create(
            seller = seller_obj,
            name = name,
            description = description,
            price = int(price),
            wholesale_price = int(price),
            active = not not active,
            is_feature_product = not not is_feature_product,
            is_customization_available = not not is_customization_available,
            customization_details = customization_details,

        )        
    obj.category.add(cat_obj)
    discount = request.POST.get("discount")
    discount_type = request.POST.get("discount_type")

    discount_obj = Discount.objects.create(
        product= obj,
        discount= int(discount),
        discount_type= discount_type,
        )
    return JsonResponse({"success": "true", "category": category, 'product_id': obj.id, 'seller_id': seller_obj.pk, 'price': price})

@csrf_exempt
@require_POST
def add_product_varient(request):
    product_id = request.POST.get('product_id', None)
    image_varient = request.POST.get('imageVarient', None)
    varient = request.POST.get('varient', None)
    price = request.POST.get('price', None)
    seller = request.POST.get('seller_id', None)
    category = request.POST.get('category', None)
    
    seller_obj = Seller.objects.get(id=int(seller))
    product_obj = Product.objects.get(id=int(product_id))
    category_obj = Category.objects.get(name=category)

    image_varient_list = ast.literal_eval(image_varient)
    varient_list = ast.literal_eval(varient)
    all_combinations = get_all_varients(image_varient_list, varient_list)
    image_varient_map = create_image_varient_map(image_varient_list)
    product_varient_required_data = []
    for each_combination in all_combinations:
        product_varient_required_data.append(
                        {'key': each_combination,
                        'image_id': get_image_id(each_combination, image_varient_map)
                        }
                    )
    for data in product_varient_required_data:
        product_image_obj = ProductImage.objects.get(id=data['image_id'])
        pv = ProductVarientList.objects.create(
                product=product_obj,
                price=float(price),
                product_image=product_image_obj
            )
        pv.sellers.add(seller_obj)
        for cat_var in data['key']:
            (k, v), = cat_var.items()
            cv = CategoryVarient.objects.get(category=category_obj, varient_type=k, value=v)
            pv.key.add(cv)
    return JsonResponse({"success": "true", 'product_url': "https://www.addictionbazaar.com/" + product_obj.get_absolute_url()})

def create_image_varient_map(image_varient_list):
    require_data = {}
    for v in image_varient_list:
        if v['imageId'] in require_data.keys():
            require_data[v['imageId']].append({v['varientType']: v['value']})
        else:
            require_data[v['imageId']] = [{v['varientType']: v['value']}]
    return require_data

def get_image_id(each_combination, image_varient_map):
    for image_id, varient_dict_list in image_varient_map.iteritems():
        if all(i in each_combination for i in varient_dict_list):
            x = image_id
    return x

def get_all_varients(image_varient_list, varient_list):
    mykeys = {}
    for i in image_varient_list + varient_list:
        if i['varientType'] in mykeys.keys() and i['value'] not in mykeys[i['varientType']]:
            mykeys[i['varientType']].append(i['value'])
        else:
            mykeys[i['varientType']] = [i['value']]
    list_of_varient_list = []
    for key, values in mykeys.iteritems():
        each_list = []
        for item in values:
            each_list.append({key: item})
        list_of_varient_list.append(each_list)
    cartesian_product = itertools.product(*list_of_varient_list)
    return list(cartesian_product)


@require_POST
@csrf_exempt
def get_all_category_varient(request):
    cat = request.POST.get("category_name", None)
    obj = CategoryVarient.objects.filter(category__name=cat)
    all_varients = []
    for var in obj:
        all_varients.append(model_to_dict(var))
    return JsonResponse({'all_category_varients': all_varients})



@require_POST
@csrf_exempt
def add_product_image(request):
    uid = request.session.get('_auth_user_id')
    product_id = request.POST.get('product_id')
    try:
        product = Product.objects.get(pk=int(product_id))
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            json = []
            for image in request.FILES.values():
                instance = ProductImage(product_photo=image)
                instance.product = product
                instance.save()
                json.append(instance.get_detailed_json())
            return JsonResponse({'images': json})
        else:
            context = {'success': False}
    except ObjectDoesNotExist:
        context = {'success': False}
    return JsonResponse(context)


@require_POST
@csrf_exempt
def add_product_tag(request):
    product = request.POST.get("product", None)
    product_obj = Product.objects.get(name=product)
    tags = request.POST.get("tag", None)
    tag_obj = Tag.objects.get(tag=tags)
    obj = ProductTagMap.objects.create(
        product = product_obj,
        tag = tag_obj,
        )
    return JsonResponse({"success": "true"})
# @csrf_exempt
# @require_POST
# def discount(request):
#     product = request.POST.get("product")
#     product_obj = Product.objects.get(name=product)
#     discount = request.POST.get("discount")
#     discount_type = request.POST.get("discount_type")

#     discount_obj = Discount.objects.create(
#         product= product_obj,
#         discount= discount,
#         discount_type= discount_type,
#         )
#     return JsonResponse({"success": "true"})

# @csrf_exempt
# @require_POST
# def comboproducts(request):
#     product = request.POST.get("product")
#     product_obj = Product.objects.get(name=product)
#     title = request.POST.get("title")
#     description = request.POST.get("description")
#     combo_type = request.POST.get("combo_type")

#     combo_obj = ComboProducts.objects.create(
#         products = product_obj,
#         title = title,
#         description = description,
#         combo_type = combo_type,
#         )

#     return JsonResponse({"success": "true"})

# def delete_category(request, id=None):
#     cat = get_object_or_404(category, id=id)
#     cat.delete()

#     return JsonResponse({"success": "true"})



    



