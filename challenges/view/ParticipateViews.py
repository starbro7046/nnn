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


#챌린지 참가 버튼

@api_view(['POST'])
#@permission_classes([IsAuthenticated])  //로그인한사용자만
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


