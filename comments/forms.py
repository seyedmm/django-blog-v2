from django.forms import ModelForm
from comments.models import Comment
from django.forms.models import modelformset_factory

AcceptFormSetBase = modelformset_factory(Comment, extra=0, fields=('accepted',))


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
