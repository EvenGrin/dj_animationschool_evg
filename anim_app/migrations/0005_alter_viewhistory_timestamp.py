# Generated by Django 3.2.25 on 2025-03-19 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anim_app', '0004_auto_20250319_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewhistory',
            name='timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='Время просмотра'),
        ),
    ]
