from django.shortcuts import render


def posts_list(request):
    name_lst = ['John', 'Nick', 'Mary', 'Margaret']
    context = {
        'names': name_lst
    }
    return render(request, 'blog/index.html', context)
