from django.shortcuts import render
from django.contrib.sites.models import Site


# Create your views here.

def home(request):

    domain = Site.objects.get_current().domain
    context = {
        'view':'myhome',
        'domain':request.subdomain,
        'mydomain': domain
    }
    return render(request,"index2.html",context)
