from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from designer.models import Designer, DesignerSliderImages, DesignercollageImages
from product.models import Product, ProductImage, Discount
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from designer .models import DesignerContactDetails
from seller .models import Seller, SellerVatDetails, SellerOnboardingHistory
from django.contrib.auth.models import User
from customer.models import Customer


@require_POST
def get_all_designers_detail(request):
    host_name = 'https://' + \
        request.get_host() if 'http' in request.get_host() else 'http://' + request.get_host()
    designers = request.POST.get('designers', None)
    product_detail_list = []
    collage_list = []
    if designers == 'all':
        all_designer_obj = Designer.objects.filter(designer__is_active=True)
    elif designers:
        all_designer_obj = Designer.objects.filter(
            designer__is_active=True, id=designers)
        designer_obj = all_designer_obj[0]

        # Designer Products
        seller_obj = designer_obj.designer
        all_prod_obj = Product.objects.filter(seller=seller_obj, active=True)
        for obj in all_prod_obj:
            product_detail = {}
            product_detail['name'] = obj.name

            product_image_obj = ProductImage.objects.filter(
                product=obj).order_by('display_priority')[:1]
            product_detail['product_photo_url'] = [
                i.get_thumbname_url() for i in product_image_obj]

            product_detail['slug'] = obj.slug
            product_detail['price'] = int(obj.price)
            product_detail['id'] = obj.id

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

        # Designer Collage Images
        collage_img_obj = DesignercollageImages.objects.filter(
            designer=designer_obj, active=True).order_by('display_priority')
        for obj in collage_img_obj:
            collage = {}
            collage['image'] = obj.image.url
            collage['title'] = obj.title
            collage['description'] = obj.description
            collage_list.append(collage)

    all_designer_list = []
    for obj in all_designer_obj:
        designer = {}
        designer['name'] = obj.designer.seller.first_name + \
            " " + obj.designer.seller.last_name
        designer['profile_link'] = host_name + \
            "/designers/profile/" + obj.slug + '/' + str(obj.pk)
        designer['gender'] = obj.designer.gender
        designer['awards'] = obj.awards
        designer['education'] = obj.education
        designer['about'] = obj.about
        designer['experience'] = obj.get_work_experience()
        designer['specialization'] = obj.specialization
        designer['is_premium'] = obj.is_premium
        designer['user_photo'] = obj.user_photo.url
        all_designer_list.append(designer)

    premium_desinger = [i for i in all_designer_list if i['is_premium']]
    other_designer = [i for i in all_designer_list if not i['is_premium']]

    context = {
        'premium_desinger': premium_desinger,
        'other_designer': other_designer,
        "product_detail_list": product_detail_list,
        'collage_list': collage_list,
    }
    return JsonResponse(context)


def get_slider_image(request, id):
    designer_obj = Designer.objects.get(id=id)
    slider_img_obj = DesignerSliderImages.objects.filter(
        designer=designer_obj, active=True).order_by('display_priority')
    slider_list = []
    for obj in slider_img_obj:
        slider = {}
        slider['image'] = obj.image.url
        slider['title'] = obj.title
        slider['description'] = obj.description
        slider_list.append(slider)
    active_slider = slider_list[0]
    del slider_list[0]

    context = {
        'success': True,
        'active_slider': active_slider,
        'slider_list': slider_list,
    }
    return JsonResponse(context)

# Designer Signup API mobile
# http://127.0.0.1:8000/designers/apis/signup-mob-api/


@require_POST
def designer_response_api(request):
    dname = request.POST.get('name', None)
    dmobile = request.POST.get('mobile', None)
    duuid = request.POST.get('uuid', None)
    if(not dmobile or (dmobile == "")):
        return JsonResponse({'msg': 'Mobile Is Mandatory'})

    if(DesignerContactDetails.objects.filter(unique_id=duuid).exists()):
        designer_obj = DesignerContactDetails.objects.get(unique_id=duuid)
        designer_obj.status = "RESPONDED"
        # checking mobile number is presece if not then adding
        if(',' in dmobile):
            return JsonResponse({'msg': 'Invalid Mobile'})
        j = 0
        if(dmobile in designer_obj.mobile):
            j = 1

        if j == 0:
            if(designer_obj.mobile.strip() == ""):
                designer_obj.mobile = dmobile
            else:
                designer_obj.mobile = designer_obj.mobile + ' ,' + dmobile

        designer_obj.save()
        context = {'msg': 'Data Updated'}

    else:
        designer_obj = DesignerContactDetails(name=dname, mobile=dmobile)
        designer_obj.save()
        context = {'msg': 'Data Added'}
    return JsonResponse(context)


@require_POST
def designer_signup_api(request):

    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    mobile = request.POST.get('mobile', None)
    pincode = request.POST.get('pincode', None)
    brand = request.POST.get('brand', None)
    if not mobile:
        return JsonResponse({'success': False, 'msg': 'Mobile is Mandatory'})

    try:
        int(mobile)
    except ValueError:
        return JsonResponse({'success': False, "msg": "invalid mobile"})

    if(len(mobile) != 0):
        if(Customer.objects.filter(mobile=mobile).exists()):
            return JsonResponse({'success': False, "msg": "mobile number already exists"})
        if(User.objects.filter(username=mobile).exists()):
            return JsonResponse({'success': False, "msg": "mobile number already exists"})

    if not password:
        return JsonResponse({'success': False, 'msg': 'Password is Mandatory'})

    if not email:
        return JsonResponse({'success': False, 'msg': 'Email is Mandatory'})

    if(len(email) != 0):
        if(User.objects.filter(email=email).exists()):
            return JsonResponse({'success': False, "msg": "email already exists"})

    try:
        int(pincode)
    except ValueError, TypeError:
        return JsonResponse({'success': False, 'msg': 'Invalid PinCode'})

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

    seller_obj = Seller.objects.create(
        seller=new_user, mobile=mobile, shop_pin_code=pincode, pickup_pin_code=pincode)
    SellerOnboardingHistory.objects.create(
        seller=seller_obj, status="REGISTERED")

    if brand:
        SellerVatDetails.objects.create(seller=seller_obj, company_name=brand)

    designer_obj = Designer(designer=seller_obj)
    designer_obj.save()

    context = {'success': True, 'msg': 'Designer Registered',
               'redirect_url': "https://www.addictionbazaar.com/designers/dashboard/"}
    return JsonResponse(context)
