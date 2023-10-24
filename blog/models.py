from django.db import models
from django.shortcuts import reverse

from .utils import gen_slug


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.title)


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)
