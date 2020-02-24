from django.conf.urls import *
from blog import views


urlpatterns = [
    url(r'^(?P<slug>[-\w]+)$', views.view_post, name='blog_post_detail'),
    url(r'^$', views.view_all, name='blog_post_all'),
    url(r'archived/(?P<slug>.*)$', views.view_post_archived,
        name='blog_post_archived'),
    url(r'^doc/(?P<slug>[-\w]+)$', views.view_imp_doc, name='view_imp_doc')
]
