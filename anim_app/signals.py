import os
import random
import shutil
from datetime import timedelta
from pathlib import Path

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import moviepy as mp
from moviepy import VideoFileClip

from anim_app.models import Video

print('файл сигналы')



@receiver(pre_save, sender=Video)
def cache_old_video_file(sender, instance, **kwargs):
    print(*('=' for i in range(50)))
    print('1) получение старого видео')
    instance._old_video_file = ''
    try:
        if instance.pk:
            old_video = sender.objects.get(pk=instance.pk)
            instance._old_video_file = old_video.video_file
    except sender.DoesNotExist:
        pass
    print(instance._old_video_file)

@receiver(post_save, sender=Video)
def update_video_duration(sender, instance, created, **kwargs):
    if created or not instance.duration or instance._old_video_file != instance.video_file:
        print(*('=' for i in range(50)))
        print('2) обновление продолжительности видео')
        try:
            clip = mp.VideoFileClip(instance.video_file.path)
            duration_in_seconds = round(clip.duration)
            instance.duration = timedelta(seconds=duration_in_seconds)
            if instance._old_video_file:
                print('Старое видео:', instance._old_video_file)
            else:
                print('Старого видео нет')
            print('Старое новое:', instance.video_file)
            instance.save(update_fields=['duration'])
            if instance._old_video_file:
                instance._old_video_file.delete(save=False)
        except Exception as e:
            # Логирование ошибки, если что-то пошло не так
            print(f'Ошибка при извлечении длительности видео: {e}')

        print('продолжительность', instance.duration)





@receiver(post_save, sender=Video)
def create_thumbnail(sender, instance, created, **kwargs):
    if not instance.thumbnail or not instance.thumbnail.path:
        print(*('=' for i in range(50)))
        print('3) создание превьюшки')
        # Получаем временный путь для миниатюры
        base_path = Path(instance.video_file.path).parent / 'thumbnails'
        base_path.mkdir(parents=True, exist_ok=True)
        thumbnail_path = base_path / f'thumbnail_{instance.pk}.jpg'

        try:
            # Открываем видео файл
            print('Открываем видео файл')
            clip = VideoFileClip(str(instance.video_file.path))

            # Извлекаем кадр на случайный кадр
            # middle_time = int(clip.duration / 2)
            middle_time=random.randint(1, int(clip.duration))
            print('Извлекаем кадр')
            frame = clip.get_frame(middle_time)
            # Преобразуем кадр в изображение
            from PIL import Image
            img = Image.fromarray(frame)

            # Сохраняем изображение в нужном формате
            img.save(thumbnail_path)

            # Сохраняем миниатюру в поле thumbnail
            instance.thumbnail.save(f'thumbnail_{instance.pk}.jpg', open(thumbnail_path, 'rb'))
            instance.save()
        except Exception as e:
            print(f'Ошибка при создании миниатюры: {e}')
        finally:
            # Удаление временной директории
            shutil.rmtree(base_path)



