from django.db import models


class Challenges(models.Model):
    board_option1 = '장기'
    board_option2 = '단기'

    board_choices = [
        (board_option1, '장기'),
        (board_option2, '단기'),
    ]

    challenge_title = models.CharField(max_length=100)
    created_username = models.ForeignKey(Users, on_delete=models.CASCADE)
    challenge_content = models.TextField()
    board = models.CharField(max_length=20, choices=board_choices, default=board_option1)
    created_date = models.DateTimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.challenge_title

    def __str__(self):
        return self.challenge_title





