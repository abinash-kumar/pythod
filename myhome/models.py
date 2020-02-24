import datetime
import os

from django.contrib.auth.models import User
from django.db import models

from product.models import Category

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def f(instance, filename):
        reqpath = "selfibaaz/" + str(instance.user.pk) + "/"
        filepath = BASE_DIR + "/uploads/" + reqpath
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        ext = filename.split('.')[-1]
        name = str(datetime.datetime.now()).replace(' ', '').replace('.', '').replace(':', '')
        return reqpath + '{}.{}'.format(name, ext)


class Selfibaaz(models.Model):
    user = models.ForeignKey(User)
    selfi = models.ImageField(upload_to=f,
                              default='uploads/blogimages/dummy.jpg',
                              blank=True, null=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.first_name


def home_page_image_upload(instance, filename):
        reqpath = "homepage/"
        filepath = BASE_DIR + "/uploads/" + reqpath
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        ext = filename.split('.')[-1]
        name = str(datetime.datetime.now()).replace(' ', '').replace('.', '').replace(':', '')
        return reqpath + '{}.{}'.format(name, ext)


def home_page_image_upload_mobile(instance, filename):
        reqpath = "homepage/"
        filepath = BASE_DIR + "/uploads/" + reqpath
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        ext = filename.split('.')[-1]
        name = "m_" + str(datetime.datetime.now()).replace(' ', '').replace('.', '').replace(':', '')
        return reqpath + '{}.{}'.format(name, ext)


class SliderImages(models.Model):
    title = models.CharField(max_length=150, unique=False)
    description = models.CharField(max_length=150, unique=False)
    image = models.ImageField(upload_to=home_page_image_upload,
                              default='uploads/blogimages/dummy.jpg',
                              blank=True, null=True)
    image_mobile = models.ImageField(upload_to=home_page_image_upload_mobile,
                                     default='uploads/blogimages/dummy.jpg',
                                     blank=True, null=True)
    active = models.BooleanField(default=False)
    url = models.URLField(max_length=200, blank=True, null=True)
    display_priority = models.IntegerField(null=True)

    def __unicode__(self):
        return self.title


class OtherBanners(models.Model):
    name = models.CharField(max_length=150, unique=False)
    image = models.ImageField(upload_to=home_page_image_upload,
                              default='uploads/blogimages/dummy.jpg',
                              blank=True, null=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class CategoryImage(models.Model):
    category = models.ForeignKey(Category)
    image_on_page = models.ImageField(upload_to=home_page_image_upload,
                                      default='uploads/blogimages/dummy.jpg',
                                      blank=True, null=True)
    image_on_menu = models.ImageField(upload_to=home_page_image_upload,
                                      default='uploads/blogimages/dummy.jpg',
                                      blank=True, null=True)

    def __unicode__(self):
        return self.category.name


class DesignerImage(models.Model):
    designer = models.CharField(max_length=150, unique=False)
    image_on_page = models.ImageField(upload_to=home_page_image_upload,
                                      default='uploads/blogimages/dummy.jpg',
                                      blank=True, null=True)

    def __unicode__(self):
        return self.designer
