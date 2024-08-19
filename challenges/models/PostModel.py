from django.db import models
from UsersModel import Users
from . import ChallengesModel
class Post(models.Model):
    username = models.ForeignKey(Users, on_delete=models.CASCADE)
    challenge_id = models.ForeignKey(ChallengesModel, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    posted_date = models.DateField()
    post_content = models.TextField()