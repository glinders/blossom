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
