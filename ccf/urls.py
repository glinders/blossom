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
    # page to view single client; this is a tabbed view
    # <int:tab> selects the tab to show
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
                'model': 'Client',
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
                'model': 'Client',
                'action': 'Update',
            },
        ),
        name='client-update',
    ),
    # page to delete a client
    path(
        'client/<int:pk>/delete/',
        views.ClientDeleteView.as_view(
            extra_context={
                'title': 'Client Delete',
                'model': 'Client',
                'name': 'display_name'
            },
        ),
        name='client-delete',
    ),
    # page to update medical details of a client
    path(
        'client/<int:pk>/medical/update/',
        views.MedicalUpdateView.as_view(
            extra_context={
                'title': 'Medical Update',
                'model': 'Medical',
                'action': 'Update',
            },
        ),
        name='medical-update',
    ),
    # page to create a note for a client
    path(
        'client/<int:client_id>/note/new/',
        views.NoteCreateView.as_view(
            extra_context={
                'title': 'New Note',
                'model': 'Note',
                'action': 'Add',
            },
        ),
        name='note-create',
    ),
    # page to update a note for a client
    path(
        'client/<int:client_id>/note/<int:pk>/update/',
        views.NoteUpdateView.as_view(
            extra_context={
                'title': 'Note Update',
                'model': 'Note',
                'action': 'Update',
            },
        ),
        name='note-update',
    ),
    # page to view a note for a client
    path(
        'client/<int:client_id>/note/<int:pk>/detail/',
        views.NoteDetailView.as_view(
            extra_context={'title': 'Note Detail'},
        ),
        name='note-detail',
    ),
    # page to delete a note
    path(
        'client/<int:client_id>/note/<int:pk>/delete/',
        views.NoteDeleteView.as_view(
            extra_context={
                'title': 'Note Delete',
                'model': 'Note',
                'name': 'title'
            },
        ),
        name='note-delete',
    ),
    # about page
    path(
        'about/',
        views.about,
        name='about',
    ),
]
