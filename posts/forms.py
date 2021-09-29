from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment


class ShareForm(forms.Form):
    name = forms.CharField(label=_('Name'), max_length=25)
    email = forms.EmailField()
    to = forms.EmailField(label=_('To'))
    comments = forms.CharField(label=_('Comments'), required=False, widget=forms.Textarea)


class CommentModelForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'body')
