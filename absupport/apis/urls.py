from django.conf.urls import url
from absupport.apis import views

urlpatterns = [
    url(r'bank/ifsc/$', views.bank_ifsc, name='bank_ifsc'),
    url(r'check/payment-modes/$', views.check_payment_modes_pincode,
        name='check_payment_modes_pincode'),
    url(r'check/pincode/$', views.check_pincode,
        name='check_pincode'),
    url(r'add/category/$', views.add_category, name='add_category'),
    url(r'add/category/varient/$', views.add_category_varient, name='add_category_varient'),
    url(r'get/category/$', views.get_category, name='get_category'),
    url(r'get/category/varient/$', views.get_category_varient, name='get_category_varient'),
    url(r'add/product/$', views.add_product, name='add_product'),
    url(r'add/product/varient/$', views.add_product_varient, name='add_product_varient'),
    url(r'get/all/category/varient/$', views.get_all_category_varient, name='get_all_category_varient'),
    url(r'add/product/image/$', views.add_product_image, name='add_product_image'),
    url(r'add/product/tag/$', views.add_product_tag, name='add_product_tag'),
    url(r'^', views.dashboard_new, name="dashboard_new"),
    # url(r'discount/$', views.discount, name='discount'),
    # url(r'add/comboproducts/$', views.comboproducts, name='comboproducts'),


]
