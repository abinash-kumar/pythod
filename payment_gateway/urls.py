""" URLs setting for payment gateways """
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<gateway>\w+)/response/$',
        views.response,
        name='pg-response'),

    url(r'^(?P<gateway>\w+)/s2sresponse/$',
        views.s2s_response,
        name='pg-s2s-response'),
]
