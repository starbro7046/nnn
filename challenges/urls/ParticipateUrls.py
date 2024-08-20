from django.urls import path
from ..view import ParticipateViews as views

#챌린지에 참가하기 (참가 버튼)
urlpatterns = [
    path('<int:challenge_id>/', views.participate_in_challenge, name='participate_in_challenge'),
    path('<str:board>/<int:challenge_id>/attend', views.post_write, name='create_attendance_post'),
]
