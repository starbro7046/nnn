
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('api/users/', include('challenges.urls.UserUrls')),
    path('api/challenges/', include('challenges.urls.ChallengeUrls')),
    path('admin/',admin.site.urls)

]
