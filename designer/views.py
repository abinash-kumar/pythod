from django.shortcuts import render
from django.shortcuts import get_object_or_404
from designer.models import Designer
from designer .models import DesignerContactDetails

# Create your views here.


def profile(request, slug, id):
    designer_obj = get_object_or_404(Designer, pk=id, slug=slug)
    print designer_obj.awards
    context = {

    }
    return render(request, 'designer/designer_profile.html', context)


def dashboard(request):
    return render(request, 'designer/designer_dashboard.html', {})

# Designers Signup page
# http://www.addictionbazaar.com/designers/signup/<Unique_id>


def signup(request, id=None):
    if id and (DesignerContactDetails.objects.filter(unique_id=id).exists()):
        designer_obj = DesignerContactDetails.objects.get(unique_id=id)
        context = {'name': designer_obj.name, 'email': designer_obj.email}
    else:
        context = {'name': "", 'email': ""}
    return render(request, 'designer/designer_signup.html', context)
