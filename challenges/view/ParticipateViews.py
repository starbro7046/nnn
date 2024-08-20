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

#챌린지 참가 버튼

@api_view(['POST'])
@permission_classes([IsAuthenticated])  #로그인한사용자만
def participate_in_challenge(request, challenge_id):
    try:
        data = request.data
        challenge_id = data.get('challenge_id')

        # 챌린지
        challenge = challenge_id

        # 현재 사용자
        user = request.user

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
            # images = data.get('images', [])
            # video = data.get('video', {})
            # audio = data.get('audio', {})

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
                posted_date=parse_date(request.POST.get('posted_date', None)),  # 날짜는 요청에서 제공될 경우
                post_content=post_content
            )

            # # 이미지 저장
            # for img in images:
            #     Images.objects.create(
            #         post_id=post,
            #         image_url=img.get('key')
            #     )
            #
            # # 비디오 저장
            # if video:
            #     Videos.objects.create(
            #         post_id=post,
            #         video_url=video.get('key')
            #     )
            #
            # # 오디오 저장
            # if audio:
            #     Audio.objects.create(
            #         post_id=post,
            #         audio_url=audio.get('key')
            #     )

            return JsonResponse({'message': 'Post created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
