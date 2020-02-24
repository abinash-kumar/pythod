from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as django_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap


from codeab.site_maps import ProductDetailSitemap, ArtistDetailSitemap, TshirtCategoryVarientSitemap, HoodieCategoryVarientSitemap, TagSitemap, CfblogSitemap, AllSiteMap

from myhome import views
from product import views as product_view

sitemaps = {
    'artist': ArtistDetailSitemap(),
    'tshirt': TshirtCategoryVarientSitemap(),
    # 'hoodies': HoodieCategoryVarientSitemap(),
    # 'tags': TagSitemap(),
    'cfblog': CfblogSitemap(),
}

# sitemaps = {
#     'tshirt': 
#     'womens-tshirt':
#     'men-half-sleeves-round-neck-tshirt': 
#     'women-half-sleeves-round-neck-tshirt':
#     'croptop':
# }


sitemaps_index = {
    'all' : AllSiteMap(),
}


# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^abset/', include(admin.site.urls)),
    url(r'^cfblog/', include('cfblog.urls')),
    url(r'^designers/', include('designer.urls')),
    url(r'^designerwear/$', views.home_designer_wear, name="home_designer_wear"),
    url(r'^my-cart/$', views.my_cart, name="my_cart"),
    url(r'^apis/', include('codeab.apis.urls')),
    url(r'^checkout/$', views.checkout, name="checkout"),
    url(r'^apis/review-order/$', views.review_order_api, name="review_order_api"),
    url(r'^blog/', include('blog.urls')),
    url(r'^user/', include('customer.urls')),
    url(r'^product/', include('product.urls')),
    url(r'^seller/', include('seller.urls')),
    # url(r'^tshirt/$', include('product.urls')),
    url(r'^mens-clothing/$', product_view.mens_products),
    url(r'^womens-clothing/$', product_view.women_products),
    url(r'^couple-tshirts/$', product_view.couple_products),
    url(r'^tshirt/$', product_view.tshirt, name="tshirt-list"),
    url(r'^ab/', include('absupport.urls')),
    url(r'^ab/expense/', include('expense.urls')),
    url(r'^aura/', include('auraai.urls')),
    url(r'^artist/', include('artist.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login/$', views.login_user, name="login_user"),
    url(r'^loginuser/$', views.login_authentication, name="login_authentication"),
    url(r'^register/$', views.register_user, name="register_user"),
    url(r'^registeruser/$', views.registeruser, name="registeruser"),
    url(r'^logout/$', django_views.logout, {'next_page': '/'}),
    url(r'^process-payment/(?P<transaction_id>[\w-]+)/$',
        views.process_payment, name="process_payment"),
    url(r'^process-cod/(?P<transaction_id>[\w-]+)/$',
        views.process_cod, name="process_cod"),
    url(r'^pay-success/$', views.success, name='success'),
    url(r'^failure/$', views.failure, name='failure'),
    url(r'^cancel/$', views.cancel, name='cancel'),
    url(r'^process-offline/$', views.process_offline, name='offline'),
    # site-map url
    # url(r'^sitemap_index\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # Paytm URL
    url(r'^paytm/payment/(?P<transaction_id>[-\w]+)/$',
        views.paytm_payment, name='paytm_payment'),
    url(r'^paytm/response/', views.paytm_response, name='paytm_response'),
    url(r'^paytm/status/(?P<transaction_id>[-\w]+)/$',
        views.paytm_status, name='paytm_status'),

    # Landing pages
    url(r'^update_sheet/?$', views.update_sheet, name='update_sheet'),
    url(r'^products/(?P<slug>[\w-]+)/$', product_view.products, name="products"),
    url(r'^sitemap_index\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps_index,'template_name': 'index_sitemap.xml'}),
    url(r'^product_sitemap\.xml$', views.render_sitemap, name='render_sitemap'),
    url(r'^(?P<sitemap_name>[-\w]+)_(?P<sitemap_param>[-\w]+)_sitemap\.xml$', views.render_sitemap, name='render_sitemap'),
    # url(r'^product_2_sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap[2],'template_name': 'sitemap.xml'}),
    # url(r'^product_3_sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap[3],'template_name': 'sitemap.xml'}),
    # url(r'^product_4_sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap[4],'template_name': 'sitemap.xml'}),
    # url(r'^product_5_sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap[5],'template_name': 'sitemap.xml'}),
    # url(r'^product_6_sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap[6],'template_name': 'sitemap.xml'}),
    # url(r'^product_7_sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap[7],'template_name': 'sitemap.xml'}),
    # url(r'^product_8_sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemap[8],'template_name': 'sitemap.xml'}),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# urlpatterns += [ url(r'^obtain-auth-token/$', obtain_auth_token) ]
