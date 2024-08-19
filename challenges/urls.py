from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'challenge'

urlpatterns = [
    path('test', views.test, name='test'),
    path('users/signup/', views.signup_view, name='signup_page'),  # 회원가입
    path('users/login/', views.login_view, name='login_page'),  # 로그인
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 토큰
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/logout/', views.logout_view, name='logout'),  # 로그아웃
    path('users/<str:username>/', views.delete_account_view, name='delete_account'),  # 회원탈퇴
    # path('show/',views.show,name="Show")
    path('', views.challenge_list),
    path('create/', views.challenge_create, name='create_challenge'),
    path('<int:challenge_id>/', views.challenge_detail, name='challenge_detail')
]