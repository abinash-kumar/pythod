from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db import models
import datetime

# Create your models here.


def f(instance, filename):
    ext = filename.split('.')[-1]
    name = str(datetime.datetime.now()).replace(' ', '').replace('.', '').replace(':', '')
    return "blogimages/" + '{}.{}'.format(name, ext)


class Blog(models.Model):
    slug = models.CharField(max_length=250, blank=True, null=False, editable=False)
    title = models.CharField(max_length=250, blank=False, null=False)
    meta_description = models.CharField(max_length=250, blank=True, null=True)
    author = models.ForeignKey(User)
    image = models.ImageField(upload_to=f, default='uploads/blogimages/dummy.jpg', blank=True, null=True)
    image_text = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=False, null=False)
    posted_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    views = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/blog/doc/' + self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)


class Tags(models.Model):
    for_blog = models.ForeignKey(Blog)
    tag_name = models.CharField(max_length=50, blank=False, null=False)
