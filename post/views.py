from django.db.models.query_utils import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from accounts.utils import login_required
from post.forms import PostForms
from post.models import Post


def post_list(request):
    search = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    posts = Post.objects.all()
    if search:
        posts = Post.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
    paginator = Paginator(posts, 2)
    posts = paginator.get_page(page)
    return render(request, 'post/list.html', {'posts': posts, 'search': search})


@login_required
def post_create(request):
    if request.method == 'POST':
        forms = PostForms(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('post:list')
        return render(request, 'post/create.html', {'forms': forms})
    forms = PostForms()
    return render(request, 'post/create.html', {'forms': forms})


def post_update(request, id=None):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        forms = PostForms(request.POST, instance=post)
        if forms.is_valid():
            forms.save()
            return redirect('post:list')
        return render(request, 'post/update.html', {'forms': forms})
    forms = PostForms(instance=post)
    return render(request, 'post/update.html', {'forms': forms})


@login_required
def post_delete(request, id=None):
    Post.objects.filter(id=id).delete()
    return redirect('post:list')
