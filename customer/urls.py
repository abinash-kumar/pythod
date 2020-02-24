from django.conf.urls import include, url
from customer import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^orders/$', views.orders, name="orders"),
    url(r'^pickedbyme/$', views.picked_items, name="picked_items"),
    url(r'^apis/', include('customer.apis.urls')),
    url(r'^update/profile-pic/$', views.customer_image_upload, name="customer_image_upload"),
    url(r'^reset-password/verify/(?P<link>[\w-]+)/$', views.verify_reset_password, name="verify_reset_password"),
    url(r'^reset-password/submit/$', views.submit_reset_password, name="submit_reset_password"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
