from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .forms import RegisterForm, UserEditForm
from .models import UserProfile
from .mixins import role_required


# ── Registration (admin-only) ─────────────────────────────────────────────────

@login_required
@role_required('admin')
def register_view(request):
    """Admin creates a new user and assigns their role."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('user-list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# ── User list (admin-only) ────────────────────────────────────────────────────

@login_required
@role_required('admin')
def user_list_view(request):
    users = User.objects.select_related('profile').order_by('username')
    return render(request, 'accounts/user_list.html', {'users': users})


# ── Edit user role (admin-only) ───────────────────────────────────────────────

@login_required
@role_required('admin')
def user_edit_view(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User '{target_user.username}' updated.")
            return redirect('user-list')
    else:
        form = UserEditForm(instance=target_user)
    return render(request, 'accounts/user_edit.html', {'form': form, 'target_user': target_user})


# ── Delete user (admin-only) ──────────────────────────────────────────────────

@login_required
@role_required('admin')
def user_delete_view(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    if target_user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('user-list')
    if request.method == 'POST':
        target_user.delete()
        messages.success(request, "User deleted.")
        return redirect('user-list')
    return render(request, 'accounts/user_confirm_delete.html', {'target_user': target_user})


# ── Profile view (any authenticated user) ────────────────────────────────────

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
