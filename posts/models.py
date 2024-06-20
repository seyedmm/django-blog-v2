from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import RichTextField


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (
        ('pub', 'عمومی'),
        ('drf', 'پیش نویس')
    )

    title = models.CharField(max_length=90, null=False, blank=False, verbose_name='عنوان')
    description = models.TextField(max_length=600, verbose_name='توضیحات')
    body = RichTextField(verbose_name='بدنه')
    author = models.ForeignKey(get_user_model(), models.CASCADE, verbose_name='نویسنده')
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name='آخرین ویرایش')
    status = models.CharField(choices=STATUS_CHOICES, max_length=3, verbose_name='حالت انتشار')

    class Meta:
        verbose_name = 'پست'
        permissions = (
            ("can_view_draft_post", "دیدن پست های پیش نویس"),)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
