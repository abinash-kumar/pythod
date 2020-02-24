from django.conf.urls import url
from seller.apis import views

urlpatterns = [
    url(r'sellers/$', views.get_all_sellers, name='get_all_sellers'),
]
