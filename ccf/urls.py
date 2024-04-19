from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='ccf-home'),
    path('about/', views.about, name='ccf-about'),
]
