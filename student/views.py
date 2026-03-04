from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView,
    DeleteView, RedirectView, DetailView,
)
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from accounts.mixins import AdminRequiredMixin, EditRequiredMixin, ViewRequiredMixin
from .models import Student, Feedback
from .forms import StudentForm, FeedbackForm


class IndexRedirectView(RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'student-list'


class StudentListView(ViewRequiredMixin, ListView):
    """Any logged-in user may view the student list."""
    model = Student
    template_name = 'student/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        from django.db.models import Q
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)  |
                Q(email__icontains=q)      |
                Q(roll_number__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_query'] = self.request.GET.get('q', '').strip()
        ctx['total_count']  = self.get_queryset().count()
        return ctx


class StudentDetailView(ViewRequiredMixin, DetailView):
    """Any logged-in user may view student details."""
    model = Student
    template_name = 'student/student_detail.html'
    context_object_name = 'student'


class StudentCreateView(EditRequiredMixin, CreateView):
    """Admin and Staff may create students."""
    model = Student
    form_class = StudentForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Add'
        return ctx


class StudentUpdateView(EditRequiredMixin, UpdateView):
    """Admin and Staff may update students."""
    model = Student
    form_class = StudentForm
    template_name = 'student/student_form.html'
    success_url = reverse_lazy('student-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['action'] = 'Edit'
        return ctx


class StudentDeleteView(AdminRequiredMixin, DeleteView):
    """Only Admin may delete students."""
    model = Student
    template_name = 'student/student_confirm_delete.html'
    success_url = reverse_lazy('student-list')


# ── Feedback ──────────────────────────────────────────────────────────────────

class FeedbackCreateView(ViewRequiredMixin, CreateView):
    """Any logged-in user can submit feedback."""
    model = Feedback
    form_class = FeedbackForm
    template_name = 'student/feedback_form.html'
    success_url = reverse_lazy('feedback-submit')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "✅ Thank you! Your feedback has been submitted.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['my_feedbacks'] = Feedback.objects.filter(
            user=self.request.user
        ).order_by('-submitted_at')[:5]
        return ctx


class FeedbackListView(AdminRequiredMixin, ListView):
    """Admin-only: view all submitted feedback."""
    model = Feedback
    template_name = 'student/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 20

    def get_queryset(self):
        qs = Feedback.objects.select_related('user').order_by('-submitted_at')
        f = self.request.GET.get('filter')
        if f == 'unread':
            qs = qs.filter(is_read=False)
        elif f == 'read':
            qs = qs.filter(is_read=True)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['unread_count'] = Feedback.objects.filter(is_read=False).count()
        ctx['current_filter'] = self.request.GET.get('filter', 'all')
        return ctx


@login_required
def feedback_mark_read(request, pk):
    """Admin toggles a feedback item's read/unread status."""
    if not request.user.profile.is_admin():
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    fb = get_object_or_404(Feedback, pk=pk)
    fb.is_read = not fb.is_read
    fb.save()
    return redirect(request.META.get('HTTP_REFERER', 'feedback-list'))
