from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    paginate_by = 3
    template_name = 'blog/index.html'
    context_object_name = 'posts'


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=slug
    )
    return render(request, 'blog/detail.html', {'post': post})
