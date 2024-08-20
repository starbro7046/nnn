from django.urls import path
from ..view import UserViews as views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('test', views.test, name='test'),
    path('signup/', views.signup_view, name='signup_page'),  # 회원가입
    path('login/', views.login_view, name='login_page'),  # 로그인
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 토큰
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.logout_view, name='logout'),  # 로그아웃
    path('delete/<str:username>/', views.delete_account_view, name='delete_account'),  # 회원탈퇴
    path('changepwd/', views.change_password_view, name='change_password'),  #비밀번호 변경
    path('findname/', views.find_username_view, name='findname'),  #아이디찾기
    path('resetpwd/', views.reset_password_view, name='resetpwd'),   #비밀번호찾기,변경(이메일로 랜덤비밀번호발송)
]