from django.conf.urls import url
from customer.apis import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^get-user-details/$', views.get_user_details, name="get_user_details"),
    url(r'^send-otp/$', views.send_otp, name="send_otp"),
    url(r'^verify-otp/$', views.verify_otp, name="verify_otp"),
    url(r'^wallet/$', views.get_wallet_data, name="get_wallet_data"),
    url(r'^redeem-coupon/$', views.redeem_coupon, name="redeem_coupon"),
    url(r'^add-new-address/$', views.add_new_address, name="add_new_address"),
    url(r'^signup-user/$', views.sign_up_user, name="sign_up_user"),
    url(r'^signin-user/$', views.sign_in_user, name="sign_in_user"),
    url(r'^check-mobile/$', views.check_mobile, name="check_mobile"),
    url(r'^send-email/$', views.send_email_verification, name="send_email_verification"),
    url(r'^verify/email/(?P<link>[\w-]+)/$', views.verify_email_verification, name="verify_email_verification"),
    url(r'^verify-emailexistence/$', views.verify_email_existence, name="verify_email_existence"),
    url(r'^customer/details/$', views.customer_details, name="customer_details"),
    url(r'^customer/details/save/$', views.edit_customer_details, name="edit_customer_details"),
    url(r'^reset-password/$', views.send_email_for_password_reset, name="send_email_for_password_reset"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
