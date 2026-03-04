from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import CustomAuthForm

urlpatterns = [
    # Auth
    path('login/',
         auth_views.LoginView.as_view(
             template_name='accounts/login.html',
             authentication_form=CustomAuthForm,
         ),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # Admin user management
    path('users/',         views.user_list_view,   name='user-list'),
    path('users/create/',  views.register_view,    name='user-create'),
    path('users/<int:pk>/edit/',   views.user_edit_view,   name='user-edit'),
    path('users/<int:pk>/delete/', views.user_delete_view, name='user-delete'),
]
