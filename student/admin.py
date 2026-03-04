from django.contrib import admin
from .models import Student, Feedback


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'roll_number', 'email')
    search_fields = ('first_name', 'last_name', 'roll_number', 'email')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'rating', 'submitted_at', 'is_read')
    list_filter = ('is_read', 'rating')
    search_fields = ('subject', 'message', 'user__username')
    readonly_fields = ('submitted_at',)
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected as unread"
