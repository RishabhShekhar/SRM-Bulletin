from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from News.models import Post, Comment
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from News.forms import PostForm, CommentForm, SubscriptionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)


# Create your views here.

class NotesView(TemplateView):
    template_name = 'News/notes.html'

class DashboardView(TemplateView):
    template_name = 'News/dashboard_new.html'

class ContactView(TemplateView):
    template_name = 'News/contact.html'

class WelcomeView(TemplateView):
    template_name = 'News/index.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post


class CreatePostView(CreateView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'News/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'News/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    success_url = reverse_lazy('post_list')


class DraftListView(ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'News/post_list.html'
    model = Post
    template_name = 'News/draft_list.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


def add_subscriber(request):

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.save()
            return redirect('post_list')
    else:
        form = SubscriptionForm()
        return render(request, 'News/subscription_form.html', {'form': form})


# ----------------------------------------------------------------------------------------------------

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    post.send_emails()
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
        return render(request, 'News/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
