# coding=utf-8
from django.conf import settings
from django.http.response import Http404

try:
    from django.utils.deprecation import MiddlewareMixin
except Exception as e:
    MiddlewareMixin = object


class Middleware(MiddlewareMixin):

    def process_response(self, request, response):
        from absupport import views
        path = request.path_info
        if (settings.DEBUG):
            return response
        if (request.is_ajax() or
                path.startswith(settings.STATIC_URL or '///') or
                path.startswith(settings.MEDIA_URL or '///') or
                request.method == 'POST' or
                request.GET.get('prerender', None) == 'true' or
                request.subdomain in ['dashboard', 'seller']):
            return response
        elif(views.is_page_cached(path)):
            return views.cached_data(path, request)
        else:
            return response
