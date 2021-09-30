import pytest
from model_bakery import baker

from posts.forms import ShareForm, CommentModelForm

pytestmark = pytest.mark.django_db


@pytest.fixture
def form():
    form_data = {'name': 'name', 'email': 'name@email.com', 'to': 'another@email.com', 'comments': 'Comment'}
    form = ShareForm(data=form_data)
    return form


def test_if_form_is_valid(form):
    assert form.is_valid()


def test_form_attributes(form):
    form.is_valid()
    assert form.cleaned_data['name'] == 'name'
    assert form.cleaned_data['email'] == 'name@email.com'
    assert form.cleaned_data['to'] == 'another@email.com'
    assert form.cleaned_data['comments'] == 'Comment'


def test_form_name_max_length(form):
    form.is_valid()
    assert len(form.cleaned_data['name']) <= 9
