from django.urls import path
from . import views


# register our namespace
app_name = 'ccf'

urlpatterns = [
    # home page; lists all clients
    path(
        '',
        views.ClientListView.as_view(),
        name='home',
    ),
    # user page; lists all clients of a user
    path(
        'user/<str:username>/',
        views.UserClientListView.as_view(),
        name='user-clients',
    ),
    # page to view single client
    path(
        'client/<int:pk>/',
        views.ClientDetailView.as_view(),
        name='client-detail',
    ),
    # page to create a client
    path(
        'client/new/',
        views.ClientCreateView.as_view(),
        name='client-create',
    ),
    # page to update a client
    path(
        'client/<int:pk>/update/',
        views.ClientUpdateView.as_view(),
        name='client-update',
    ),
    # page to delete a client
    path(
        'client/<int:pk>/delete/',
        views.ClientDeleteView.as_view(),
        name='client-delete',
    ),
    # about page
    path(
        'about/',
        views.about,
        name='about',
    ),
]
