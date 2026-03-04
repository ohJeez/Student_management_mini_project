from django.urls import path
from . import views

urlpatterns = [
    # Root redirect
    path('', views.IndexRedirectView.as_view(), name='student-index'),

    # Student CRUD
    path('students/',                      views.StudentListView.as_view(),   name='student-list'),
    path('students/create/',               views.StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/',             views.StudentDetailView.as_view(), name='student-detail'),
    path('students/<int:pk>/edit/',        views.StudentUpdateView.as_view(), name='student-update'),
    path('students/<int:pk>/delete/',      views.StudentDeleteView.as_view(), name='student-delete'),

    # Feedback
    path('feedback/',                      views.FeedbackCreateView.as_view(), name='feedback-submit'),
    path('feedback/all/',                  views.FeedbackListView.as_view(),   name='feedback-list'),
    path('feedback/<int:pk>/toggle-read/', views.feedback_mark_read,           name='feedback-mark-read'),
]
