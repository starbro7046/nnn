from django.db import models

class Videos(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    video_url = models.TextField()