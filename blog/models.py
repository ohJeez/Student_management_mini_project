from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
import math


class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_DRAFT     = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES   = [
        (STATUS_DRAFT,     'Draft'),
        (STATUS_PUBLISHED, 'Published'),
    ]

    title      = models.CharField(max_length=200)
    slug       = models.SlugField(max_length=220, unique=True, blank=True)
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category   = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='posts')
    cover_color = models.CharField(
        max_length=7, default='#4f63d2',
        help_text='Hex colour used as the cover gradient base (e.g. #4f63d2)',
    )
    excerpt    = models.TextField(max_length=300, blank=True,
                                  help_text='Short summary shown on the list page.')
    body       = models.TextField()
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES,
                                  default=STATUS_DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    # ── helpers ──────────────────────────────────────────────────────────
    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        # Auto-set published_at on first publish
        if self.status == self.STATUS_PUBLISHED and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'slug': self.slug})

    @property
    def reading_time(self):
        """Estimate reading time in minutes (avg 200 words/min)."""
        word_count = len(self.body.split())
        minutes = math.ceil(word_count / 200)
        return max(1, minutes)

    @property
    def is_published(self):
        return self.status == self.STATUS_PUBLISHED


class Comment(models.Model):
    post    = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    body    = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on '{self.post.title}'"
