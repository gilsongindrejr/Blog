import pytest
from model_bakery import baker

from posts.models import Post, Comment

pytestmark = pytest.mark.django_db


@pytest.fixture
def post():
    post1 = baker.make(Post)
    post1.status = 'published'
    post1.save()
    return post1


@pytest.fixture
def comment():
    return baker.make(Comment)


def test_post_str(post):
    assert post.title == str(post)


def test_post_get_absolute_url_method(post):
    assert post.get_absolute_url() == f'/blog/{post.publish.year}/{post.publish.month}/{post.publish.day}/{post.slug}/'


def test_comment_str(comment):
    assert str(comment) == f'Comment by {comment.name} on post {comment.post}'


def test_post_published_manager(post):
    assert Post.published.all()[0] == Post.objects.filter(status='published')[0]
