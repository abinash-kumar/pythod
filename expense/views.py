# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import ExpenceDetails, ABDoc, Channel
import datetime
from django.db.models import Sum
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')
    expence_list = ExpenceDetails.objects.order_by('expense_date')
    from_date = None
    to_date = None
    if((request.GET.get('from_date', None)) and (request.GET.get('to_date', None))):
        from_date = request.GET.get('from_date', None)
        to_date = request.GET.get('to_date', None)
        from_date_object = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        to_date_object = datetime.datetime.strptime(to_date, '%Y-%m-%d')
        expence_list = ExpenceDetails.objects.filter(expense_date__range=(from_date_object, to_date_object))

    expence_data_by_user = []
    expence_by_users = ExpenceDetails.objects.values('expense_by').distinct()
    for i in expence_by_users:
        expence_data = {}
        expence_data['user'] = User.objects.get(id=i['expense_by']).username
        expence_data['amount'] = expence_list.filter(expense_by__id=i['expense_by']).aggregate(Sum('amount'))
        expence_data_by_user.append(expence_data)

    expence_data_by_category = []
    expence_by_category = ExpenceDetails.objects.values('channel').distinct()
    for i in expence_by_category:
        expence_data = {}
        expence_data['channel'] = Channel.objects.get(id=i['channel'])
        expence_data['amount'] = expence_list.filter(channel__id=i['channel']).aggregate(Sum('amount'))
        expence_data_by_category.append(expence_data)

    expence_data = []
    for i in expence_list:
        expence = {}
        expence['expence'] = i
        expence['bills'] = i.bill.all()
        expence_data.append(expence)
    bill_list = ABDoc.objects.order_by('title')
    expence_sum = expence_list.aggregate(Sum('amount'))
    context = {
        'expence_data': expence_data,
        'bill_list': bill_list,
        'expence_sum': expence_sum,
        'expence_data_by_user': expence_data_by_user,
        'expence_data_by_category': expence_data_by_category,
        'from_date': from_date,
        'to_date': to_date
    }
    return render(request, "all_expense.html", context)
