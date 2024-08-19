from django.db import models
from . import UsersModel
class Login(models.Model):
    username = models.ForeignKey(Users, on_delete=models.CASCADE)
    email = models.EmailField()
    password = models.CharField(max_length=15)