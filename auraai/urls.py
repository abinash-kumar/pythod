from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from auraai import views

urlpatterns = [
    url(r'^apis/', include('auraai.apis.urls')),
    url(r'^fb/request/', views.get_fb_data, name='get_fb_data'),
    url(r'^fb/request2/', views.get_fb_data2, name='get_fb_data2'),
    url(r'^google/', views.google_sign_in, name='google_sign_in'),
    url(r'^tag/products/?$', views.product_list, name='product_list'),
    url(r'^tag/manage/(?P<id>[-\d]+)/$',
        views.manage_tags, name='manage_tags'),
    url(r'^product/search/?$', views.product_tag_search, name='product_tag_search'),
    url(r'^magic/search/?$', views.fb_magic_search, name='fb_magic_search'),
    url(r'^refresh-search-page/$', views.refresh_search_page,
        name='refresh_search_page'),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
