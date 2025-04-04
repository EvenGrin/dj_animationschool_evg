import json


from lib2to3.fixes.fix_input import context
from re import search

import humanize
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import comment
from moviepy import VideoFileClip
from django.utils.translation import gettext_lazy as _
from pyexpat.errors import messages

from anim_app.forms import RegisterForm
from anim_app.models import Video, Comment, ViewHistory, Playlist
from anim_app.services import open_file

search_video = Video.objects.all()


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
                'created_at': _(humanize.naturaltime(comment.created_at)) ,
            }
            return JsonResponse(comment_data)
    return HttpResponse()

def like_video(request, pk):
    video = Video.objects.get(pk=pk)
    message = False
    is_auth = False
    if request.user.is_authenticated:
        is_auth = True
        if request.user in video.likes.all():
            video.likes.remove(request.user)
            message = False
        else:
            # Ставим лайк
            video.likes.add(request.user)
            message = True
        if request.user in video.dislikes.all():
            video.dislikes.remove(request.user)

    data = {
        'total_likes': video.total_likes(),
        'total_dislikes': video.total_dislikes(),
        'is_auth': is_auth,
        'message': message
    }
    return JsonResponse(data)


def dislike_video(request, pk):
    video = Video.objects.get(pk=pk)
    message = False
    is_auth = False
    if request.user.is_authenticated:
        is_auth = True
        if request.user in video.dislikes.all():
            video.dislikes.remove(request.user)
            message = False
        else:
            video.dislikes.add(request.user)
            message = True
        if request.user in video.likes.all():
            video.likes.remove(request.user)

    data = {
        'total_likes': video.total_likes(),
        'total_dislikes': video.total_dislikes(),

        'is_auth': is_auth,
        'message': message
    }
    return JsonResponse(data)


def search_queryset(queryset, search_string):
    # Разделяем строку поиска на отдельные слова
    search_words = search_string.split()

    # Формируем сложный запрос с использованием оператора OR для каждого слова
    query = Q()
    for word in search_words:
        query |= Q(name__iregex=word)

    # Применяем сформированный запрос к queryset
    search_result = queryset.filter(query)

    return search_result


# главная страница
def index(request):
    context = {}
    search_query = request.GET.get('q')
    print(search_query)
    videos = Video.objects.all().order_by('-date_published')
    if search_query:
        videos = search_queryset(videos, search_query)

    context["videos"]= videos
    context["search_video"]= search_video
    context["search_query"]= search_query

    return render(request, 'index.html', context=context)


def video_detail(request,pk, pk_list=0):
    video = get_object_or_404(Video, pk=pk)
    if request.user.is_authenticated:
        history = ViewHistory.objects.update_or_create(user=request.user, video=video)
        print(history)
    context = {
        'video': video,
        'video_list': Video.objects.all().order_by('-date_published'),
        "playlist": Playlist.objects.filter(pk=pk_list),
        "search_video": search_video,
    }
    return render(request, 'video_detail.html', context=context)


# плейлисты
def playlist(request):
    playlists = Playlist.objects.all()
    context = {
        'playlists': playlists,
        "search_video": search_video,
    }
    return render(request, 'playlist.html', context=context)

# видео в плейлистах
def playlist_detail(request, pk):
    playlists = Playlist.objects.filter(pk=pk)
    context = {
        'playlists': playlists,
        "search_video": search_video,
    }
    return render(request, 'playlist_video.html', context=context)


# история просмотров
def user_history(request):
    context={
        "history": ViewHistory.objects.filter(user=request.user).order_by('-timestamp')
    }
    return render(request, 'history.html', context=context)

# история просмотров
def user_favourites(request):
    context={
        'favorites': Video.objects.all().filter(likes=request.user)
    }
    return render(request, 'favorites.html', context = context)


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
        'form': form,
        "search_video": search_video,
    }
    return render(request, 'registration/registration.html', context=context)


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response

def update_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get('comment_id')
        new_text = request.POST.get('new_text')

        try:
            comment = Comment.objects.get(pk=comment_id)
            if comment.user == request.user:  # Проверка прав на редактирование
                comment.text = new_text
                comment.save()
                return JsonResponse({'success': True, 'comment': {'id': comment.id, 'text': comment.text}}, safe=False)
        except Comment.DoesNotExist:
            pass

    return JsonResponse({'success': False})

def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
        if comment.user == request.user:  # Проверка прав на удаление
            comment.delete()
            return JsonResponse({'success': True})
    except Comment.DoesNotExist:
        pass

    return JsonResponse({'success': False}, status=400)