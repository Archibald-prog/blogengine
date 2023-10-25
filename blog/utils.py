from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
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
        context = {self.model.__name__.lower(): obj}
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

# class ObjectListMixin:
#     model = None
#     template = None
#
#     def get(self, request):
#         obj_list = self.model.objects.all()
#         context = {
#             self.model.__name__.lower() + 's': obj_list
#         }
#         return render(request, self.template, context)
