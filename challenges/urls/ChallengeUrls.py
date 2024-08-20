from django.urls import path
from ..view import ChallengeViews as views

urlpatterns = [
    path('', views.challenge_list),
    path('create/', views.challenge_create, name='create_challenge'),
    path('<str:board>/<int:challenge_id>/', views.challenge_detail, name='challenge_detail')
]
