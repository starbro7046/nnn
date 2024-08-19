from django.db import models
from . import UsersModel
from . import ChallengesModel
class Bookmark(models.Model):
    username = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    challenge_id = models.ForeignKey(ChallengesModel, on_delete=models.CASCADE)
