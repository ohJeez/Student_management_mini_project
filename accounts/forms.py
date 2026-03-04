from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import UserProfile, ROLES


# ── Login form ────────────────────────────────────────────────────────────────

class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': ' ', 'id': 'id_username'})
        self.fields['password'].widget.attrs.update({'placeholder': ' ', 'id': 'id_password'})


# ── Registration form ─────────────────────────────────────────────────────────

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': ' '}))
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': ' '}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'placeholder': ' '}))
    role = forms.ChoiceField(choices=ROLES.CHOICES, initial=ROLES.VIEWER,
                             widget=forms.Select())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].widget.attrs.update({'placeholder': ' '})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # The signal creates the profile; we just update the role
            profile = user.profile
            profile.role = self.cleaned_data['role']
            profile.save()
        return user


# ── Edit-user form (admin only) ───────────────────────────────────────────────

class UserEditForm(forms.ModelForm):
    """Allow an admin to change username, email, names, and role."""
    role = forms.ChoiceField(choices=ROLES.CHOICES)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            try:
                self.fields['role'].initial = self.instance.profile.role
            except UserProfile.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data['role']
            profile.save()
        return user
