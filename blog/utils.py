from django.shortcuts import render
from django.shortcuts import get_object_or_404


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        context = {self.model.__name__.lower(): obj}
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
