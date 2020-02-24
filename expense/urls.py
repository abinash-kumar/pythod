from django.conf.urls import url

from . import views

app_name = 'expencemgmt'
urlpatterns = [
    # ex: /expence/
    url(r'^$', views.index, name='index'),
]