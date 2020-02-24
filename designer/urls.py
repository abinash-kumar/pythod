from django.conf.urls import include, url
from designer import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^profile/(?P<slug>[-\w]+)/(?P<id>[-\d]+)$', views.profile, name="designer_profile"),
    url(r'^apis/', include('designer.apis.urls')),
    url(r'^signup/(?P<id>[\w-]+)$', views.signup, name="designer_signup"),
    url(r'^signup/?$', views.signup, name="designer_signup"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
