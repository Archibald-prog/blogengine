from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import View
from .models import Post, Tag
from .forms import TagForm
from .utils import ObjectDetailMixin


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


class TagCreate(View):
    def get(self, request):
        form = TagForm()
        context = {
            'form': form
        }
        return render(request, 'blog/tag_create.html', context)

    def post(self, request):
        bound_form = TagForm(request.POST)

        context = {
            'form': bound_form
        }

        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        return render(request, 'blog/tag_create.html', context)


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
