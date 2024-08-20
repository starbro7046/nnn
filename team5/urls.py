
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('api/users/', include('challenges.urls.UserUrls')),
    path('api/challenges/', include('challenges.urls.ChallengeUrls')),
    path('api/participant/', include('challenges.urls.ParticipateUrls')),
    path('api/like/', include('challenges.urls.LikeUrls')),
    path('admin/',admin.site.urls)

]
