from django.db import models

class Bookmark(models.Model):
    username = models.ForeignKey(Users, on_delete=models.CASCADE)
    challenge_id = models.ForeignKey(Challenges, on_delete=models.CASCADE)
