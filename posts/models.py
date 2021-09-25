from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(get_user_model(), related_name='posts', on_delete=models.CASCADE)
    slug = models.SlugField(unique_for_date='published', max_length=250)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='draft')
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-published',)
