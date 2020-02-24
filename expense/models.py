from __future__ import unicode_literals
from django.db import models
import os
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_file_path(instance, filename):
    return "files/" + filename


class Channel(models.Model):
    channelName = models.CharField(max_length=120, blank=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.channelName)


class ExpenceDetails(models.Model):
    channel = models.ForeignKey('Channel')
    created_date = models.DateField(auto_now=False, auto_now_add=True)
    updated_date = models.DateField(auto_now=True, auto_now_add=False)
    expense_date = models.DateField(default=datetime.now, blank=False)
    expense_by = models.ForeignKey(User, related_name='expence_by')
    updated_by = models.ForeignKey(User, related_name='updated_by')
    amount = models.IntegerField(blank=False, default=0)
    remark = models.CharField(max_length=500, default='', blank=False)
    bill = models.ManyToManyField('ABDoc', blank=True)

    def __unicode__(self):
        return unicode(self.remark)


class ABDoc(models.Model):
    title = models.CharField(max_length=120, blank=False, unique=True)
    user = models.ForeignKey(User)
    file = models.FileField(upload_to=get_file_path, blank=False)

    def __unicode__(self):
        return unicode(self.title)
