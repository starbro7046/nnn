from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models.UsersModel import Users
from .models.ChallengesModel import Challenges

admin.site.register(Challenges)

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')