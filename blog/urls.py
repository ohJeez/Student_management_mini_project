from django.urls import path
from . import views

urlpatterns = [
    path('',                         views.BlogListView.as_view(),   name='blog-list'),
    path('new/',                     views.BlogCreateView.as_view(), name='blog-create'),
    path('my-posts/',                views.my_posts_view,            name='blog-my-posts'),
    path('<slug:slug>/',             views.BlogDetailView.as_view(), name='blog-detail'),
    path('<slug:slug>/edit/',        views.BlogUpdateView.as_view(), name='blog-edit'),
    path('<slug:slug>/delete/',      views.BlogDeleteView.as_view(), name='blog-delete'),
]
