from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from seller import views as views
from django.contrib.auth import views as django_auth_views
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import login

from seller.views import BasicPlusVersionCreateView

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/myhome/')


urlpatterns = [
    url(r'^$', views.register, name="register_seller"),
    url(r'^register/$', views.register, name="register_seller"),
    url(r'^myhome/$', views.dashboard, name="dashboard"),
    url(r'^openshop/$', views.seller_form, name="register_form"),
    url(r'^thanks/$', views.seller_thanku_for_register,
        name="seller_thanku_for_register"),
    url(r'^setpassword/$', views.set_password, name="set_password"),
    url(r'^createseller/$', views.create_seller, name='create_seller'),
    url(r'^sendotp/$', views.send_otp, name='send_otp'),
    url(r'^verifyotp/$', views.verify_otp, name='verify_otp'),
    url(r'^login/$', login_forbidden(login),
        {'template_name': 'seller/seller_login.html'}, 'seller_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/login'}),
    url(r'^add-product/$', views.add_product, name="add_product"),
    url(r'^all-product/$', views.all_product, name="all_product"),
    url(r'^add-category/$', views.add_category, name="add_category"),
    url(r'^add-product-post/$', views.add_product_post, name="add_product"),
    url(r'^add-product-details/$', views.add_product_details,
        name="add_product_details"),
    url(r'^get-child-category/$', views.get_child_category,
        name="get_child_category"),
    url(r'^check-existing-mobile/$', views.check_existing_mobile,
        name="check_existing_mobile"),
    url(r'^check-existing-email/$', views.check_existing_email,
        name="check_existing_email"),
    url(r'^upload-image/$', BasicPlusVersionCreateView.as_view(),
        name='upload-basic-plus'),
    url(r'^update_category/$', views.update_category, name='update_category'),
    url(r'^apis/', include('seller.apis.urls')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
