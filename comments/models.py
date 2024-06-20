from django.db import models
from posts.models import Post
from django.contrib.auth import get_user_model


# Create your models here.
class Comment(models.Model):
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='comments',
                               verbose_name='نویسنده', null=False, blank=False)

    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments',
                             verbose_name='پست', null=False, blank=False)

    text = models.TextField(max_length=480, verbose_name='متن', null=False, blank=False)

    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name='زمان نوشتن', null=False, blank=False)

    accepted = models.BooleanField(max_length=1, verbose_name='تایید شده', default=False,
                                 null=False, blank=False)
    checked = models.BooleanField(max_length=1, verbose_name='بررسی شده', default=False,
                                 null=False, blank=False)

    class Meta:
        verbose_name = 'کامنت'
        permissions = (('accept_comment','تایید کامنت'),)

    def __str__(self):
        return self.text[:20]
