import json
from lib2to3.fixes.fix_input import context

import humanize
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from moviepy import VideoFileClip
from django.utils.translation import gettext_lazy as _
from anim_app.forms import RegisterForm
from anim_app.models import Video, Comment, ViewHistory, Playlist

def create_comment(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        text = request.POST.get('comment')
        if text:
            comment = Comment.objects.create(video=video, user=request.user, text=text)
            comment.save()

            comment_data = {
                'id': comment.id,
                'text': comment.text,
                'user': str(comment.user),  # Здесь можно использовать другое представление пользователя
                'created_at': _(humanize.naturaltime(comment.created_at)) ,  # Преобразуем дату в ISO формат
            }
            return JsonResponse(comment_data)
    return HttpResponse()

def like_video(request, pk):

    if request.user.is_authenticated:

        print(Video.objects.get(pk=pk).likes.all())
        return JsonResponse({'is_auth':True})
    else:
        return JsonResponse({'is_auth': False})



# главная страница
def index(request):
    videos = Video.objects.all().order_by('-date_published')

    # for v in videos:
    #     video = VideoFileClip(v.video_file.url)

    context = {"videos": videos}
    return render(request, 'index.html', context=context)


def video_detail(request,pk, pk_list=0):
    video = get_object_or_404(Video, pk=pk)
    if request.user.is_authenticated:
        history = ViewHistory.objects.update_or_create(user=request.user, video=video)
        print(history)
    context = {
        'video': video,
        'video_list': Video.objects.all().order_by('-date_published'),
        "playlist": Playlist.objects.filter(pk=pk_list)
    }
    return render(request, 'video_detail.html', context=context)


# плейлисты
def playlist(request):
    playlists = Playlist.objects.all()
    context = {
        'playlists': playlists
    }
    return render(request, 'playlist.html', context=context)

# видео в плейлистах
def playlist_detail(request, pk):
    playlists = Playlist.objects.filter(pk=pk)
    context = {
        'playlists': playlists
    }
    return render(request, 'playlist_video.html', context=context)


# история просмотров
def user_history(request):
    pass

# история просмотров
def user_favourites(request):
    pass


# регистрация
def registration(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'registration/registration.html', context=context)
