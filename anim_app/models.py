from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class User(AbstractUser):
    surname = models.CharField(max_length=20, verbose_name="Фамилия")
    name = models.CharField(max_length=20, verbose_name="Имя")
    patronymic = models.CharField(max_length=20, verbose_name="Отчество")

    def __str__(self):
        return self.username

# Модель для хранения информации о категориях видео
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")



    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


# Общая модель для хранения информации о любых видео
class Video(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    description = models.TextField(verbose_name="Описание")
    duration = models.DurationField(verbose_name="Продолжительность")  # Продолжительность видео
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='videos', verbose_name="Категория")
    video_file = models.FileField(upload_to='videos/%Y/%m/%d/', verbose_name="Видео файл")
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/%d/', verbose_name="Обложка видео", blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_videos', blank=True, verbose_name="Нравится")
    dislikes = models.ManyToManyField(User, related_name='disliked_videos', blank=True, verbose_name="Не нравится")

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def get_absolute_url(self):
        return reverse('video_detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def average_rating(self):
        return (self.total_likes() - self.total_dislikes()) / (self.total_likes() + self.total_dislikes())

    def __str__(self):
        return self.name


# Модель для хранения информации о комментариях к видео
class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments', verbose_name="Видео")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'Коментарий у {self.user.username}'


# Модель для управления плейлистами
class Playlist(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название плейлиста")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists', verbose_name="Владелец")
    videos = models.ManyToManyField(Video, related_name='playlists', verbose_name="Видео")
    is_public = models.BooleanField(default=True, verbose_name="Открытый плейлист")

    class Meta:
        verbose_name = "Плейлист"
        verbose_name_plural = "Плейлисты"

    def __str__(self):
        return self.name


# Модель для управления подписками пользователей на категории и видео
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Категория")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Видео")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        if self.category:
            return f'Подписка на категорию: {self.category.name}'
        elif self.video:
            return f'Подписка на видео: {self.video.name}'


# Новая модель для отслеживания истории просмотров видео
class ViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="Видео")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время просмотра")

    class Meta:
        verbose_name = "История просмотров"
        verbose_name_plural = "Истории просмотров"

    def __str__(self):
        return f'{self.user.username} просмотрел {self.video.name} в {self.timestamp}'