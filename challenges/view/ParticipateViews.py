from ..models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..forms.ChallengeForm import challengeForm
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import ChallengeParticipation, Challenges
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.dateparse import parse_date
from datetime import datetime

#챌린지 참가 버튼

@api_view(['POST'])
@permission_classes([IsAuthenticated])  #로그인한사용자만
def participate_in_challenge(request, board, challenge_id):
    try:
        # 현재 사용자
        user = request.user

        data = json.loads(request.body)
        username = data.get('username')

        # 사용자 인스턴스 가져오기
        try:
            participant = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return Response({'status': 'error', 'message': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        #챌린지 인스턴스 가져오기
        try:
            challenge = Challenges.objects.get(id=challenge_id, board=board)
        except Challenges.DoesNotExist:
            return Response({'status': 'error', 'message': '챌린지를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 이미 참가한 챌린지인지 확인
        if ChallengeParticipation.objects.filter(user=user, challenge=challenge).exists():
            return Response({'status': 'error', 'message': '이미 참가한 챌린지입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 참가 기록 생성
        ChallengeParticipation.objects.create(user=user, challenge=challenge)

        return Response({'status': 'success', 'message': '챌린지에 참가했습니다.'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#챌린지 인증글 작성

#def post_write(request):
#    if request.method == "POST":
#        printf("post method입니다")    //글 작성


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_write(request, board, challenge_id):
    if request.method == 'POST':
        try:
            # 인증된 사용자 가져오기
            user = request.user

            # 요청 데이터 파싱
            data = json.loads(request.body)
            post_title = data.get('post_title')
            post_content = data.get('post_content')
            images = data.get('images', [])
            video = data.get('video', {})
            audio = data.get('audio', {})

            #현재 날짜와 시간 가져오기
            posted_date = datetime.now()

            # 챌린지 유효성 검사
            try:
                challenge = Challenges.objects.get(id=challenge_id, board=board)
            except Challenges.DoesNotExist:
                return JsonResponse({'error': 'Challenge not found'}, status=404)

            # 챌린지 참여 여부 확인
            if not ChallengeParticipation.objects.filter(user=user, challenge=challenge).exists():
                return JsonResponse({'error': 'User not participating in this challenge'}, status=403)

            # 인증글 생성
            post = Post.objects.create(
                username=user,
                challenge_id=challenge,
                post_title=post_title,
                posted_date=posted_date,  # 현재 날짜와 시간 저장
                post_content=post_content
            )

            # 이미지 저장
            for img_url in images:
                Images.objects.create(
                    post=post,
                    image_url=img_url
                )

            # 비디오 저장
            if video:
                Videos.objects.create(
                    post=post,
                    video_url=video.get('url')
                )

            # 오디오 저장
            if audio:
                Audio.objects.create(
                    post=post,
                    audio_url=audio.get('url')
                )

            return JsonResponse({'message': 'Post created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
