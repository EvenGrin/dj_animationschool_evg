from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Video, Comment, Playlist, Subscription, ViewHistory
from moviepy import VideoFileClip
# Регистрация моделей в административной панели
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ['duration']
    list_display = ['thumbnail_tag', 'name', 'description', 'duration', 'date_published', 'category']
    search_fields = ['name', 'description']
    list_filter = ['date_published', 'category']
    fields = ['name', 'description', "category", 'duration', 'video_file', 'thumbnail']

    def thumbnail_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.thumbnail.url))


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['video', 'user', 'created_at']
    list_filter = ['created_at']


class VideoInlines(admin.TabularInline):
    model = Playlist.videos.through
    extra = 0

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'is_public']
    list_filter = ['is_public']
    fields = ['name', 'owner', 'is_public']
    inlines = [VideoInlines]

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'video']

@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'timestamp']
    list_filter = ['timestamp']
