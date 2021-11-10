from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Group, Post, User


@login_required
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/index.html'
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user).all()
    count_user_posts = Post.objects.filter(author=user).all().count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = username
    template = 'posts/profile.html'
    context = {
        'user': user,
        'count_user_posts': count_user_posts,
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, username=post.author)
    count = Post.objects.filter(author_id=user).all().count()
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'count': count,
    }
    return render(request, template, context)
