from django.db import models
from . import PostModel

class Images(models.Model):
    post_id = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    image_url = models.TextField()