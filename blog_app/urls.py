from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('post/<str:pk>', views.post, name='post'),
    path('auth/login', views.login, name='login'),
    path('auth/create', views.create, name='create'),
    path('auth/logout', views.logout, name='logout'),
    path('search', views.search, name='search'),
]
