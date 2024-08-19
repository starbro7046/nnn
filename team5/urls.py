
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('users/', include('challenges.urls.UserUrls')),
    path('challenges/', include('challenges.urls.ChallengeUrls')),

]
