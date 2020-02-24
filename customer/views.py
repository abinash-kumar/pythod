import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from customer.models import Customer, CustomerEmailVerify
from customer.forms import CustomerImageForm



# Create your views here.
def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    user = User.objects.get(username=request.user.username)
    customer = Customer.objects.get(customer=user)
    tab = request.GET.get('tab', 0)
    if tab == 'orders':
        tab = 1
    elif tab == 'picked':
        tab = 2

    context = {
        "customer": customer,
        'tab': tab,
    }
    return render(request, "user_profile.html", context)


def orders(request):
    context = {

    }
    return render(request, "orders.html", context)


def picked_items(request):
    context = {

    }
    return render(request, "orders.html", context)


@require_POST
def get_user_details(request):
    context = {
    }
    return JsonResponse(context)


def customer_image_upload(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    customer = Customer.objects.get(customer=user)
    form = CustomerImageForm(request.POST or None, request.FILES or None, instance=customer)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        context = {'success': True}
    else:
        context = {'success': False}
    return JsonResponse(context)


def verify_reset_password(request, link):
    expiry_days = 3
    try:
        verify_obj = CustomerEmailVerify.objects.get(link=link)
        if (not verify_obj.is_clicked) and (((datetime.datetime.now().date() - verify_obj.created_on).days) < expiry_days ):
            return render(request, "password_reset.html", {'success':True, 'link':link})
        else:
            return render(request, "password_reset.html", {'success':False})
    except ObjectDoesNotExist:
        return render(request, "password_reset.html", {'success':False})

def submit_reset_password(request):
    expiry_days = 3
    link = request.POST.get('link', None)
    password = request.POST.get('password', None)
    if link:
        if password and len(password) > 1:
            try:
                verify_obj = CustomerEmailVerify.objects.get(link=link)
                if (not verify_obj.is_clicked) and (((datetime.datetime.now().date() - verify_obj.created_on).days) < expiry_days ):
                    user = verify_obj.customer.customer
                    user.set_password(password)
                    verify_obj.is_clicked = True
                    verify_obj.save()
                    user.save()
                    return render(request, "password_reset_submit.html", {'success':True})
                else:
                    return render(request, "password_reset_submit.html", {'success':False})  
            except ObjectDoesNotExist:
                return render(request, "password_reset_submit.html", {'success':False})

    return render(request, "password_reset_submit.html", {'success':False})