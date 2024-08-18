from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'challenge'

urlpatterns = [
    path('', views.challenge_list),
    path('create/', views.challenge_create, name='create_challenge'),
    path('<int:challenge_id>/', views.challenge_detail, name='challenge_detail')
]