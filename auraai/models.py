from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from product.models import Product, Category
from django.template.defaultfilters import slugify

# Create your models here.


def get_file_path(instance, filename):
    return "files/auraai/" + str(instance.id) + "_" + filename


def f(instance, filename):
    return "files/tag/banner" + filename


class UserImage(models.Model):
    FOCUS_ON = (
        ("TOP", "top"),
        ("BOTTOM", "bottom"),
        ("WHOLE", "whole")
    )
    url = models.URLField(max_length=2000, blank=True)
    imported_from = models.CharField(max_length=200, blank=True)
    uploader = models.ForeignKey(User, blank=True, null=True)
    upload_date = models.DateField(auto_now=False, auto_now_add=True)
    image_for = models.CharField(
        max_length=60, blank=True, choices=FOCUS_ON, default=FOCUS_ON[2])
    active = models.BooleanField(default=True)
    likes_top = models.IntegerField(default=0)
    likes_bottom = models.IntegerField(default=0)
    likes_whole = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    riplicable = models.BooleanField(default=True)
    photo = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    relevent = models.BooleanField(default=True)


class UserPhysique(models.Model):
    BODY_TYPE_CHOICE = (
        ("AVERAGE", "average"),
        ("EXTRA", "extra"),
        ("ATHLETIC", "athletic"),
        ("SLIM", "slim"),
        ("BIG&BOLD", "big&bold"),
        ("MUSCULAR", "muscular")
    )
    HAIR_COLOR_CHOICE = (
        ("BLACK", "black"),
        ("BROWN", "brown"),
        ("GREEN", "green"),
        ("BLUE", "BLUE"),
        ("GREY", "grey"),
        ("HAZEL", "hazel")
    )
    EYE_COLOR_CHOICE = (
        ("BLACK", "black"),
        ("BROWN", "brown"),
        ("RED", "red"),
        ("BLOND", "blond"),
        ("GREY", "grey"),
        ("WHITE", "white"),
        ("SHAVED", "shaved"),
        ("DYED", "dyed"),
        ("BULD", "buld")
    )
    GENDER_CHOICE = (
        ("MALE", "male"),
        ("FEMALE", "female"),
        ("OTHER", "other")
    )
    user = models.ForeignKey(User, blank=True, null=True)
    create_date = models.DateField(auto_now=False, auto_now_add=True)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    body_type = models.CharField(
        max_length=60, blank=True, choices=BODY_TYPE_CHOICE, default=BODY_TYPE_CHOICE[0])
    hair_color = models.CharField(
        max_length=60, blank=True, choices=HAIR_COLOR_CHOICE, default=HAIR_COLOR_CHOICE[0])
    eye_color = models.CharField(
        max_length=60, blank=True, choices=EYE_COLOR_CHOICE, default=EYE_COLOR_CHOICE[0])
    gender = models.CharField(
        max_length=20, blank=True, choices=GENDER_CHOICE, default=GENDER_CHOICE[0])
    age = models.IntegerField(default=1)


class UserFbLikes(models.Model):
    user = models.ForeignKey(User, blank=False, null=False)
    fb_page = models.CharField(max_length=300, blank=True)
    page_id = models.CharField(max_length=30, blank=True)


class UserFbDetails(models.Model):
    user = models.ForeignKey(User, blank=False, null=False)
    user_email = models.EmailField(max_length=260, blank=True)
    fb_id = models.CharField(max_length=30, blank=True)
    token = models.CharField(max_length=300, blank=True)


class Tag(models.Model):
    category = models.ForeignKey(Category)
    tag = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return self.tag

    def __unicode__(self):
        return self.tag


class ProductTagMap(models.Model):
    product = models.ForeignKey(Product)
    tag = models.ForeignKey(Tag)

    def __str__(self):
        return str(self.product) + '-' + str(self.tag)

    def __unicode__(self):
        return str(self.product) + '-' + str(self.tag)


class TagBanner(models.Model):
    banner_name = models.CharField(max_length=50, blank=False)
    tags = models.ManyToManyField(Tag)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    banner_image = models.ImageField(upload_to=f,
                                     default='uploads/blogimages/dummy.jpg',
                                     blank=True,
                                     null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.banner_name)
        super(TagBanner, self).save(*args, **kwargs)

    def __str__(self):
        return self.banner_name + str(' Active' if self.active else ' Deactive')

    def __unicode__(self):
        return self.banner_name + str(' Active' if self.active else ' Deactive')
