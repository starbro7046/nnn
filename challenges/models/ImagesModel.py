from django.db import models


class Images(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.TextField()