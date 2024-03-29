from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group
from models_portal.models import Post, Category, Subscribes, Author, StaffUser
from django.contrib.auth.models import User

from .filters import PostFilter
from .forms import PostForm

from datetime import datetime, date

from .tasks import email_sending

from django.core.cache import cache

from django.core.mail import EmailMultiAlternatives


class NewsList(ListView):
    model = Post
    template_name = 'post_list.html'
    ordering = 'pk'
    context_object_name = 'all_posts'
    paginate_by = 5
    queryset = Post.objects.filter(user_choice=Post.new)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['next_news'] = None
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(user_choice=Post.new)

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class NewsSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post'
    queryset = Post.objects.filter(user_choice=Post.new)

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.now()
        context['filterset'] = self.filterset
        return context


class NewCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'models_portal.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    queryset = Post.objects.filter(user_choice=Post.new)
    success_url = '/news/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user_choice = 'NE'

        today = date.today()
        post_limit = Post.objects.filter(author=post.author, creation_time_post__date=today).count()

        if post_limit >= 3:
            return render(self.request, 'post_limit.html', {'author': post.author})

        post.save()

        email_sending(post, form)

        return super().form_valid(form)


class NewUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'models_portal.change_post'
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'
    queryset = Post.objects.filter(user_choice=Post.new)


class NewDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'models_portal.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    context_object_name = 'post'
    queryset = Post.objects.filter(user_choice=Post.new)


class SendMailAdd(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'subscribe.html', {'categories': Category.objects.all()})

    def post(self, request, *args, **kwargs):
        category = Subscribes(category_id=request.POST['category'],
                              user_id=request.user.pk)

        category.save()
        return redirect('subscribe')


@login_required()
def authors_add(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        StaffUser.objects.create(user_id=user.pk)
        Author.objects.create(staff_user_id=len(StaffUser.objects.all()))
        author_group.user_set.add(user)
    return redirect('/news/')
