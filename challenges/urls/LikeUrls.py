from django.urls import path
from ..view import LikeViews as views

urlpatterns = [
    path('<int:post_id>/', views.like_post, name='like_post') #좋아요
]