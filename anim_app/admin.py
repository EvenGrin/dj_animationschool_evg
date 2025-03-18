from django.contrib import admin
from .models import Category, Video, Comment, Playlist, Subscription, ViewHistory

# Регистрация моделей в административной панели
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'duration', 'date_published', 'category']
    search_fields = ['name', 'description']
    list_filter = ['date_published', 'category']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['video', 'user', 'created_at']
    list_filter = ['created_at']

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'is_public']
    list_filter = ['is_public']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'video']

@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'timestamp']
    list_filter = ['timestamp']
