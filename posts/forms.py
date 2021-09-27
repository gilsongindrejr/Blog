from django import forms

from .models import Comment


class ShareForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentModelForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'body')
