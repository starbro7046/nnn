from django.db import models

class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=30)


class Challenges(models.Model):
    board_option1 = 'LONG_TERM'
    board_option2 = 'SHORT_TERM'

    board_choices = [
        (board_option1, 'LONG_TERM'),
        (board_option2, 'SHORT_TERM'),
    ]

    challenge_title = models.CharField(max_length=100)
    duration = models.IntegerField(default=0)
    created_username = models.ForeignKey(Users, on_delete=models.CASCADE)
    challenge_content = models.TextField()
    board = models.CharField(max_length=20, choices=board_choices, default=board_option1)
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()



class Post(models.Model):
    username = models.ForeignKey(Users, on_delete=models.CASCADE)
    challenge_id = models.ForeignKey(Challenges, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    posted_date = models.DateField()
    post_content = models.TextField()


class Report(models.Model):
    report_username = models.ForeignKey(Users, on_delete=models.CASCADE)
    report_post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    report_reason = models.TextField()


class Bookmark(models.Model):
    username = models.ForeignKey(Users, on_delete=models.CASCADE)
    challenge_id = models.ForeignKey(Challenges, on_delete=models.CASCADE)


class Images(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.TextField()

class Videos(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    video_url = models.TextField()


class Audio(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    audio_url = models.TextField()


class Login(models.Model):
    username = models.ForeignKey(Users, on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField(max_length=15)