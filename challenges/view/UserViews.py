#from .models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpRequest, HttpResponse
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import json
# 0.Test code-----------------------------------------------------------------------------------------------------
def test(request: HttpRequest) -> HttpResponse:
    return HttpResponse(str(request.GET.items()))

#1. user signup,login,logout,delete ------------------------------------------------------------------------------

# CSRF 토큰을 포함한 페이지를 반환하여 Postman 등의 도구에서 사용할 수 있게 함
def csrf_token_view(request: HttpRequest) -> JsonResponse:
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

#1-1. 회원가입
@csrf_protect
@permission_classes([AllowAny])
def signup_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            if not username or not password or not email:
                return JsonResponse({'error': '모든 필드를 입력해야 합니다.'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': '이미 존재하는 사용자입니다.'}, status=409)

            user = User(username=username, password=make_password(password), email=email)
            user.save()

            # 사용자 생성 후 JWT 발급
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return JsonResponse({
                'message': '회원가입 성공',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 형식입니다.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'GET':
        return render(request, 'challenge/signup.html')


#1-2. 로그인
@csrf_protect
def login_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': '모든 필드를 입력해야 합니다.'}, status=400)

            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is None:
                return JsonResponse({'error': '사용자 인증 실패'}, status=401)

            # JWT 토큰 발급
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return JsonResponse({
                'message': '로그인 성공',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 형식입니다.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        return render(request, 'challenge/login.html')
    else:
        return JsonResponse({'error': '잘못된 요청'}, status=400)


#1-3. 로그아웃(확인해보지못함)
@api_view(['POST'])
def logout_view(request):
    try:
        # 클라이언트에서 전달된 refresh token 가져오기
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return JsonResponse({'error': 'Refresh token이 필요합니다.'}, status=400)

        # Refresh token을 블랙리스트에 추가
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return JsonResponse({'error': '유효하지 않은 토큰입니다.'}, status=400)

        return JsonResponse({'message': '로그아웃 성공'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#1-4. 회원탈퇴

@csrf_protect
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account_view(request, username):
    try:
        # 현재 요청한 사용자
        current_user = request.user
        # 삭제할 사용자 찾기
        user_to_delete = User.objects.filter(username=username).first()
        if not user_to_delete:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)
        # 현재 사용자가 본인 또는 관리자일 때만 삭제 가능
        if current_user.username != username and not current_user.is_superuser:
            return JsonResponse({'error': '권한이 없습니다.'}, status=403)
        # 사용자 삭제
        user_to_delete.delete()
        return JsonResponse({'message': '회원 탈퇴 성공'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)