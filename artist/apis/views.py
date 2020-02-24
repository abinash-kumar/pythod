
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from artist.models import ArtistDesign, ArtistDetail, ProductArtistDesignMap, SocialLink, ArtistBankDetail
from customer.models import Customer
from notification.models import Notification
from product.apis.views import product_details
from artist.forms import ArtistDesignEditForm
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from abutils.utils import create_products


@require_POST
def get_artist_designs(request):
    # if not request.user.is_authenticated():
    #     return JsonResponse({'error':'not authenticated'})
    status = request.POST.get('status', None)
    is_slider_images = request.POST.get('isSlider', None)
    customer = Customer.objects.get(customer=request.user)
    try:
        artist = ArtistDetail.objects.get(customer=customer)
        data = []
        designs = ArtistDesign.objects.filter(customer=artist)
        slider_list = []
        if status:
            designs = designs.filter(status=status.upper())
        for design in designs:
            data.append({'id': design.id, 'title': design.title, 'status': design.status,
                         'comment': design.comment, 'tags': design.tags, 'image': design.get_thumbname_url()})
            slider_list.append(
                {'image': design.design.url, 'title': design.title, 'description': design.comment})
        if is_slider_images == 'true':
            context = {
                'success': True,
                'active_slider': [],
                'slider_list': slider_list,
            }
        else:
            context = {'designs': data, 'count': len(designs)}
    except ObjectDoesNotExist:
        context = {'designs': []}
    return JsonResponse(context)


@require_POST
def edit_artist_designs(request):
    design_id = request.POST.get('design_id', None)
    comment = request.POST.get('comment', None)
    tags = request.POST.get('tags', None)
    title = request.POST.get('title', None)
    f = request.FILES.get('design', None)
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)

    if not design_id:
        return JsonResponse({'success': False, 'msg': 'design Id mandetory'})

    customer = Customer.objects.get(customer=user)
    try:
        artist = ArtistDetail.objects.get(customer=customer)
        artist_design = ArtistDesign.objects.get(id=design_id)
        if title and len(title) > 0:
            artist_design.title = title
        if comment and len(comment) > 0:
            artist_design.comment = comment
        if tags and len(tags) > 0:
            artist_design.tags = tags
        artist_design.save()
        form = ArtistDesignEditForm(
            request.POST or None, request.FILES or None, instance=artist_design)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            instance.create_thumbnail()
            create_products(instance.design.path, instance.id)
        context = {'success': True}
    except ObjectDoesNotExist:
        context = {'success': False}

    return JsonResponse(context)


@require_POST
def get_artist_social_links(request):
    # if not request.user.is_authenticated():
    #     return JsonResponse({'error':'not authenticated'})
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    customer = Customer.objects.get(customer=user)
    try:
        artist = ArtistDetail.objects.get(customer=customer)
        social_links = SocialLink.objects.filter(artist=artist)
        data = []
        for social_link in social_links:
            data.append(social_link.url)
        context = {'social_links': data}

    except ObjectDoesNotExist:
        context = {'social_links': []}

    return JsonResponse(context)


@require_POST
def set_artist_social_links(request):
    # if not request.user.is_authenticated():
    #     return JsonResponse({'error':'not authenticated'})
    url = request.POST.get('url', None)
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    customer = Customer.objects.get(customer=user)
    try:
        artist = ArtistDetail.objects.get(customer=customer)
        if url:
            SocialLink.objects.create(artist=artist, url=url)
            context = {'success': True}
        else:
            context = {'error': 'url Mandetory'}

    except ObjectDoesNotExist:
        context = {'error': 'Artist Details Not Found'}

    return JsonResponse(context)


@require_POST
def get_artist_products(request):
    user_name = request.POST.get('user_name', None)
    if user_name:
        try:
            user = User.objects.get(username=user_name)
            customer = Customer.objects.get(customer=user)
            artist = ArtistDetail.objects.get(customer=customer)
            designs = ArtistDesign.objects.filter(customer=artist)
            products = []
            for d in designs:
                product_map = ProductArtistDesignMap.objects.filter(
                    artist_design=d)
                for p in product_map:
                    products.append(p.product)

            product_detail_list = product_details(set(products))
            context = {'product_detail_list': product_detail_list}

        except ObjectDoesNotExist:
            context = {'error': 'Artist Details Not Found'}
    else:
        context = {'error': 'user_name mandetory'}
    return JsonResponse(context)


