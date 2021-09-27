from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import reverse

from taggit.managers import TaggableManager


class PostManager(models.Manager):
    def get_queryset(self):
        return super(PostManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(get_user_model(), related_name='posts', on_delete=models.CASCADE)
    slug = models.SlugField(unique_for_date='publish', max_length=250)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='draft')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PostManager()
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-publish',)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.name} on post {self.post}'
