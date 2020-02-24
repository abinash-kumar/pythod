from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect

from django.views.decorators.http import require_POST

from django.contrib.auth.models import User
from social.apps.django_app.default.models import UserSocialAuth
from django.utils.safestring import mark_safe
from requests.exceptions import ConnectionError
from codeab.settings import SOCIAL_AUTH_FACEBOOK_KEY, SOCIAL_AUTH_FACEBOOK_SECRET
from product.models import Product, Category, ProductImage
from .models import Tag, ProductTagMap
from customer.models import Customer

import requests
import yaml
import ast
import logging

from .models import UserFbLikes, UserFbDetails
from django.views.decorators.cache import never_cache

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

# Create your views here.
redirect_uri = "/aura/fb/request2/"
#redirect_uri = "http://local.addictionbazaar.com:8000/aura/fb/request2/"
app_id = str(SOCIAL_AUTH_FACEBOOK_KEY)
app_secret = SOCIAL_AUTH_FACEBOOK_SECRET

logger = logging.getLogger('django')


def fb_access_url_request():
    redirect_uri = "https://www.addictionbazaar.com/aura/fb/request/"
    scope = 'email,user_likes'
    url = "https://www.facebook.com/v2.10/dialog/oauth?client_id=" + app_id + \
        "&display=popup&response_type=code&redirect_uri=" + redirect_uri + 'scope=' + scope
    return url


def fb_declined_access_url_request(request, list_scope):
    if request.is_secure():
        host = 'https://' + str(request.META['HTTP_HOST'])
    else:
        host = 'http://' + str(request.META['HTTP_HOST'])
    #redirect_uri = "https://www.addictionbazaar.com/aura/fb/request2/"
    scope = ','.join(list_scope)
    url = "https://www.facebook.com/v2.10/dialog/oauth?client_id=" + app_id + \
        "&redirect_uri=" + host + redirect_uri + "&auth_type=rerequest&scope=" + scope
    return url


def get_fb_data(request):
    scope = ['email', 'user_likes']
    link = fb_declined_access_url_request(request, scope)
    return render(request, "fbpermissions.html", {'link': mark_safe(link)})


def get_fb_data2(request):
    redirect_page = "/"
    try:
        code = request.GET.get('code', None)
        if code:
            token = get_fb_token_from_code(request, code)
            if token:
                declined_permissions = get_declined_permissions(token)
                if 'email' not in declined_permissions:
                    logger.warning("token-----------> " + token)
                    logger.warning(get_fb_email(token))
                    email, fb_id = get_fb_email(token)
                    if fb_id:
                        user = request.user
                        fbuser = UserFbDetails.objects.filter(user=user)
                        if len(fbuser) == 0:
                            fbuser = UserFbDetails.objects.create(
                                user=user, token=token)
                            if email:
                                customer = Customer.objects.get(customer=user)
                                fbuser.user_email = email
                                fbuser.save()
                                customer.is_email_verified = True
                                customer.save()

                        else:
                            fbuser[0].token = token
                            fbuser[0].save()
                        if 'user_likes' not in declined_permissions:
                            likes = get_likes(token)
                            if len(likes) > 0:
                                redirect_page = '/aura/magic/search/'
                                UserFbLikes.objects.filter(user=user).delete()
                                for like in likes:
                                    UserFbLikes.objects.create(user=user, fb_page=like[
                                                               'name'], page_id=like['id'])
    except ConnectionError:
        print 'Connection Error!!!'
    host = str(request.get_host())
    response = HttpResponseRedirect("http://" + host + redirect_page)
    response.set_cookie("isSignIn", "true")
    return response


def get_fb_token_from_code(request, code):
    # redirect_uri = "https://www.addictionbazaar.com/"
    if request.is_secure():
        host = 'https://' + str(request.META['HTTP_HOST'])
    else:
        host = 'http://' + str(request.META['HTTP_HOST'])
    url = "https://graph.facebook.com/v2.10/oauth/access_token?client_id=" + app_id + \
        "&redirect_uri=" + host + redirect_uri + \
        "&client_secret=" + app_secret + "&code=" + code
    resp = requests.get(url)
    data = yaml.load(resp.content)
    try:
        access_token = data['access_token']
        return access_token
    except KeyError:
        print data
        return None