@require_POST
def artist_signup(request):
    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    mobile = request.POST.get('mobile', None)
    artist_type = request.POST.get('artist_type', None)
    if not mobile:
        return JsonResponse({'success': False, 'msg': 'mobile is Mandatory'})

    if not password:
        return JsonResponse({'success': False, 'msg': 'password is Mandatory'})

    if User.objects.filter(username=mobile).exists():
        return JsonResponse({'success': False, 'msg': 'mobile Number is Already Registered'})

    first_name = name.rsplit(' ', 1)[0]
    try:
        last_name = name.rsplit(' ', 1)[1]
    except IndexError:
        last_name = ""

    if(len(email) <= 30):
        un = email
    else:
        un = mobile

    new_user = User.objects.create(
        email=email, username=un, first_name=first_name, last_name=last_name)
    new_user.set_password(password)
    new_user.save()
    customer_obj = Customer.objects.get(customer=new_user)
    customer_obj.mobile = mobile
    customer_obj.save()
    ArtistDetail.objects.create(customer=customer_obj, artist_type=artist_type)
    user = authenticate(username=new_user.username, password=password)
    login(request, user)
    host = str(request.get_host())
    context = {
        'success': True,
        'msg': 'Artist Registered',
        'redirect_url': "http://" + host + "/artist/home/"
    }
    artist_signup_mail(email, name)
    artist_sigup_sms(mobile, name)
    return JsonResponse(context)


def artist_signup_mail(email, name):
    notification = Notification.objects.get(nid='artist_signup')
    notification.email_to = [email]
    notification.send_email([name, email])


def artist_sigup_sms(mobile, name):
    notification = Notification.objects.get(nid='artist_signup')
    notification.numbers = [mobile]
    notification.send_sms([name, mobile])


