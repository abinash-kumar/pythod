from django.contrib.sitemaps import Sitemap
from product.models import Product, CategoryVarient, Category, ProductVarientList, ProductImage
from artist.models import ArtistDetail
from auraai.models import Tag
from cfblog.models import Content
from redisearch import Client
import itertools
import datetime
from product.views import get_product_detail_page_title

def get_image(protocol, domain, item):
    all_product_images = ProductImage.objects.filter(product=item)
    images_list = []
    for img in all_product_images:
        images_list.append({'image_url': "%s://%s%s" % (protocol, domain, img.product_photo.url), 'image_name': get_product_detail_page_title(item)})
    return images_list



class ProductDetailSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6
    lastmod = ''

    def __init__(self, start_from, no_of_products):
        self.start_from = start_from
        self.no_of_products = no_of_products

    def items(self):
        return Product.objects.filter(active=True)[self.start_from: self.no_of_products]

    def __get(self, name, obj, default=None):
        try:
          attr = getattr(self, name)
        except AttributeError:
          return default
        if callable(attr):
          return attr(obj)
        return attr

    def get_urls(self, page=1, site=None, protocol=None):
        # Determine protocol
        if self.protocol is not None:
          protocol = self.protocol
        if protocol is None:
          protocol = 'http'

        # Determine domain
        if site is None:
          if Site._meta.installed:
              try:
                  site = Site.objects.get_current()
              except Site.DoesNotExist:
                  pass
          if site is None:
              raise ImproperlyConfigured("To use sitemaps, either enable the sites framework or pass a Site/RequestSite object in your view.")
        domain = site.domain

        urls = []
        for item in self.items():
          loc = "%s://%s%s" % (protocol, domain, item.get_absolute_url())
          priority = self.__get('priority', item, None)
          url_info = {
              'item':       item,
              'location':   loc,
              'lastmod':    item.last_modified,
              'changefreq': self.__get('changefreq', item, None),
              'priority':   str(priority is not None and priority or ''),
              'images'   :   get_image(protocol, domain, item), # changed here
          }
          urls.append(url_info)
        return urls


class ArtistDetailSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ArtistDetail.objects.all()

    def location(self, obj):
        return "/artist/profile/" + str(obj.id) + "/" + str(obj.slug) + "/"


class TshirtCategoryVarientSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        category_varients = CategoryVarient.objects.all()
        category_tshirt = Category.objects.get(slug='tshirt')
        category_varient_tshirt_gender = list(category_varients.filter(
            category=category_tshirt, varient_type='GENDER'))
        category_varient_tshirt_colors = list(category_varients.filter(
            category=category_tshirt, varient_type='COLOR')) + [None]
        category_varient_tshirt_sleeves = list(category_varients.filter(
            category=category_tshirt, varient_type='SLEEVES')) + [None]
        category_varient_tshirt_fitting = list(category_varients.filter(
            category=category_tshirt, varient_type='FITTING')) + [None]
        category_varient_tshirt_neck = list(category_varients.filter(
            category=category_tshirt, varient_type='NECK')) + [None]
        category_varient_tshirt_size = list(category_varients.filter(
            category=category_tshirt, varient_type='SIZE')) + [None]
        category_varient_tshirt_fabric = list(category_varients.filter(
            category=category_tshirt, varient_type='FABRIC')) + [None]
        all_combinations = dict_maker(category_varient_tshirt_fabric,
                                      dict_maker(category_varient_tshirt_size,
                                                 dict_maker(category_varient_tshirt_neck, dict_maker(category_varient_tshirt_fitting,
                                                                                                     dict_maker(category_varient_tshirt_sleeves,
                                                                                                                dict_maker(category_varient_tshirt_colors,
                                                                                                                           dict_maker(category_varient_tshirt_gender)))))))
        return all_combinations

    def location(self, obj):
        if obj['varients']:
            category = str(obj['varients'][0].category.slug)
            varients = []
            for v in obj['varients']:
                temp = ('-' + str(v.varient_type)
                        ) if v.varient_type == 'SIZE' or v.varient_type == 'COLOR' else ''
                varients.append(str(v.name if v.varient_type ==
                                    'GENDER' else v.value).replace(' ', '--') + temp)
            return ('/products/' + '-'.join(varients) + '-' + category).lower()
        else:
            return '/'


class HoodieCategoryVarientSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        category_varients = CategoryVarient.objects.all()
        category_hoodie = Category.objects.get(slug='hoodie')
        category_varient_hoodie_colors = list(category_varients.filter(
            category=category_hoodie, varient_type='COLOR')) + [None]
        category_varient_hoodie_size = list(category_varients.filter(
            category=category_hoodie, varient_type='SIZE')) + [None]
        return dict_maker(category_varient_hoodie_size, dict_maker(category_varient_hoodie_colors))

    def location(self, obj):
        if obj['varients']:
            category = str(obj['varients'][0].category.slug)
            varients = []
            for v in obj['varients']:
                varients.append(str(v.varient_type) + '-' +
                                str(v.value).replace(' ', '_'))
            return "/product/buy/" + category + '/' + '--'.join(varients)
        else:
            return '/'


def dict_maker(varient_list, list_dict=[{'varients': []}]):
    temp_list = list(itertools.product(list_dict, varient_list))
    final_list = []
    for a, b in temp_list:
        if b:
            final_list.append({'varients': a['varients'] + [b]})
        else:
            final_list.append({'varients': a['varients'] + []})
    return final_list


class TagSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.3

    def items(self):
        client = Client('productIndex')
        filter_tags = []
        for tag in Tag.objects.all():
            if int(client.search(tag.tag).total):
                filter_tags.append(tag)
        return filter_tags

    def location(self, obj):
        return '/aura/product/search/?search=' + str(obj.tag)


class CfblogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Content.objects.filter(status=2)


class AllSiteMap(Sitemap):
    changefreq = "daily"
    priority = 0.6
    lastmod = ''

    def items(self):
        items = ['https://www.addictionbazaar.com/product_sitemap.xml']
        items = items + ['https://www.addictionbazaar.com/product_{}_sitemap.xml'.format(str(i)) for i in xrange(1, 20)]
        return items

    def __get(self, name, obj, default=None):
        try:
          attr = getattr(self, name)
        except AttributeError:
          return default
        if callable(attr):
          return attr(obj)
        return attr

    def get_urls(self, page=1, site=None, protocol=None):
        # Determine protocol
        if self.protocol is not None:
          protocol = self.protocol
        if protocol is None:
          protocol = 'http'

        # Determine domain
        if site is None:
          if Site._meta.installed:
              try:
                  site = Site.objects.get_current()
              except Site.DoesNotExist:
                  pass
          if site is None:
              raise ImproperlyConfigured("To use sitemaps, either enable the sites framework or pass a Site/RequestSite object in your view.")
        domain = site.domain

        urls = []

        for item in self.items():
          loc = item
          priority = self.__get('priority', item, None)
          url_info = {
              'item':       item,
              'location':   loc,
              'lastmod':    datetime.datetime.today(),
              'changefreq': self.__get('changefreq', item, None),
              'priority':   str(priority is not None and priority or ''),
          }
          urls.append(url_info)
        return urls
