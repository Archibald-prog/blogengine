from django.shortcuts import render
from django.views.generic.base import View
from .models import Post, Tag
from .forms import TagForm, PostForm
from .utils import ObjectDetailMixin, ObjectCreateMixin


# class PostsList(ObjectListMixin, View):
#     model = Post
#     template = 'blog/index.html'


def posts_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/index.html', context)


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create_form.html'


class TagCreate(ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tag_create.html'


# class TagsList(ObjectListMixin, View):
#     model = Tag
#     template = 'blog/tags_list.html'


def tags_list(request):
    tags = Tag.objects.all()
    context = {
        'tags': tags
    }
    return render(request, 'blog/tags_list.html', context)


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'
