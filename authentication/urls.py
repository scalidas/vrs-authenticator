from django.urls import path

from . import views

urlpatterns = [
    path('g_authenticate', views.g_authenticate, name='g_authenticate'),
]