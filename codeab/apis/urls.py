from django.conf.urls import url
from codeab.apis import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^get-slider-image/$', views.get_slider_image, name="get_slider_image"),
    url(r'^notification/$', views.notification, name="notification"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
