# Generated by Django 5.2 on 2025-05-12 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_postlike_post_remove_postlike_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='post',
            name='updated_at',
        ),
    ]
