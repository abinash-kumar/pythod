from __future__ import unicode_literals
import os
from django.conf import settings
from seller.models import Seller
from django.db import models
from django.template.defaultfilters import slugify
import datetime
from django_extensions.db.fields import UUIDField
from abutils.telegram import send_message as telegram
import uuid
# Create your models here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_user_image_path(instance, filename):
    reqpath = "designer_photo/"
    filepath = settings.BASE_DIR + "/uploads/" + reqpath
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    ext = filename.split('.')[-1]
    name = str(instance.designer.seller.first_name).lower() + "_" + str(instance.id)
    return reqpath + '{}.{}'.format(name, ext)


class Designer(models.Model):
    """docstring for Customer"""
    GENDER = (
        ("MALE", "male"),
        ("FEMALE", "female")
    )
    designer = models.OneToOneField(Seller, on_delete=models.CASCADE, related_name='ab_designer')
    slug = models.SlugField(max_length=200, blank=True, null=True)
    awards = models.CharField(max_length=200, blank=True, null=True)
    education = models.CharField(max_length=200, blank=True, null=True)
    working_since = models.DateTimeField(null=True, blank=True)
    about = models.CharField(max_length=2000, blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    user_photo = models.ImageField(upload_to=get_user_image_path,
                                   default='uploads/user_dummy.jpg',
                                   blank=True,
                                   null=True)

    def __unicode__(self):
        return self.designer.seller.first_name

    def get_work_experience(self):
        this_year = datetime.datetime.today().year
        experience = this_year - self.working_since.year
        if experience == 0:
            return '< 1'
        else:
            return str(experience)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.designer.seller.first_name + self.designer.seller.last_name)
        telegram("New Arist signed up : " + self.designer.seller.first_name + " " + self.designer.seller.last_name)
        super(Designer, self).save(*args, **kwargs)


class DesignerSocialLinks(models.Model):
    designer = models.OneToOneField(Designer, on_delete=models.CASCADE, related_name='ab_designer_social_links')
    website = models.CharField(max_length=200, blank=True, null=True)
    fb = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    youtube = models.CharField(max_length=200, blank=True, null=True)


def designer_slider_images(instance, filename):
    if instance.__class__.__name__ == 'DesignercollageImages':
        reqpath = "designer_photo/collage" + str(instance.designer.pk) + "/"
    if instance.__class__.__name__ == 'DesignerSliderImages':
        reqpath = "designer_photo/slider" + str(instance.designer.pk) + "/"
    filepath = BASE_DIR + "/uploads/" + reqpath
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    ext = filename.split('.')[-1]
    name = str(datetime.datetime.now()).replace(' ', '').replace('.', '').replace(':', '')
    return reqpath + '{}.{}'.format(name, ext)


class DesignerSliderImages(models.Model):
    designer = models.ForeignKey(Designer)
    title = models.CharField(max_length=150, unique=False)
    description = models.CharField(max_length=150, unique=False)
    image = models.ImageField(upload_to=designer_slider_images,
                              default='uploads/blogimages/dummy.jpg',
                              blank=True, null=True)
    active = models.BooleanField(default=False)
    display_priority = models.IntegerField(null=True)

    def __unicode__(self):
        return self.title


class DesignercollageImages(models.Model):
    designer = models.ForeignKey(Designer)
    title = models.CharField(max_length=150, unique=False)
    description = models.CharField(max_length=150, unique=False)
    image = models.ImageField(upload_to=designer_slider_images,
                              default='uploads/blogimages/dummy.jpg',
                              blank=True, null=True)
    active = models.BooleanField(default=False)
    display_priority = models.IntegerField(null=True)

    def __unicode__(self):
        return self.title


class DesignerContactDetails(models.Model):
    STATUS = (
        ("DRAFT", "draft"),
        ("CONTACTED", "contacted"),
        ("RESPONDED", "responded"),
        ("FOLLOWUP", "followup"),
        ("ONBOARDED", "onboarded"),
        ("REFUSED", "refused")
    )
    CONTACT_CHANNEL = (
        ("EMAIL", "email"),
        ("INPERSON", "inperson"),
        ("SELF", "self")
    )
    unique_id = UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=150, blank=False)
    email=models.CharField(max_length=150, blank=True)
    mobile = models.CharField(max_length=60, blank=True)
    website=models.CharField(max_length=150, blank=True)
    address=models.CharField(max_length=400, blank=True)
    status = models.CharField(max_length=60, choices=STATUS, blank=False, default=STATUS[1])
    contact_channel = models.CharField(max_length=60, choices=CONTACT_CHANNEL, blank=False, default=CONTACT_CHANNEL[1])
    remarks=models.CharField(max_length=400, blank=True)

