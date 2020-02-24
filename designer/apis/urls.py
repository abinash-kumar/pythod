from django.conf.urls import url
from designer.apis import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^get-all-designers/$', views.get_all_designers_detail, name="get_all_designers_detail"),
    url(r'^slider-image/(?P<id>[-\d]+)/$', views.get_slider_image, name="get_slider_image"),
    url(r'^signup-mob-api/$', views.designer_response_api, name="designer_response_api"),
    url(r'^designer-signup-api/$', views.designer_signup_api, name="designer_signup_api"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
