from django.http import HttpResponse


def posts_list(request):
    return HttpResponse('<h1>Hello World</h1>')
