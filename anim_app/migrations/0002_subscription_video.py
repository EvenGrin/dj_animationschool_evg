# Generated by Django 5.1.7 on 2025-03-17 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anim_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='anim_app.video', verbose_name='Видео'),
        ),
    ]
