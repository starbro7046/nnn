from django.urls import path
from ..view import UserViews
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('test', UserViews.test, name='test'),
    path('users/signup/', UserViews.signup_view, name='signup_page'),  # 회원가입
    path('users/login/', UserViews.login_view, name='login_page'),  # 로그인
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 토큰
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/logout/', UserViews.logout_view, name='logout'),  # 로그아웃
    path('users/<str:username>/', UserViews.delete_account_view, name='delete_account'),  # 회원탈퇴
]