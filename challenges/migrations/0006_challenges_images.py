# Generated by Django 5.1 on 2024-08-21 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0005_alter_audio_audio_url_alter_images_image_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenges',
            name='images',
            field=models.TextField(blank=True, null=True),
        ),
    ]
