from django.urls import path
from . import views


# register our namespace
app_name = 'ccf'

urlpatterns = [
    # home page; lists all posts
    path(
        '',
        views.PostListView.as_view(),
        name='home',
    ),
    # page to view single post
    path(
        'post/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post-detail',
    ),
    # page to create a post
    path(
        'post/new/',
        views.PostCreateView.as_view(),
        name='post-create',
    ),
    # page to update a post
    path(
        'post/<int:pk>/update/',
        views.PostUpdateView.as_view(),
        name='post-update',
    ),
    # page to delete a post
    path(
        'post/<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='post-delete',
    ),
    # about page
    path(
        'about/',
        views.about,
        name='about',
    ),
]

# these contain the function based views
urlpatterns_unused = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]
