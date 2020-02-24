# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Channel
from .models import ExpenceDetails
from .models import ABDoc
from django.contrib.auth.models import User
admin.site.register(Channel)


class ExpenceDetailsView(admin.ModelAdmin):
    list_display = ["remark", "channel", "expense_date", "amount", "expense_by", "created_date"]
    readonly_fields = ('updated_by',)
    model = ExpenceDetails
    filter_horizontal = ['bill']
    search_fields = ["expense_by", "remark", "channel"]

    def save_model(self, request, obj, form, change):
        obj.updated_by = User.objects.get(id=request.user.id)
        obj.save()


admin.site.register(ExpenceDetails, ExpenceDetailsView)


class ABDocView(admin.ModelAdmin):
    list_display = ["title", "file"]
    search_fields = ["title", "file"]


admin.site.register(ABDoc, ABDocView)
