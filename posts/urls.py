from django.urls import path
from posts import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('drafts', views.DraftPostListView.as_view(), name='draft_post_list'),
    path('search', views.search_view, name='search'),
    path('newpost', views.CreatePostView.as_view(), name='new_post'),
    path('<int:pk>', views.post_detail_view, name='post_detail'),
    path('delete/<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('update/<int:pk>', views.PostUpdateView.as_view(), name='post_update'),
]
