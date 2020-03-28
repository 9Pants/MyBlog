from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Post

class BlogListView(ListView):
    model=Post
    template_name='blog.html'
    login_url='account_login'

class BlogDetailView(DetailView):
    model=Post
    template_name='post_detail.html'
    login_url='account_login'

class BlogCreateView(LoginRequiredMixin, CreateView):
    model=Post
    template_name='post_new.html'
    fields=['title','body']
    login_url='account_login'

    def form_valid(self, form):
        print(self.request.user)
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model=Post
    template_name='post_edit.html'
    fields=['title','body']
    login_url='account_login'

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model=Post
    template_name='post_delete.html'
    success_url=reverse_lazy('post')
    login_url='account_login'