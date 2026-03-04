from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


# ── function-based decorator ───────────────────────────────────────────────────

def role_required(*roles):
    """Decorator for function-based views.
    Usage:  @role_required('admin', 'staff')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.conf import settings
                from django.shortcuts import redirect
                return redirect(settings.LOGIN_URL)
            profile = getattr(request.user, 'profile', None)
            if profile is None or profile.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# ── class-based view mixins ───────────────────────────────────────────────────

class RoleRequiredMixin(LoginRequiredMixin):
    """Base mixin: subclass and set `allowed_roles = ['admin', 'staff']`."""
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        # super() handles the login check; if it passed, check the role
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile is None or profile.role not in self.allowed_roles:
                raise PermissionDenied
        return response


class AdminRequiredMixin(RoleRequiredMixin):
    """Only admin role is allowed."""
    allowed_roles = ['admin']


class EditRequiredMixin(RoleRequiredMixin):
    """Admin and Staff may edit."""
    allowed_roles = ['admin', 'staff']


class ViewRequiredMixin(LoginRequiredMixin):
    """Any authenticated user (all roles) may view."""
    pass
