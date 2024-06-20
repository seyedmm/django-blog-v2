from django.urls import path
from comments.views import comment_check_view

urlpatterns = [
    path('not_accepted/<int:page_num>', comment_check_view, name='not_accepted_comments'),
    path('not_accepted/', comment_check_view, name='not_accepted_comments_no_arg'),
]