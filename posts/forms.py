from django import forms
from posts import models
from ckeditor.widgets import CKEditorWidget


# from tinymce.widgets import TinyMCE


class CreatePostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = models.Post
        fields = ['title', 'description', 'body', 'status']

