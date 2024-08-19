from django.db import models
from . import PostModel

class Audio(models.Model):
    post_id = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    audio_url = models.TextField()