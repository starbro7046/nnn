from django.db import models
from . import UsersModel
from . import PostModel
class Report(models.Model):
    report_username = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    report_post_id = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    report_reason = models.TextField()
