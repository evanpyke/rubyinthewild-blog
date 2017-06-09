
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from .forms import PostForm, CommentForm
from .models import Post, Comment, Category
from .instagram_widget import *


# Create your views here.
def post_list(request):
    post_list = Post.objects.filter(
        published_date__lte=timezone.now()
        ).order_by('-published_date')

    category_list = Category.objects.all()

    inst = Instagram(instagram_url)

    category_btn = request.GET.get('category')
    if category_btn:
        post_list = post_list.filter(
            category__name__icontains=category_btn
        ).distinct()

    item_btn = request.GET.get('item')
    if item_btn:
        post_list = post_list.filter(
            Q(post_type__name__icontains='review') &
            Q(gear__short_name__icontains=item_btn)
        ).distinct()

    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(author__username__icontains=query) |
            Q(category__name__icontains=query) |
            Q(post_type__name__icontains=query)
        ).distinct()

    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(request, 'blog/post_list.html', {'posts': posts, 'category': category_list, 'instagram': inst})

def search_posts(request):
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(author__username__icontains=query) |
            Q(category__name__icontains=query) |
            Q(post_type__name__icontains=query)
        ).distinct()
    return post_list

def post_detail(request, post_type=None, slug=None):
    post = get_object_or_404(Post, post_type=post_type, slug=slug)
    if post.published_date == None and not request.user.is_staff:
        raise Http404

    query = request.GET.get('item')
    if query:
        print(query)
        return redirect('/')

    return render(request, 'blog/post_detail.html', {'post': post,})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            if 'save' in request.POST:
                post.publish(False)
            if 'publish' in request.POST:
                post.publish(True)
            return redirect('post:detail', post_type=post.post_type, slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            if 'save' in request.POST:
                post.publish(False)
            if 'publish' in request.POST:
                post.publish(True)

            return redirect('post:detail', post_type=post.post_type, slug=slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    post.publish(True)
    return redirect('post:detail', post_type=post.post_type, slug=slug)

@login_required
def post_remove(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post:list')

def add_comment_to_post(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post:detail', post_type=post.post_type, slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})