from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from artist.apis import views

urlpatterns = [
    url(r'^artist-signup/$', views.artist_signup, name="artist_signup"),
    url(r'^artist/details/$', views.artist_details, name="artist_details"),
    url(r'^get/designs/$', views.get_artist_designs, name='get_artist_designs'),
    url(r'^get/products/$', views.get_artist_products, name='get_artist_products'),
    url(r'^get/social-links/$', views.get_artist_social_links, name='get_artist_social_links'),
    url(r'^set/social-links/$', views.set_artist_social_links, name='set_artist_social_links'),
    url(r'^get/other/details/$', views.artist_other_details, name='artist_other_details'),
    url(r'^set/other/details/$', views.artist_other_details_update, name='artist_other_details_update'),
    url(r'^get/bank/details/$', views.artist_bank_details, name='artist_bank_details'),
    url(r'^set/bank/details/$', views.artist_bank_details_update, name='artist_bank_details_update'),
    url(r'^get-profile/$', views.get_public_profile, name='get_public_profile'),
    url(r'^remove/design/$', views.remove_artist_design, name='remove_artist_design'),
    url(r'^edit/design/$', views.edit_artist_designs, name='edit_artist_designs'),
    url(r'^get/designs/public$', views.get_artist_designs_public, name='get_artist_designs_public'),
     url(r'^all-artists/$', views.all_artists, name="all_artists"),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
