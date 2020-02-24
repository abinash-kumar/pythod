import json
import logging
import operator
import uuid
from orderedset import OrderedSet

import ast
from django.db.models import Q
from django.conf import settings
from django.core import serializers
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django_redis import get_redis_connection
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.forms.models import model_to_dict

# AB import

from seller.models import Seller

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@csrf_exempt
def get_all_sellers(request):
    response = []
    all_active_sellers = Seller.objects.filter(is_active=True)
    for seller in all_active_sellers:
        response.append(seller.get_detailed_json())
    return JsonResponse(response, safe=False)