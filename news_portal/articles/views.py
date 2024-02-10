from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from models_portal.models import Post
from .forms import ArticleForm
from .filters import ArticleFilter
from datetime import datetime


class ArticleList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'all_posts'
    ordering = 'creation_time_post'
    paginate_by = 2
    queryset = Post.objects.filter(user_choice=Post.article)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        return context


class ArticleDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(user_choice=Post.article)


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'models_portal.add_post'
    form_class = ArticleForm
    model = Post
    template_name = 'post_create.html'
    queryset = Post.objects.filter(user_choice=Post.article)

    def form_valid(self, form):
        article = form.save(commit=False)
        article.user_choice = 'AR'
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'models_portal.change_post'
    form_class = ArticleForm
    model = Post
    template_name = 'post_create.html'
    queryset = Post.objects.filter(user_choice=Post.article)


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'models_portal.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_urls = reverse_lazy('article_list')
    context_object_name = 'post'
    queryset = Post.objects.filter(user_choice=Post.article)


class ArticleSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(user_choice=Post.article)

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticleFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['filterset'] = self.filterset
        return context
