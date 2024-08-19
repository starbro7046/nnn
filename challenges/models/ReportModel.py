
from django.db import models
class Report(models.Model):
    report_username = models.ForeignKey(Users, on_delete=models.CASCADE)
    report_post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    report_reason = models.TextField()
