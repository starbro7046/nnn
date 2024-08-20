from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=20)
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
    post_id = models.AutoField(primary_key=True)   #postid추가
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
    id = models.AutoField(primary_key=True)
    refresh_token = models.TextField()
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    expired_date = models.DateField()

#추가: 챌린지에 참가한 사람 정보
class ChallengeParticipation(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenges, on_delete=models.CASCADE)
    #joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'challenge')

#추가: 좋아요
class Like(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'  #목록표시 시