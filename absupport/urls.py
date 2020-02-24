from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from absupport import views

urlpatterns = [
    # url(r'/$', views.dashboard_new, name='dashboard_new'),
    # url(r'^$', views.dashboard_new, name="dashboard_new"),
    url(r'^apis/', include('absupport.apis.urls')),
    url(r'dashboard/$', views.dashboard, name='dashboard'),
    url(r'artists/$', views.artist_stats, name='artist_stats'),
    url(r'alert/$', views.alert, name='alert'),
    url(r'clear-cache/$', views.clear_cache, name='clear_cache'),
    url(r'product/invalid/$', views.list_products_without_varients,
        name='list_products_without_varients'),
    url(r'product/update-varient/(?P<id>[-\d]+)/$',
        views.update_product_varient, name='update_product_varient'),
    url(r'product/submit-price-quantity/$', views.update_price_quantity_generic,
        name='update_price_quantity_generic'),
    url(r'product/submit-varient-generic/$', views.submit_product_varient_generic,
        name='submit_product_varient_generic'),

    url(r'product/submit-art-product/$',
        views.submit_art_product, name='submit_art_product'),
    url(r'product/create/(?P<id>[-\d]+)/$',
        views.artist_design_list, name='artist_design_list'),
    url(r'product/make/(?P<slug>[-\w]+)/(?P<id>[-\w]+)/$',
        views.make_product_from_design, name='make_product_from_design'),
    url(r'login-as/$', views.login_as, name='login_as'),
    url(r'send-email/$', views.send_email, name='send_email'),
    url(r'initiate-email-sending/(?P<id>[-\d]+)/$',
        views.initiate_email_sending, name='initiate_email_sending'),
    url(r'initiate-sms-sending/(?P<id>[-\d]+)/$',
        views.initiate_sms_sending, name='initiate_sms_sending'),
    url(r'address/pickup/(?P<id>[\w-]+)/$',
        views.seller_pickup_address_reg, name='seller_pickup_address_reg'),
    url(r'address/pickup/$', views.seller_pickup_address_reg,
        name='seller_pickup_address_reg_no_arg'),
    url(r'seller-pickup-address-update/$', views.seller_pickup_address_update,
        name='seller_pickup_address_update'),
    url(r'^orders/$', views.orders, name='orders'),
    url(r'orders/(?P<id>[-\d]+)/$', views.order_detail, name='order_detail'),
    url(r'order-confirm/$', views.order_confirm, name='order_confirm'),
    url(r'orders-tranction/$', views.order_transactions, name='order_transactions'),
    url(r'refresh-offer/$', views.refresh_offers, name='refresh_offers'),
    url(r'product-image-map/$', views.product_image_mapping,
        name='product_image_mapping'),
    url(r'^test/?$', views.test_template, name='test_template'),
    url(r'^refresh-products/?$', views.refresh_products, name='refresh_products'),
    url(r'^refresh-products-status/?$', views.refresh_products_status,
        name='refresh_products_status'),
    url(r'^refresh-products-page/?$', views.refresh_products_page,
        name='refresh_products_page'),
    url(r'^delete-cache-key/?$', views.delete_cache_key,
        name='delete_cache_key'),
    url(r'^create-combo-page/?$', views.create_combo_page,
        name='create_combo_page'),
    url(r'^create-combo-product/?$', views.create_combo_product,
        name='create_combo_product'),
    url(r'^refresh-artist-design/?$', views.refresh_artist_design,
        name='refresh_artist_design'),
    url(r'^Campaigns-and-Coupons/?$', views.Campaigns_and_Coupons,
        name='Campaigns_and_Coupons'),
    url(r'^offline-orders/$', views.offline_orders, name='offline_orders'),
    url(r'^offline-orders/details/$', views.offline_orders_detail, name='offline-orders/details/'),
    url(r'^offline-orders/submit/$', views.offline_orders_submit, name='offline-orders/submit/'),


    # /ab/offline-orders/details/ make this url link to view - offline_orders_detail

    # /ab/offline-orders/submit/ make this and link to view - offline_orders_submit

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
