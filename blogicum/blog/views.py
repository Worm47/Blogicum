from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

from .constants import POSTS_PER_PAGE, USER
from .forms import CommentForm, PostForm
from .mixins import (
    CommentSuccessUrlMixin,
    OnlyAuthorMixin,
    PostsQuerySetMixin
)
from .models import Category, Comment, Post
from .serializers import PostSerializer


def get_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)


class HomepageListView(PostsQuerySetMixin, ListView):
    model = Post
    paginate_by = POSTS_PER_PAGE
    template_name = "blog/index.html"

    def get_queryset(self):
        return self.get_filtered_queryset()


class CategoryPostsListView(PostsQuerySetMixin, ListView):
    model = Post
    paginate_by = POSTS_PER_PAGE
    template_name = 'blog/category.html'

    def get_queryset(self):
        category_obj = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug']
        )
        qs = self.get_filtered_queryset()
        return qs.filter(category=category_obj)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.only('is_published', 'slug'),
            is_published=True, slug=self.kwargs['category_slug']
        )
        return context


class ProfileListView(PostsQuerySetMixin, ListView):
    model = Post
    paginate_by = POSTS_PER_PAGE
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            USER,
            username=self.kwargs['username']
        )
        return context

    def get_queryset(self):
        user_obj = get_object_or_404(
            USER,
            username=self.kwargs['username']
        )
        if user_obj == self.request.user:
            qs = self.get_base_queryset()
        else:
            qs = self.get_filtered_queryset()

        return qs.filter(author=user_obj)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    fields = ('first_name', 'last_name', 'username', 'email')
    model = USER
    template_name = 'blog/user.html'

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.object.username}
        )

    def get_object(self):
        return self.request.user


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        post_obj = self.get_object()
        if user != post_obj.author:
            post_obj = get_object_or_404(
                Post,
                id=self.kwargs['post_id'],
                category__is_published=True,
                is_published=True,
                pub_date__lte=timezone.now()
            )
        context['comments'] = post_obj.comments.select_related('author')
        context['form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(LoginRequiredMixin, OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(LoginRequiredMixin, OnlyAuthorMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = "blog/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        return context

    def get_success_url(self):
        return reverse('blog:index')


class CommentCreateView(
    LoginRequiredMixin,
    CommentSuccessUrlMixin,
    CreateView
):
    form_class = CommentForm
    model = Comment

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post,
            id=self.kwargs['post_id']
        )
        return super().form_valid(form)


class CommentUpdateView(
    LoginRequiredMixin,
    CommentSuccessUrlMixin,
    OnlyAuthorMixin,
    UpdateView
):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class CommentDeleteView(
    LoginRequiredMixin,
    CommentSuccessUrlMixin,
    OnlyAuthorMixin,
    DeleteView
):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'
