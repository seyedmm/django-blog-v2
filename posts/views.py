from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import Http404
from allauth.account.utils import has_verified_email
from posts import forms, models
from comments.forms import CommentForm
from comments.models import Comment

# View for displaying a list of published posts
class PostListView(generic.ListView):
    model = models.Post
    context_object_name = 'posts'
    template_name = 'pages/post_list.html'
    paginate_by = 10

    def get_queryset(self):
        # Retrieve and return a queryset of published posts
        queryset = super(PostListView, self).get_queryset()
        return queryset.filter(status='pub').order_by('-datetime_created')


# View for displaying a list of draft posts (requires login and permission)
class DraftPostListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = models.Post
    context_object_name = 'posts'
    template_name = 'pages/post_list.html'
    permission_required = 'Post.delete_post'
    permission_denied_message = 'شما به این صفحه دسترسی ندارید'
    paginate_by = 10

    def get_queryset(self):
        # Retrieve and return a queryset of draft posts
        queryset = super(DraftPostListView, self).get_queryset()
        return queryset.filter(status='drf').order_by('-datetime_created')


# View for handling search functionality
def search_view(request):
    if request.method == 'POST':
        not_checked_comments = Comment.objects.filter(checked=False).order_by('-datetime_created')
        not_checked_comments_count = not_checked_comments.count()
        query = request.POST['search-query']
        # Filter posts based on the search query
        posts = models.Post.objects.filter(status='pub', title__contains=query)
        context = {
            'is_search': True,
            'search_query': str(query),
            'posts': posts,
            'not_checked_comments_count': not_checked_comments_count,
        }
        return render(request, 'pages/post_list.html', context)
    else:
        return redirect(reverse('home'))


# View for creating a new post (requires login and permission)
class CreatePostView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    form_class = forms.CreatePostForm
    template_name = 'pages/post_create.html'
    success_url = reverse_lazy('home')
    permission_required = 'posts.add_post'
    permission_denied_message = 'شما به این صفحه دسترسی ندارید'

    def has_permission(self):
        # Check if the user has verified their email and has permission
        has_access = super().has_permission()
        return has_access and has_verified_email(self.request.user, email=None)

    def get_success_url(self):
        success_url = reverse_lazy('post_detail', kwargs={'pk': self.object.pk})
        return str(success_url)

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'پست با موفقیت ساخته شد.')
        return super().form_valid(form)


# View for displaying post details and handling comments
def post_detail_view(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    comment_list = post.comments.filter(accepted=True).order_by('-datetime_created')
    not_checked_comments = Comment.objects.filter(checked=False).order_by('-datetime_created')
    not_checked_comments_count = not_checked_comments.count()
    if request.user.is_authenticated:
        email_verified = has_verified_email(request.user, email=None)
    else:
        email_verified = False
    if post.status == 'pub' or request.user.has_perm('posts.can_view_draft_post'):
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                messages.success(request, 'نظر شما ثبت شد و پس از تایید توسط مدیر وبسایت به نمایش در خواهد آمد. درصورت تایید یا رد نظر، شما ایمیلی دریافت خواهید کرد.')
                comment_form = CommentForm()
        else:
            comment_form = CommentForm()

        context = {
            'post': post,
            'comments': comment_list,
            'comment_form': comment_form,
            'not_checked_comments_count': not_checked_comments_count,
            'email_verified': email_verified,
        }
        return render(request, 'pages/post_detail.html', context)
    else:
        raise Http404


class PostDraftList(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = models.Post
    template_name = 'pages/post_list.html'
    permission_required = 'Post.can_view_draft_post'
    permission_denied_message = 'شما به این صفحه دسترسی ندارید'


# View for deleting a post (requires login and permission)
class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = models.Post
    template_name = 'pages/post_delete.html'
    success_url = reverse_lazy('home')
    permission_required = 'Post.delete_post'
    permission_denied_message = 'شما به این صفحه دسترسی ندارید'

    def has_permission(self):
        perms = self.get_permission_required()
        if self.request.user == self.get_object().author:
            return True
        else:
            return self.request.user.has_perms(perms)

    def form_valid(self, form):
        messages.success(self.request, 'پست با موفقیت ساخته شد')
        return super().form_valid(form)


# View for updating a post (requires login and permission)
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = models.Post
    form_class = forms.CreatePostForm
    template_name = 'pages/post_create.html'
    success_url = reverse_lazy('post_detail', {'pk': 'self.object.pk'})
    permission_required = 'Post.update_post'
    permission_denied_message = 'شما به این صفحه دسترسی ندارید'
    extra_context = {
        'is_update': True,
    }

    def has_permission(self):
        perms = self.get_permission_required()
        if self.request.user == self.get_object().author:
            return True
        else:
            return self.request.user.has_perms(perms)

    def get_success_url(self):
        success_url = reverse_lazy('post_detail', kwargs={'pk': self.object.pk})
        return str(success_url)

    def form_valid(self, form):
        messages.success(self.request, 'پست با موفقیت ویرایش شد')
        return super().form_valid(form)