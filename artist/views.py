from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from artist.forms import ArtistForm
from artist.models import ArtistDetail
from django.contrib.auth.models import User
from customer.models import Customer
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from abutils.utils import create_products

# Create your views here.


def upload_design(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    customer = Customer.objects.get(customer=user)
    try:
        artist = ArtistDetail.objects.get(customer=customer)
        form = ArtistForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            # ArtistDesign.objects.create(comment=request.POST.get('comment',None))
            instance = form.save(commit=False)
            instance.customer = artist
            instance.status = 'PENDING'
            instance.save()
            instance.create_thumbnail()
            create_products(instance.design.path, instance.id)
            context = {'success': True}
        else:
            context = {'success': False}
    except ObjectDoesNotExist:
        context = {'success': False}
    return JsonResponse(context)


def artist_home(request):
    # if user is not artist redirect to artist login...
    if request.user.is_authenticated() and get_object_or_404(ArtistDetail, customer=Customer.objects.get(customer=request.user)):
        context = {}
        return render(request, 'artist/artist_home.html', context)
    else:
        return HttpResponseRedirect("/login/?next=/artist/home/")


def artist_products(request, slug, artist_id):
    context = {}
    return render(request, 'artist/artist_products.html', context)


def artist_signup(request, id=None):
    return render(request, 'artist/artist_signup.html', {})


def artist_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    new_user = False
    if request.GET.get('new', False):
        new_user = True
        print "this is a new user hahahaha"
    context = {
        "new_user": new_user
    }
    return render(request, "artist/artist_login.html", context)


def artist_profile_page(request, artist_id, slug):
    artist_obj = ArtistDetail.objects.get(id=artist_id)
    name = artist_obj.customer.customer.first_name + " " + \
        artist_obj.customer.customer.last_name
    context = {
        'title': name + "'s Profile - Artist at AddictionBazaar.com",
        'image': artist_obj.customer.user_photo.url,
        'description': "Checkout " + name + "'s Arts and Products at AddictionBazaar.com",
        'keywords': "",
    }
    return render(request, 'artist/artist_profile.html', context)


def all_artists(request):
    context = {
        'title': "All Artists - Addiction Bazaar",
        'description': "Our Legend Artists, And their Designs",
        'keywords': "",
        'image': "https://www.addictionbazaar.com/uploads/artist_design/8800447876/th_2017-10-11033528217715.png?s=5150125",
    }
    return render(request, 'artist/all_artists.html', context)
