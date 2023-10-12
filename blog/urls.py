from django.urls import path

from blog.views import *

urlpatterns = [
    path('', posts_list),
]
