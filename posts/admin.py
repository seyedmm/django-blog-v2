from django.contrib import admin
from .models import Post
from django.contrib.sites.models import Site


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'datetime_created', 'datetime_modified', 'status')
