from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy

from accounts.mixins import EditRequiredMixin, AdminRequiredMixin, ViewRequiredMixin
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm


# ── Blog List (all logged-in users) ──────────────────────────────────────────

class BlogListView(ViewRequiredMixin, ListView):
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        qs = Post.objects.select_related('author', 'category')

        # Staff/Admin see all; viewers only see published
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.can_edit():
            pass  # see everything including drafts
        else:
            qs = qs.filter(status=Post.STATUS_PUBLISHED)

        # Category filter
        cat_slug = self.request.GET.get('cat')
        if cat_slug:
            qs = qs.filter(category__slug=cat_slug)

        # Search
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(excerpt__icontains=q) |
                Q(body__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        ctx['current_cat'] = self.request.GET.get('cat', '')
        ctx['search_query'] = self.request.GET.get('q', '')
        ctx['total_posts'] = self.get_queryset().count()
        return ctx


# ── Blog Detail (all logged-in users, with comments) ──────────────────────────

class BlogDetailView(ViewRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        user = self.request.user
        # Viewers can only see published posts
        if post.status == Post.STATUS_DRAFT:
            if not (hasattr(user, 'profile') and user.profile.can_edit()):
                raise PermissionDenied
        return post

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = self.object.comments.filter(
            is_approved=True
        ).select_related('author')
        ctx['comment_form'] = CommentForm()
        ctx['related_posts'] = Post.objects.filter(
            status=Post.STATUS_PUBLISHED,
            category=self.object.category,
        ).exclude(pk=self.object.pk).select_related('author')[:3]
        return ctx

    def post(self, request, *args, **kwargs):
        """Handle comment submission."""
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, "💬 Comment posted!")
            return redirect('blog-detail', slug=self.object.slug)
        # If invalid, re-render with errors
        ctx = self.get_context_data()
        ctx['comment_form'] = form
        return render(request, self.template_name, ctx)


# ── Blog Create (admin + staff) ───────────────────────────────────────────────

class BlogCreateView(EditRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "✅ Post created successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Create'
        return ctx


# ── Blog Update (admin + staff, but only own posts unless admin) ───────────────

class BlogUpdateView(EditRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/blog_form.html'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        user = self.request.user
        # Staff can only edit their own posts; admin can edit any
        if not user.profile.is_admin() and post.author != user:
            raise PermissionDenied
        return post

    def form_valid(self, form):
        messages.success(self.request, "✅ Post updated successfully!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit'
        return ctx


# ── Blog Delete (admin only, or own post for staff) ───────────────────────────

class BlogDeleteView(EditRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog-list')
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        user = self.request.user
        if not user.profile.is_admin() and post.author != user:
            raise PermissionDenied
        return post

    def form_valid(self, form):
        messages.success(self.request, "🗑️ Post deleted.")
        return super().form_valid(form)


# ── Dashboard (my posts) – staff/admin ───────────────────────────────────────

@login_required
def my_posts_view(request):
    if not request.user.profile.can_edit():
        raise PermissionDenied
    posts = Post.objects.filter(author=request.user).select_related('category')
    return render(request, 'blog/my_posts.html', {'posts': posts})
