from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from anim_app import views

urlpatterns = [
    #
    path('favicon.ico', lambda _: redirect('/static/media/logo/favicon.ico', permanent=True)),
    #
    path('admin/', admin.site.urls),
    #
    path('', views.index, name='home'),

    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path('playlist/', views.playlist, name='playlist'),
    path('playlist/<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:pk_list>/video/<int:pk>', views.video_detail, name='playlist_video'),
    #
    path('accounts/', include("django.contrib.auth.urls")),
    # path('accounts/profile', ),
    path('accounts/history/', views.user_history, name='user_history'),
    path('accounts/favourites/', views.user_favourites, name='user_favourites'),
    path('accounts/registration', views.registration, name='registration'),
    #
    path('video/<int:pk>/create_comment/', views.create_comment, name='create_comment'),
    path('update_comment/', views.update_comment, name='update_comment'),
    path('delete_comment/<int:pk>', views.delete_comment, name='delete_comment'),
    path('like_video/<int:pk>', views.like_video, name='like_video'),
    path('dislike_video/<int:pk>', views.dislike_video, name='dislike_video'),
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
