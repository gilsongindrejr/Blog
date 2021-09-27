from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail

from .models import Post
from .forms import ShareForm, CommentModelForm


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
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentModelForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = CommentModelForm()
    else:
        comment_form = CommentModelForm()
    return render(
        request,
        'blog/detail.html',
        {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form
        }
    )


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    shared = False

    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(
                subject=subject,
                message=message,
                from_email='junior.gindre@gmail.com',
                recipient_list=[cd['to']]
            )
            shared = True
    else:
        form = ShareForm()
    return render(request, 'blog/share.html', {'form': form, 'post': post, 'shared': shared})
