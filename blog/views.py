from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog
from blog.services import get_blog_from_cache


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')
    login_url = reverse_lazy('users:login')


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    login_url = reverse_lazy('users:login')

    def get_queryset(self):
        return get_blog_from_cache()


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
    login_url = reverse_lazy('users:login')