@require_POST
def artist_details(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    customer = Customer.objects.get(customer=user)
    if get_object_or_404(ArtistDetail, customer=customer):
        # fetch Details
        first_name = user.first_name
        last_name = user.last_name
        user_photo = customer.user_photo.url
        mobile = customer.mobile
        email = user.email
        context = {'first_name': first_name,
                   'last_name': last_name,
                   'user_photo': user_photo,
                   'mobile': mobile,
                   'email': email}
    else:
        context = {'error': 'user is not an artist'}
    return JsonResponse(context)


@require_POST
def artist_other_details(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    customer = Customer.objects.get(customer=user)
    try:
        artist = ArtistDetail.objects.get(customer=customer)
        about = artist.about
        address = artist.address
        pin_code = artist.pin_code
        city = artist.city
        state = artist.state
        artist_type = artist.artist_type

        context = {'success': True,
                   'about': about,
                   'address': address,
                   'pin_code': pin_code,
                   'city': city,
                   'state': state,
                   'artist_type': artist_type
                   }

    except ObjectDoesNotExist:
        context = {'success': False}

    return JsonResponse(context)


@require_POST
def artist_bank_details(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    customer = Customer.objects.get(customer=user)
    try:
        artist = ArtistDetail.objects.get(customer=customer)
        bank_details = ArtistBankDetail.objects.get(artist=artist)
        account_holder_name = bank_details.account_holder_name
        bank_name = bank_details.bank_name
        branch_name = bank_details.branch_name
        pan = bank_details.pan
        ifsc_code = bank_details.ifsc_code
        account_no = bank_details.account_no
        bank_branch_address = bank_details.bank_branch_address
        account_type = bank_details.account_type

        context = {'success': True,
                   'account_holder_name': account_holder_name,
                   'bank_name': bank_name,
                   'branch_name': branch_name,
                   'pan': pan,
                   'ifsc_code': ifsc_code,
                   'account_no': account_no,
                   'bank_branch_address': bank_branch_address,
                   'account_type': account_type,
                   }

    except ObjectDoesNotExist:
        context = {'success': False}

    return JsonResponse(context)


@require_POST
def artist_other_details_update(request):
    about = request.POST.get('about', None)
    address = request.POST.get('address', None)
    pin_code = request.POST.get('pin_code', None)
    city = request.POST.get('city', None)
    state = request.POST.get('state', None)
    artist_type = request.POST.get('artist_type', None)
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    customer = Customer.objects.get(customer=user)
    try:
        artist = ArtistDetail.objects.get(customer=customer)
        if about and about.strip() != "":
            artist.about = about
        artist.save()

        if address and address.strip() != "":
            artist.address = address
        artist.save()

        if pin_code and pin_code.strip() != "":
            artist.pin_code = pin_code
        artist.save()

        if city and city.strip() != "":
            artist.city = city
        artist.save()

        if state and state.strip() != "":
            artist.state = state
        artist.save()

        if artist_type and artist_type.strip() != "":
            artist.artist_type = artist_type
        artist.save()
        context = {'success': True}

    except ObjectDoesNotExist:
        context = {'success': False}

    return JsonResponse(context)


@require_POST
def artist_bank_details_update(request):
    account_holder_name = request.POST.get('account_holder_name', None)
    ifsc_code = request.POST.get('ifsc_code', None)
    account_no = request.POST.get('account_no', None)
    pan = request.POST.get('pan', None)
    bank_name = request.POST.get('bank_name', None)
    branch_name = request.POST.get('branch_name', None)
    bank_branch_address = request.POST.get('bank_branch_address', None)
    account_type = request.POST.get('account_type', None)
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    customer = Customer.objects.get(customer=user)
    try:
        artist = ArtistDetail.objects.get(customer=customer)
        artist_bank_details = ArtistBankDetail.objects.filter(artist=artist)
        if len(artist_bank_details) == 0:

            if not account_holder_name or account_holder_name.strip() == "":
                return JsonResponse({'success': False})

            if not ifsc_code or len(ifsc_code.strip()) != 11:
                return JsonResponse({'success': False})

            if not account_no or account_no.strip() == "":
                return JsonResponse({'success': False})

            if not pan or pan.strip() == "":
                return JsonResponse({'success': False})

            if not bank_name or bank_name.strip() == "":
                return JsonResponse({'success': False})

            if not branch_name or branch_name.strip() == "":
                return JsonResponse({'success': False})

            if not bank_branch_address or bank_branch_address.strip() == "":
                return JsonResponse({'success': False})

            if not account_type or account_type.strip() == "":
                return JsonResponse({'success': False})
            ArtistBankDetail.objects.create(artist=artist,
                                            account_holder_name=account_holder_name,
                                            bank_name=bank_name,
                                            branch_name=branch_name,
                                            pan=pan,
                                            ifsc_code=ifsc_code,
                                            account_no=account_no,
                                            bank_branch_address=bank_branch_address,
                                            account_type=account_type)
            context = {'success': True}
        else:
            context = {'success': False}
    except ObjectDoesNotExist:
        context = {'success': False}

    return JsonResponse(context)


def get_public_profile(request):
    artistID = request.POST.get('artistID', None)
    artist_obj = ArtistDetail.objects.get(id=artistID)
    dsgn_objs = ArtistDesign.objects.filter(customer=artist_obj)
    designs_url = [i.design.url for i in dsgn_objs]
    products = []
    for d in dsgn_objs:
        product_map = ProductArtistDesignMap.objects.filter(
            artist_design=d)
        for p in product_map:
            products.append(p.product)
        product_detail_list = product_details(set(products))
    context = {
        'name': artist_obj.customer.customer.first_name + " " + artist_obj.customer.customer.last_name,
        'about': artist_obj.about,
        'user_photo': artist_obj.customer.user_photo.url,
        'designs': designs_url,
        'product_detail_list': product_detail_list,
    }
    return JsonResponse(context)


@require_POST
def remove_artist_design(request):
    if not request.user.is_authenticated():
        return JsonResponse({'success': False, 'error': 'not authenticated'})
    design_id = request.POST.get('design_id', None)
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    customer = Customer.objects.get(customer=user)
    try:
        artist = ArtistDetail.objects.get(customer=customer)
        if design_id:
            design = get_object_or_404(
                ArtistDesign, customer=artist, id=design_id, status='PENDING')
            design.delete()
            context = {'success': True}
        else:
            context = {'success': False}

    except ObjectDoesNotExist:
        context = {'success': False, 'error': 'Artist Details Not Found'}
    return JsonResponse(context)


@require_POST
def get_artist_designs_public(request):
    artistID = request.POST.get('artistID', None)
    try:
        artist = ArtistDetail.objects.get(id=artistID)
        first_name = artist.customer.customer.first_name
        last_name = artist.customer.customer.last_name
        user_photo = artist.customer.user_photo.url
        about = artist.about
        data = []
        products = []
        designs = ArtistDesign.objects.filter(customer=artist,status='APPROVED')
        for design in designs:
            product_map = ProductArtistDesignMap.objects.filter(artist_design=design)
            link = ''
            if product_map:
                link = '/product/'+ product_map[0].product.slug + '/' + str(product_map[0].product.id) + '/'
            data.append({'id': design.id, 'title': design.title, 'status': design.status,
                         'comment': design.comment, 'tags': design.tags, 'link': link, 'image': design.get_thumbname_url()})
            for p in product_map:
                products.append(p.product)
        product_detail_list = product_details(set(products))
        context = { 'first_name': first_name,
                    'last_name': last_name, 
                    'user_photo': user_photo, 
                    'about': about, 
                    'designs': data, 
                    'product_detail_list': product_detail_list,
                    "breadcrumb": [{'link': '/', 'value': 'home'},
                      {'link': '/artist/all/', 'value': 'all artists'},
                      {'link': '', 'value': first_name}]}
    except ObjectDoesNotExist:
        context = {'first_name':'',
                    'last_name':'', 
                    'user_photo':'', 
                    'about': '', 
                    'designs': [],
                    'product_detail_list': []}
    return JsonResponse(context)


def all_artists(request):
    artists = ArtistDetail.objects.all()
    artist_data = []
    for artist in artists:
        first_name = artist.customer.customer.first_name
        last_name = artist.customer.customer.last_name
        user_photo = artist.customer.user_photo.url
        email = artist.customer.customer.email
        about = artist.about
        link = '/artist/profile/' + str(artist.id) + '/' + str(artist.slug) + '/'
        arts = ArtistDesign.objects.filter(customer = artist,status = 'APPROVED')
        artist_data.append({'first_name':first_name,
                            'last_name':last_name,
                            'user_photo':user_photo,
                            'no_of_arts':len(arts),
                            'about':about if about else '...' ,
                            'link':link})
    artist_data = sorted(artist_data, key = lambda user: user['no_of_arts'],reverse=True)
    context = {'artist_data':artist_data,
                "breadcrumb": [{'link': '/', 'value': 'home'},
                      {'link': '', 'value': 'all artists'}]}
    return JsonResponse(context)    
