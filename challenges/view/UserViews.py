from django.contrib.auth import authenticate
from django.shortcuts import render
from django.conf import settings
from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password, check_password
import datetime
from config.utils.TokenUtil import TokenUtil
from ..models import *

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
import json

MOCK_USER_CREDENTIALS = {
    'username': 'testuser',
    'password': 'testpassword'
}


# 0.Test code-----------------------------------------------------------------------------------------------------
def test(request: HttpRequest) -> HttpResponse:
    return HttpResponse(str(request.GET.items()))


# 1. user signup,login,logout,delete ------------------------------------------------------------------------------

# CSRF 토큰을 포함한 페이지를 반환하여 Postman 등의 도구에서 사용할 수 있게 함
def csrf_token_view(request: HttpRequest) -> JsonResponse:
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


# 1-1. 회원가입

@permission_classes([AllowAny])
def signup_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            # 사용자 생성 후 JWT 발급

            user=Users.objects.filter(username=username).first();
            if(user is None):
                return JsonResponse({
                    'message': '닌망했어',
                    'access_token': 'ㅁㄴㄹㄴㅁㄹ',
                    'refresh_token': 'ㅁㄴㄹㄻㄴ'
                }, status=4444)
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            refresh_token = str(token)

            return JsonResponse({
                'message': f'회원가입 성공 {username},{password},{email}, ',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': '잘못된 JSON 형식입니다.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    # elif request.method == 'GET':
    #     return render(request, 'challenge/signup.html')


# 1-2. 로그인
# @csrf_exempt
def login_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': '모든 필드를 입력해야 합니다.'}, status=400)
            # Authenticate user


            # JWT 토큰 발급
            user = Users.objects.filter(username=username).first();
            if (user is None):
                return JsonResponse({
                    'message': '닌망했어',
                    'access_token': 'ㅁㄴㄹㄴㅁㄹ',
                    'refresh_token': 'ㅁㄴㄹㄻㄴ'
                }, status=4444)
            token = TokenObtainPairSerializer.get_token(user)
            access_token = str(token.access_token)
            refresh_token = str(token)

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


# 1-3. 로그아웃

@csrf_exempt
def logout_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        try:

            # 요청 헤더에서 토큰 가져오기
            token = request.headers.get('Authorization').split()[1]
            at=AccessToken(token)
            b=at['username']
            print(b)
            #RefreshToken(token).blacklist()
            return JsonResponse({'message': 'Logged out successfully'})
        except (IndexError, TokenError):
            return JsonResponse({'error': 'Invalid token'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



# 1-4. 회원탈퇴
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_account_view(request, username):
    try:
        # print(f"Current user: {request.user.username}")  # 로그에 현재 사용자 정보 출력
        # 현재 요청한 사용자
        current_user = request.user
        # 삭제할 사용자 찾기
        # 현재 사용자가 본인 또는 관리자일 때만 삭제 가능


        return JsonResponse({'message': '회원 탈퇴 성공'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 1-5. 비밀번호 변경 (인증없이 새 비밀번호 변경)
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def change_password_view(request: HttpRequest) -> JsonResponse:
    try:
        user = request.user
        data = json.loads(request.body)

        # 현재 비밀번호, 새 비밀번호 입력받음
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        # 입력하지 않으면 에러
        if not current_password or not new_password:
            return JsonResponse({'error': '현재 비밀번호와 새 비밀번호를 모두 입력해야 합니다.'}, status=400)

        # 현재 비밀번호 확인
        if not user.check_password(current_password):
            return JsonResponse({'error': '현재 비밀번호가 올바르지 않습니다.'}, status=400)

        # 새 비밀번호 설정
        user.set_password(new_password)
        user.save()

        return JsonResponse({'message': '비밀번호가 성공적으로 변경되었습니다.'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': '잘못된 JSON 형식입니다.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 1-6. 아이디 찾기
@api_view(['POST'])
@permission_classes([AllowAny])
def find_username_view(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
        email = data.get('email')

        if not email:
            return JsonResponse({'error': '이메일을 입력해야 합니다.'}, status=400)

        # 이메일로 사용자 찾기
        user = Users.objects.filter(email=email).first()

        if user is None:
            return JsonResponse({'error': '해당 이메일로 등록된 사용자를 찾을 수 없습니다.'}, status=404)

        return JsonResponse({'message': '아이디 찾기 성공', 'username': user.username}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': '잘못된 JSON 형식입니다.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# 1-7. 비밀번호찾기,변경

import random  # 랜덤비밀번호
import string
from django.core.mail import send_mail


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_view(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
        email = data.get('email')

        if not email:
            return JsonResponse({'error': '이메일을 입력해야 합니다.'}, status=400)

        # 이메일로 사용자 찾기
        user = Users.objects.filter(email=email).first()

        if user is None:
            return JsonResponse({'error': '해당 이메일로 등록된 사용자를 찾을 수 없습니다.'}, status=404)

        # 임시 비밀번호 생성
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user.set_password(temp_password)
        user.save()

        # 임시 비밀번호를 이메일로 전송
        send_mail(
            '비밀번호 재설정',
            f'임시 비밀번호는 {temp_password}입니다. 로그인 후 비밀번호를 변경해주세요.',
            'from@gmail.com',  # 발신자 이메일  (어떤 이메일로 보내는지?)
            [email],
            fail_silently=False,
        )

        return JsonResponse({'message': '임시 비밀번호가 이메일로 전송되었습니다.'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': '잘못된 JSON 형식입니다.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
