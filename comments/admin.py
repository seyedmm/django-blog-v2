from django.contrib import admin
from comments import models


# Register your models here.
@admin.register(models.Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('text', 'checked', 'accepted', 'author', 'post', 'datetime_created')
