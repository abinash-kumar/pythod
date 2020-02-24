from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from artist import views

urlpatterns = [
    url(r'^apis/', include('artist.apis.urls')),
    url(r'^upload/design/', views.upload_design, name='upload_design'),
    url(r'^home/$', views.artist_home, name='artist_home'),
    url(r'^signup/?$', views.artist_signup, name="artist_signup"),
    url(r'^login/?$', views.artist_login, name="artist_login"),
    url(r'^products/(?P<slug>[-\w]+)/(?P<artist_id>[-\d]+)/$',
        views.artist_products, name='artist_products'),
    url(r'^profile/(?P<artist_id>[-\d]+)/(?P<slug>[-\w]+)/$',
        views.artist_profile_page, name='artist_profile_page'),
    url(r'^all/', views.all_artists, name='all_artists'),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
