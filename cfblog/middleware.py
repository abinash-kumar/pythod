# coding=utf-8
from django.conf import settings
from django.http.response import Http404

try:
    from django.utils.deprecation import MiddlewareMixin
except Exception as e:
    MiddlewareMixin = object


class Middleware(MiddlewareMixin):

    def process_response(self, request, response):
        # ignore all ajax, static and media requests
        # from product.views import get_category_and_varients_from_slug
        # ignore all product listing requests
        path = request.path_info
        slug = path
        if request.is_ajax() or \
                path.startswith(settings.STATIC_URL or '///') or \
                path.startswith(settings.MEDIA_URL or '///'):
            return response

        # if response.status_code != 404 and get_category_and_varients_from_slug(slug)[0]:
        #     return response

        from .views import cms_page_index
        # we return the original response
        # if the 404 response is given by cms_page_index
        if getattr(request.resolver_match, 'func', None) is cms_page_index:
            return response

        try:
            return cms_page_index(request)
        except Http404:
            return response
        except Exception:
            if settings.DEBUG:
                raise
            return response
