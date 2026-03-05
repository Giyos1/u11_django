from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models.query_utils import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from accounts.models import RoleChoice
# from django.contrib.auth.decorators import user_passes_test

# from accounts.utils import poster_
from post.forms import PostForms
from post.models import Post
from django.contrib.auth.decorators import permission_required


class PostListView(ListView):
    model = Post
    template_name = 'post/list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        search = self.request.GET.get(
            'search', '')

        posts = Post.objects.all()
        if self.request.user.is_authenticated:
            if self.request.user.role == RoleChoice.POSTER:
                posts = posts.filter(author=self.request.user)

        if search:
            posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))

        return posts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['search'] = \
            self.request.GET.get('search', '')
        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'post/create.html'
    form_class = PostForms
    extra_context = {
        'forms': PostForms,
    }
    permission_required = 'post.add_post'
    success_url = reverse_lazy('post:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(
    PermissionRequiredMixin,
    UpdateView
):
    model = Post
    form_class = PostForms
    template_name = 'post/update.html'
    success_url = reverse_lazy('post:list')
    permission_required = 'post.change_post'
    pk_url_kwarg = 'id'


class PostDeleteView(
    PermissionRequiredMixin,
    DeleteView
):
    model = Post
    success_url = reverse_lazy('post:list')
    permission_required = 'post.delete_post'
    template_name = 'post/post_confirm_delete.html'
    pk_url_kwarg = 'id'


def post_list(request):
    search = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    posts = Post.objects.all()

    if request.user.is_authenticated:
        if request.user.role == RoleChoice.POSTER:
            posts = posts.filter(author=request.user)

    if search:
        posts = Post.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
    paginator = Paginator(posts, 2)
    posts = paginator.get_page(page)
    return render(request, 'post/list.html', {'posts': posts, 'search': search})


@permission_required('post.add_post', raise_exception=True)
# @user_passes_test(poster_)
def post_create(request):
    if request.method == 'POST':
        forms = PostForms(request.POST)
        if forms.is_valid():
            post = forms.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:list')
        return render(request, 'post/create.html', {'forms': forms})
    forms = PostForms()
    return render(request, 'post/create.html', {'forms': forms})


@permission_required('post.change_post')
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

@permission_required('post.delete_post', raise_exception=True)
def post_delete(request, id=None):
    Post.objects.filter(id=id).delete()
    return redirect('post:list')
