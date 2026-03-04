from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display   = ('title', 'author', 'category', 'status', 'created_at', 'reading_time')
    list_filter    = ('status', 'category')
    search_fields  = ('title', 'body', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    date_hierarchy = 'created_at'
    actions        = ['publish_posts', 'draft_posts']

    def publish_posts(self, request, queryset):
        from django.utils import timezone
        queryset.filter(status=Post.STATUS_DRAFT).update(
            status=Post.STATUS_PUBLISHED,
            published_at=timezone.now(),
        )
    publish_posts.short_description = "Publish selected posts"

    def draft_posts(self, request, queryset):
        queryset.update(status=Post.STATUS_DRAFT)
    draft_posts.short_description = "Move selected posts to Draft"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('author', 'post', 'created_at', 'is_approved')
    list_filter   = ('is_approved',)
    search_fields = ('author__username', 'body', 'post__title')
    actions       = ['approve', 'unapprove']

    def approve(self, request, queryset):
        queryset.update(is_approved=True)
    approve.short_description = "Approve selected comments"

    def unapprove(self, request, queryset):
        queryset.update(is_approved=False)
    unapprove.short_description = "Unapprove selected comments"
