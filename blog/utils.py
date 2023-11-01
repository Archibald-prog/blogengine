from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

from uuid import uuid4
from pytils.translit import slugify


def gen_slug(instance, slug):
    """Generates unique slugs for models"""
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:4]}'
    return unique_slug


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        context = {
            self.model.__name__.lower(): obj,
            'admin_object': obj,
            'detail': True
        }
        return render(request, self.template, context)


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        context = {
            'form': form
        }
        return render(request, self.template, context)

    def post(self, request):
        bound_form = self.form_model(request.POST)

        context = {
            'form': bound_form
        }

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context)


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        context = {
            'form': bound_form,
            self.model.__name__.lower(): obj
        }
        return render(request, self.template, context)

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)
        context = {
            'form': bound_form,
            self.model.__name__.lower(): obj
        }
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context)


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        context = {
            self.model.__name__.lower(): obj
        }
        return render(request, self.template, context)

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))


class ObjectListMixin:
    model = None
    template = None
    paginate_by = None

    def get(self, request):
        search_query = request.GET.get('search', '')

        if search_query:
            obj_list = self.model.objects.filter(Q(title__icontains=search_query) |
                                                 Q(body__icontains=search_query))
        else:
            obj_list = self.model.objects.all()

        if self.paginate_by is not None:
            paginator = Paginator(obj_list, self.paginate_by)
            page_number = request.GET.get('page', 1)
            page = paginator.get_page(page_number)
            is_paginated = page.has_other_pages()

            if page.has_previous():
                previous_page_url = '?page={}'.format(page.previous_page_number())
            else:
                previous_page_url = ''

            if page.has_next():
                next_page_url = '?page={}'.format(page.next_page_number())
            else:
                next_page_url = ''

            context = {
                'page_object': page,
                'is_paginated': is_paginated,
                'previous_url': previous_page_url,
                'next_url': next_page_url
            }
        else:
            context = {
                self.model.__name__.lower() + 's': obj_list
            }
        return render(request, self.template, context)
