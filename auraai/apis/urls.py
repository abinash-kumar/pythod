from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from auraai.apis import views

urlpatterns = [
    url(r'^tags/search/$', views.search_tags, name='search_tags'),
    url(r'^tags/products/$', views.get_all_products_by_tag_name,
        name='get_all_products_by_tag_name'),
    url(r'^tags/get/tags/$', views.get_tags_of_product, name='get_tags_of_product'),
    url(r'^tags/get/all-banners/$', views.get_all_banners, name='get_all_banners'),
    url(r'^tags/search/product/$', views.search_products_by_tag,
        name='search_products_by_tag'),
    url(r'^tags/banner/get/products/$',
        views.get_products_by_banner, name='get_products_by_banner'),
    url(r'^product/search/$', views.product_search, name='product_search'),
    url(r'^autocomplete/$', views.product_autocomplete,
        name='product_autocomplete'),
    url(r'^refresh-search/$', views.refresh_search_keys, name='refresh_search_keys'),
    url(r'^refresh-search-status/$', views.refresh_search_status,
        name='refresh_search_status'),
    url(r'^magic/search/$', views.magic_fb_search, name='magic_fb_search'),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
