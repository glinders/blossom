from django.urls import path
from . import views


# register our namespace
app_name = 'ccf'

urlpatterns = [
    # home page; lists all clients
    path(
        '',
        views.ClientListView.as_view(
            extra_context={'title': 'Home'},
        ),
        name='home',
    ),
    # user page; lists all clients of a user
    path(
        'user/<str:username>/',
        views.UserClientListView.as_view(
            extra_context={'title': 'Clients'},
        ),
        name='user-clients',
    ),
    # page to view single client
    path(
        'client/<int:pk>/detail/<int:tab>/',
        views.ClientDetailView.as_view(
            extra_context={'title': 'Client Detail'},
        ),
        name='client-detail',
    ),
    # page to create a client
    path(
        'client/new/',
        views.ClientCreateView.as_view(

            extra_context={
                'title': 'New Client',
                'action': 'Add',
            },
        ),
        name='client-create',
    ),
    # page to update a client
    path(
        'client/<int:pk>/update/',
        views.ClientUpdateView.as_view(
            extra_context={
                'title': 'Client Update',
                'action': 'Update',
            },
        ),
        name='client-update',
    ),
    # page to delete a client
    path(
        'client/<int:pk>/delete/',
        views.ClientDeleteView.as_view(
            extra_context={'title': 'Client Delete'},
        ),
        name='client-delete',
    ),
    # page to update medical details of a client
    path(
        'client/<int:pk>/medical/update/',
        views.MedicalUpdateView.as_view(
            extra_context={
                'title': 'Medical Update',
                'action': 'Update',
            },
        ),
        name='medical-update',
    ),
    # about page
    path(
        'about/',
        views.about,
        name='about',
    ),
]
