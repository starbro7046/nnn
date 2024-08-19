from django.db import models

class Audio(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    audio_url = models.TextField()