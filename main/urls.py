"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from anim_app import views

urlpatterns = [
    #
    path('favicon.ico', lambda _ : redirect('/static/media/logo/favicon.ico', permanent=True)),
    #
    path('admin/', admin.site.urls),
    #
    path('', views.index, name='home'),

    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path('playlist/', views.playlist, name='playlist'),
    path('playlist/<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:pk_list>/video/<int:pk>', views.video_detail, name='playlist_video' ),
    #
    path('accounts/', include("django.contrib.auth.urls")),
    # path('accounts/profile', ),
    path('accounts/history/', views.user_history, name='user_history'),
    path('accounts/favourites/', views.user_favourites, name='user_favourites'),
    path('accounts/registration', views.registration, name='registration'),
    #
    path('video/<int:pk>/create_comment/', views.create_comment, name='create_comment'),
    path('like_video/<int:pk>', views.like_video, name='like_video')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
