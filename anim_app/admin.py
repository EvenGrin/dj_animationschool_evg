from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Video, Comment, Playlist, Subscription, ViewHistory, User
from moviepy import VideoFileClip


# Регистрация моделей в административной панели
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['thumbnail_tag', 'name', 'duration', 'date_published', 'category_list', 'total_likes',
                    'total_dislikes', 'average_rating', 'view_count']
    search_fields = ['name', 'description']
    list_filter = ['date_published', 'category']
    fields = ['name', 'description', "category", 'duration', 'video_file', 'thumbnail', 'video_tag']
    readonly_fields = ['duration', 'video_tag']
    filter_horizontal = ['category', ]
    list_per_page = 5

    def total_likes(self, obj):
        return obj.total_likes()

    total_likes.short_description = 'Количество лайков'

    def total_dislikes(self, obj):
        return obj.total_dislikes()

    total_dislikes.short_description = 'Количество дизлайков'

    def average_rating(self, obj):
        return obj.average_rating()

    average_rating.short_description = "средний показатель"

    def view_count(self, obj):
        return obj.view_count()

    view_count.short_description = "количество просмотров"

    def category_list(self, obj):
        return format_html(",</br>".join([category.name for category in obj.category.all()]))

    category_list.short_description = 'Категория'

    def video_tag(self, obj):
        return format_html(f"""
        <video 
        style="max-width: 100%;"
        class='bg-dark' 
        poster='{obj.thumbnail.url}'
        autoplay='autoplay' 
        loop='loop' 
        controls='controls' 
        tabindex='0'>
        <source src="/stream/{obj.pk}/" type="video/mp4">
        <source src="/stream/{obj.pk}/" type="video/webm">
        Ваш браузер не поддерживает воспроизведение видео.
        </video>
        """)

    video_tag.short_description = 'Видео'

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html(f'<img src="{obj.thumbnail.url}" style="max-width:200px; max-height:200px"/>')
        else:
            return 'нет превьюшки'

    thumbnail_tag.short_description = 'Обложка видео'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['video', 'text', 'user', 'created_at']
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




@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'timestamp']
    list_filter = ['timestamp']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'surname','name','patronymic', 'email']