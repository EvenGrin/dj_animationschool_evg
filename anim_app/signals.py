from datetime import timedelta
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import moviepy as mp

from anim_app.models import Video

print('файл сигналы')

@receiver(pre_save, sender=Video)
def cache_old_video_file(sender, instance, **kwargs):
    print('получение старого видео')
    instance._old_video_file = ''
    try:
        if instance.pk:
            old_video = sender.objects.get(pk=instance.pk)
            instance._old_video_file = old_video.video_file
    except sender.DoesNotExist:
        pass



@receiver(post_save, sender=Video)
def update_video_duration(sender, instance, created, **kwargs):
    print('обновление продолжительности видео')
    print(instance.duration)
    if created or not instance.duration or instance._old_video_file != instance.video_file:
        try:
            clip = mp.VideoFileClip(instance.video_file.path)
            duration_in_seconds = round(clip.duration)
            instance.duration = timedelta(seconds=duration_in_seconds)
            if instance._old_video_file:
                print('Старое видео:',instance._old_video_file)
            else:
                print('Старого видео нет')
            print('Старое новое:', instance.video_file)
            instance.save(update_fields=['duration'])
            if instance._old_video_file:
                instance._old_video_file.delete(save=False)
        except Exception as e:
            # Логирование ошибки, если что-то пошло не так
            print(f'Ошибка при извлечении длительности видео: {e}')