from __future__ import unicode_literals

import os
import datetime
from django.db import models
from customer.models import Customer
from product.models import Category, Product
from django.template.defaultfilters import slugify
from urlparse import urlparse
from abutils.telegram import send_message as telegram
from PIL import ImageFile
from resizeimage import resizeimage
from abutils.utils import create_tiny_artist_design
from product import constant as product_constant

from customer.models import Coupon
# from abutils.telegram import send_message as telegram

# Create your models here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ArtistDetail(models.Model):
    ARTIST_TYPE = (
        ("INDEPENDENT", "INDEPENDENT"),
        ("YOUTUBER", "YOUTUBER"),
        ("BLOGGER", "BLOGGER"),
        ("NGO", "NGO"),
        ("OTHER", "OTHER"),
    )
    customer = models.OneToOneField(Customer, related_name='artist')
    about = models.CharField(max_length=500, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    pin_code = models.IntegerField(null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    state = models.CharField(max_length=60, blank=True, null=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    artist_type = models.CharField(
        max_length=60, blank=True, null=True, choices=ARTIST_TYPE)

    def __unicode__(self):
        return self.customer.customer.first_name + ' ' + self.customer.customer.last_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.customer.customer.first_name + self.customer.customer.last_name)
        telegram("New Arist signed up : " + self.customer.customer.first_name + " " + self.customer.customer.last_name)
        super(ArtistDetail, self).save(*args, **kwargs)


class ArtistBankDetail(models.Model):
    ACCOUNT_TYPE = (
        ("SAVING", "SAVING"),
        ("CURRENT", "CURRENT"),
    )
    artist = models.ForeignKey(ArtistDetail, null=False, blank=False)
    account_holder_name = models.CharField(
        max_length=60, blank=False, null=False)
    bank_name = models.CharField(max_length=100, blank=False, null=False)
    branch_name = models.CharField(max_length=100, blank=False, null=False)
    pan = models.CharField(max_length=15, blank=False, null=False)
    ifsc_code = models.CharField(max_length=15, blank=False, null=False)
    account_no = models.CharField(max_length=30, blank=False, null=False)
    bank_branch_address = models.CharField(
        max_length=200, blank=False, null=False)
    account_type = models.CharField(
        max_length=60, blank=True, null=True, choices=ACCOUNT_TYPE)


class SocialLink(models.Model):
    artist = models.ForeignKey(ArtistDetail, null=False, blank=False)
    url = models.URLField(max_length=600, null=False, blank=False)
    website = models.CharField(
        max_length=60, blank=True, null=True)

    def save(self, *args, **kwargs):
        website = urlparse(self.url).hostname
        self.website = website
        artist_links = SocialLink.objects.filter(artist=self.artist, website=website)
        if len(artist_links) == 0:
            super(SocialLink, self).save(*args, **kwargs)


def get_artwork_path(instance, filename):
    path = "artist_design/" + \
        str(instance.customer.customer.customer.username) + "/"
    filepath = BASE_DIR + "/uploads/" + path
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    ext = filename.split('.')[-1]
    name = str(datetime.datetime.now()).replace(
        ' ', '').replace('.', '').replace(':', '')
    return path + '{}.{}'.format(name, ext)


class ArtistDesign(models.Model):
    STATUS_TYPE = (
        ("APPROVED", "APPROVED"),
        ("PENDING", "PENDING"),
        ("REJECTED", "REJECTED")
    )
    customer = models.ForeignKey(ArtistDetail, related_name='ab_artist')
    categoty = models.ManyToManyField(Category)
    title = models.TextField(null=True, blank=True, max_length=100)
    comment = models.TextField(null=True, blank=True, max_length=1500)
    tags = models.TextField(null=True, blank=True, max_length=1500)
    create_date = models.DateField(auto_now=False, auto_now_add=True)
    status = models.CharField(max_length=150, choices=STATUS_TYPE)
    design = models.FileField(upload_to=get_artwork_path,
                              default='uploads/blogimages/dummy.jpg',
                              blank=True,
                              null=True)

    def __unicode__(self):
        return unicode(self.title) or u''

    def create_thumbnail(self):
        original_image_path = self.design.url.split('/', 1)[1]
        original_image = open(original_image_path.replace('%40', '@'), 'rw')
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        img = ImageFile.Image.open(original_image)
        img.load()
        img = resizeimage.resize_thumbnail(img, [200, 200])
        path, file_name = original_image_path.rsplit('/', 1)
        new_path = path.replace('%40', '@') + "/th_" + file_name
        img.save(new_path, img.format)
        original_image.close()
        create_tiny_artist_design(self.design.path, new_path)

    def get_thumbname_url(self):
        try:
            s = str(self.design.size)
        except Exception:
            s= " "
        path, file_name = self.design.url.rsplit('/', 1)
        return path + "/th_" + file_name + "?s=" + s


class ProductArtistDesignMap(models.Model):
    product = models.ForeignKey(Product, blank=False, null=False)
    artist_design = models.ForeignKey(ArtistDesign, blank=False, null=False)
    product_type = models.CharField(max_length=150, choices=product_constant.ALL_CATEGORIES)

    def __str__(self):
        return str(self.artist_design.title) + "-" + str(self.product.name)

    def __unicode__(self):
        return unicode(self.artist_design.title) + "-" + unicode(self.product.name)



class ArtistCoupon(Coupon):
    artist = models.ForeignKey(ArtistDetail)
    
    def condition(self):
        pass