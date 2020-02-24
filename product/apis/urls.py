from django.conf.urls import url, include
from product.apis import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^get-product-detail/$', views.product_details_api,
        name='product_details_api'),
    url(r'^list/(?P<slug>[-\w]+)/(?P<id>[-\d]+)/$',
        views.product_listing_api, name='product_listing'),
    url(r'^similer-products/$', views.similer_product, name='similer_product'),
    url(r'^tshirt/list/$', views.product_listing_api, name='product_listing_api'),
    url(r'^tshirt/add/cart/$', views.add_cart, name='add_cart_tshirt'),
    url(r'^tshirt/varient/byid/$', views.tshirt_varients, name='tshirt_varients'),
    url(r'^add-cart/$', views.add_cart, name='add_cart'),
    url(r'^tshirt/varient/id-price/$',
        views.tshirt_varient_price, name='tshirt_varient_price'),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
