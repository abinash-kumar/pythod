from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown2
# Create your views here.
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext

from .models import Blog


def view_post(request, slug):
    all_post = Blog.objects.filter(active=True)
    month_year = []
    for i in all_post:
        month_year.append(i.posted_on.strftime('%B %Y'))
    month_year = set(month_year)
    post = get_object_or_404(Blog, slug=slug, active=True)
    post.content = markdown2.markdown(post.content)
    return render_to_response('blog/blog_post.html',
                              {
                                  'post': post,
                                  'calender': month_year
                              },
                              context_instance=RequestContext(request))


def view_imp_doc(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    post.content = markdown2.markdown(post.content)
    return render_to_response('blog/other_doc.html',
                              {
                                  'post': post,
                              },
                              context_instance=RequestContext(request))


def view_post_archived(request, slug):
    all_post = Blog.objects.filter(active=True)
    req_post = []
    for i in all_post:
        if i.posted_on.strftime('%B %Y') == slug.replace('*', ' '):
            req_post.append(i)

    post_all = []
    for i in req_post:
        k = {}
        try:
            k['image'] = i.image
        except ValueError:
            k['image'] = "None"
        k['content']=markdown2.markdown(i.content[0:200])
        k['title'] = i.title
        k['slug'] = i.slug
        post_all.append(k)

    paginator = Paginator(post_all, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post_list = paginator.page(paginator.num_pages)

    return render_to_response('blog/blog_all.html',
                              {
                                  'post': post_list,
                                  'page': page
                              },
                              context_instance=RequestContext(request))


def view_all(request):
    post = Blog.objects.filter(active=True)

    post_all = []
    for i in post:
        k = {}
        try:
            k['image'] = i.image
        except ValueError:
            k['image'] = "None"
        k['content'] = markdown2.markdown(i.content[0:200])
        k['title'] = i.title
        k['slug'] = i.slug
        post_all.append(k)

    paginator = Paginator(post_all, 5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post_list = paginator.page(paginator.num_pages)

    return render_to_response('blog/blog_all.html',
                              {
                                  'post': post_list,
                                  'page': page
                              },
                              context_instance=RequestContext(request))
