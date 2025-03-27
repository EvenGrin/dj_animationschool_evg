# Generated by Django 3.2.25 on 2025-03-26 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anim_app', '0011_auto_20250326_1020'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_at'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='videos', to='anim_app.Category', verbose_name='Категория'),
        ),
    ]
