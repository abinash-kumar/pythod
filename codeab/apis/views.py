from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from myhome.models import SliderImages


@require_POST
def get_slider_image(request):
    slider_img_obj = SliderImages.objects.filter(active=True).order_by('display_priority')
    slider_list = []
    for obj in slider_img_obj:
        slider = {}
        slider['image'] = obj.image.url
        slider['image_mobile'] = obj.image_mobile.url
        slider['title'] = obj.title
        slider['description'] = obj.description
        slider['url'] = obj.url
        slider_list.append(slider)
    active_slider = slider_list[0]
    del slider_list[0]
    return JsonResponse({'success': True, 'active_slider': active_slider, 'slider_list': slider_list})


@require_POST
def notification(request):
    context = {
        'success': False,
        'shortMessage': 'Use code SIGNUP100 and earn Rs. 100'
    }
    return JsonResponse(context)
