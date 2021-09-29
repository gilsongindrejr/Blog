from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.utils.translation import gettext as _, get_language, activate

from taggit.models import Tag

from .models import Post
from .forms import ShareForm, CommentModelForm


def post_list(request, tag_slug=None):
    context = {}
    objects = Post.published.all()
    tag = None
    lang = get_language()
    context['lang'] = lang
    activate(lang)

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        objects = objects.filter(tags__in=[tag])

    paginator = Paginator(objects, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context['page'] = page
    context['posts'] = posts
    context['tag'] = tag
    return render(request, 'blog/index.html', context)


def post_detail(request, year, month, day, slug):
    context = {}
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
    lang = get_language()
    context['lang'] = lang
    activate(lang)

    if request.method == 'POST':
        comment_form = CommentModelForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            comment_form = CommentModelForm()
    else:
        comment_form = CommentModelForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    context['post'] = post
    context['comments'] = comments
    context['new_comment'] = new_comment
    context['comment_form'] = comment_form
    context['similar_posts'] = similar_posts
    return render(request, 'blog/detail.html', context)


def post_share(request, post_id):
    context = {}
    post = get_object_or_404(Post, id=post_id, status='published')
    shared = False
    lang = get_language()
    context['lang'] = lang
    activate(lang)

    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} {_('recommends you read')} {post.title}"
            message = f"{_('Read')} {post.title} {_('at')} {post_url}\n\n{cd['name']}\'s {_('comments')}: {cd['comments']}"
            send_mail(
                subject=subject,
                message=message,
                from_email='junior.gindre@gmail.com',
                recipient_list=[cd['to']]
            )
            shared = True
    else:
        form = ShareForm()
    context['form'] = form
    context['post'] = post
    context['shared'] = shared
    return render(request, 'blog/share.html', context)
