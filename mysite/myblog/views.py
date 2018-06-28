import markdown
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Post, Category, Tag

import logging


logger = logging.getLogger(__name__)


'''
def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'myblog/index.html', context={
        'post_list': post_list,
    })
'''


class IndexView(ListView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'post_list'
    paginate_by = 8

    def get_queryset(self):
        return Post.objects.order_by('-modified_time')


def detail(request, slugtitle):
    post = get_object_or_404(Post, slug=slugtitle)
    post.views_add()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite', # codehilite和代码高亮插件prism.js共同使用
                                  ])
    return render(request, 'myblog/detail.html', context={
        'post': post,
    })


class ArchiveView(IndexView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs['year']
        month = self.kwargs['month']

        return Post.objects.filter(modified_time__year=year,
                                   modified_time__month=month
                                   ).order_by('-modified_time')



'''
def category(request, pk):
    c = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=c).order_by('-created_time')
    return render(request, 'myblog/index.html', context={
        'post_list': post_list,
    })
'''


class CategoryView(IndexView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        logger.info('get_queryset in class CategoryView')
        c = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(category=c).order_by('-modified_time')


class TagView(IndexView):
    model = Post
    template_name = 'myblog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs['pk'])
        return Post.objects.filter(tags=t).order_by('-modified_time')


def about(request):
    return render(request, 'myblog/about.html', context={
    })


def signin(request):
    return render(request, 'myblog/signin.html', context={
    })


def register(request):
    return render(request, 'myblog/register.html', context={
    })





