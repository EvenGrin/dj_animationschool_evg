# Generated by Django 3.2.25 on 2025-03-19 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anim_app', '0003_auto_20250318_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='duration',
            field=models.DurationField(blank=True, editable=False, null=True, verbose_name='Продолжительность видео'),
        ),
        migrations.AlterField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(upload_to='thumbnails/%Y/%m/%d/', verbose_name='Обложка видео'),
        ),
    ]
