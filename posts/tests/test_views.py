from django.test import Client, RequestFactory
from django.shortcuts import reverse
import pytest
from model_bakery import baker

from posts.views import post_share, post_detail, post_list
from posts.models import Post

pytestmark = pytest.mark.django_db


@pytest.fixture
def request_obj():
    return RequestFactory()


@pytest.fixture
def post():
    post = baker.make(Post)
    post.status = 'published'
    post.save()
    return post


def test_post_share_view(post, request_obj):
    data = {'name': 'name', 'email': 'name@email.com', 'to': 'another@email.com', 'comments': 'Comments'}
    request_post = request_obj.post('/blog/1/share/', data)
    request_get = request_obj.get('/blog/1/share/')
    assert request_post.method == 'POST'
    assert request_get.method == 'GET'
    assert post_share(request_post, 1).status_code == 200
    assert post_share(request_get, 1).status_code == 200


def test_post_detail_view(post, request_obj):
    url = reverse('blog:detail', args=(
        post.publish.year, post.publish.month, post.publish.day, post.slug
    ))
    comment_data = {
        'post': post.id,
        'name': 'Name',
        'body': 'Comment',
    }
    request_post = request_obj.post(url, data=comment_data)
    assert request_post.method == 'POST'
    request_get = request_obj.get(url)
    assert request_get.method == 'GET'
    assert post_detail(request_post, post.publish.year, post.publish.month, post.publish.day, post.slug).status_code == 200
    assert post_detail(request_get, post.publish.year, post.publish.month, post.publish.day, post.slug).status_code == 200


def test_post_list_view(post, request_obj):
    request = request_obj.get(reverse('blog:index'))
    post.tags.add('tag')
    assert post_list(request).status_code == 200
    assert post_list(request, post.tags.all()[0]).status_code == 200
    assert post_list(request, post.tags.all()[0], page=2).status_code == 200

