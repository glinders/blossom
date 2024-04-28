from django.urls import path
from . import views


# register our namespace
app_name = 'ccf'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]
