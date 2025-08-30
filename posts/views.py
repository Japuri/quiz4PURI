from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    login_url = 'auth:signin'
    ordering = ['-created_at']

class PostDetailSlugView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:post-list')
    login_url = 'auth:signin'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied("You don't have permission to delete this post.")
        return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_update.html'
    login_url = 'auth:signin'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        if obj.user != self.request.user:
            raise PermissionDenied("You can't edit this post.")
        return obj

    def get_success_url(self):
        return self.object.get_absolute_url()

class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/post_create.html'
    success_url = reverse_lazy('posts:post-list')
    login_url = 'auth:signin'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
