from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Store(models.Model):
	"""docstring for Store"""
	name = models.CharField(max_length=120, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    open_since = models.DateTimeField(auto_now_add=True, auto_now=False)

		