def get_declined_permissions(token):
    url = 'https://graph.facebook.com/me/permissions?access_token=' + token
    resp = requests.get(url)
    data = yaml.load(resp.content)
    l = []
    for d in data['data']:
        if d['status'] != 'granted':
            l.append(d['permission'])

    return l


def get_fbid_firstname_lastname_age_gender(token):
    url = "https://graph.facebook.com/v2.10/me/?fields=first_name%2Clast_name%2Cage_range%2Cgender&access_token=" + token
    resp = requests.get(url)
    data = yaml.load(resp.content)
    fbid = data['id']
    first_name = data['first_name']
    last_name = data['last_name']
    age_range = data['age_range']['min']
    gender = data['gender']
    return fbid, first_name, last_name, age_range, gender


def get_fb_email(token):
    url = "https://graph.facebook.com/v2.10/me/?fields=email&access_token=" + token
    resp = requests.get(url)
    data = yaml.load(resp.content)
    try:
        email = data['email']
    except KeyError:
        email = None

    try:
        uid = data['id']
    except KeyError:
        uid = None

    return email, uid


def get_likes(token):
    url = "https://graph.facebook.com/v2.10/me/?fields=likes.limit(100)&access_token=" + token
    resp = requests.get(url)
    data = ast.literal_eval(resp.content)
    try:
        likes = data['likes']['data']
    except KeyError:
        return []

    flag = True
    try:
        nxt = data['likes']['paging']['next']
        url = nxt.replace("\\", "")
    except KeyError:
        flag = False
    while(flag):
        resp = requests.get(url)
        data = ast.literal_eval(resp.content)
        likes = likes + data['data']
        try:
            nxt = data['paging']['next']
            url = nxt.replace("\\", "")
        except KeyError:
            flag = False
    return likes


def google_sign_in(request):
    host = str(request.get_host())
    response = HttpResponseRedirect("http://" + host + '/')
    response.set_cookie("isSignIn", "true")
    return response


@never_cache
def product_list(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')
    cat_id = request.POST.get('cat_id', None)


    categories = Category.objects.all()

    paginator = Paginator(Product.objects.all().order_by('id'), 15) # Show 25 contacts per page

    page = request.GET.get('page')




    try:
        productss = paginator.page(page)
    except PageNotAnInteger:
        productss = paginator.page(1)
    except EmptyPage:
        productss = paginator.page(paginator.num_pages)

    # import ipdb; ipdb.set_trace()
    if cat_id:
        category = Category.objects.get(id=cat_id)
        products = Product.objects.filter(category=category)

    else:
        products = Product.objects.all()
    product_tags = []
    for product in productss.object_list:
        tags = ProductTagMap.objects.filter(product=product)
        product_tags.append({'product': product, 'tags': tags})
        
    context = {'products': product_tags, 'categories': categories, "object_list": productss  }
    return render(request, 'auraai/product_list_tag.html', context)



def listing(request):
    contact_list = Contacts.objects.all()


    return render(request, 'list.html', {'contacts': contacts})


@never_cache
def manage_tags(request, id):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')
    new_tags = request.POST.get('new_tags', None)
    product = Product.objects.get(id=id)
    category = product.category.all()[0]
    product_image = ProductImage.objects.filter(product=product)
    image_url = ''
    if len(product_image) > 0:
        image_url = product_image[0].product_photo.url
    product_tags = ProductTagMap.objects.filter(product=product)
    if new_tags:
        new_tags = new_tags.strip()
        new_tags_list = new_tags.split(',')
        for tag in new_tags_list:
            t = tag.strip()
            tag_l = Tag.objects.filter(tag=t, category=category)
            if len(tag_l):
                tag = Tag.objects.get(tag=t, category=category)
            else:
                tag = Tag.objects.create(category=product.category.all()[0], tag=t)
            tag_map = ProductTagMap.objects.filter(tag=tag, product=product)
            if len(tag_map) == 0:
                ProductTagMap.objects.create(tag=tag, product=product)

    return render(request, 'auraai/add_product_tag.html', {'product': product, 'tags': product_tags, 'image_url': image_url})


@never_cache
def product_tag_search(request):
    return render(request, 'auraai/product_tag_search.html', {})


def fb_magic_search(request):
    return render(request, 'auraai/fb_magic_search.html', {})


def refresh_search_page(request):
    if not (request.user.is_authenticated() and request.user.is_staff):
        return HttpResponseRedirect("/login/")
    return render(request, 'auraai/refresh_search_page.html', {})
