from django.urls import path
from ..view import ParticipateViews as views

#챌린지에 참가하기 (참가 버튼)
urlpatterns = [
    path('<int:challenge_id>/', views.participate_in_challenge, name='participate_in_challenge')
]