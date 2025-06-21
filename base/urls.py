from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello'),
    path('api/hello/', views.api_hello, name='api_hello'),
]