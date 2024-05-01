from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views


# register our namespace
app_name = 'users'

urlpatterns = [
    path(
        'register/',
        views.register,
        name='register',
    ),
    path(
        'profile/',
        views.profile,
        name='profile',
    ),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='users/login.html',
            extra_context={'title': 'Login'},
        ),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            template_name='users/logout.html',
            extra_context={'title': 'Logged Out'},
        ),
        name='logout',
    ),
]

# get correct location for media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)