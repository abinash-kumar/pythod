from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from product import views

urlpatterns = [
    url(r'^apis/', include('product.apis.urls')),
    url(r'^$', views.products, name='products'),
    url(r'^buy/(?P<category>[-\w]+)/(?P<varient>[-\w]+)/?$',
        views.buy_varient_wise, name='buy_varient_wise'),

    url(r'^(?P<slug>[-\w]+)/(?P<id>[-\d]+)/?$',
        views.product_details, name='product_details'),

    url(r'^tag/(?P<slug>[-\w]+)/$',
        views.sub_category_listing, name='sub_category_listing'),

    url(r'^list/customization/379$',
        views.cust, name='cust'),

    url(r'^list/(?P<slug>[-\w]+)/(?P<id>[-\d]+)/?$',
        views.product_listing, name='product_listing'),

    url(r'^delete-cart/?$',
        views.delete_cart, name='delete_cart'),

    url(r'^update-cart-count/?$',
        views.update_cart_count, name='update_cart_count'),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
