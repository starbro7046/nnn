from django.db import models
import self

class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=30)

    def __str__(self):
        return self.username

class Login(models.Model):
    username = models.ForeignKey(Users, on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField(max_length=15)

