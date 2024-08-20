from ..models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..forms.ChallengeForm import challengeForm
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

#챌린지 생성
def challenge_create(request):
    if request.method == "POST":
        form = challengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.created_username = request.user
            challenge.created_date = timezone.now()
            challenge.save()  # DB에 적용

            # 방금 생성한 PK와 일치하는 챌린지의 상세페이지로 이동
            return redirect('challenge_detail', pk=challenge.pk)

    else:
        form = challengeForm()

    # 챌린지 생성 페이지
    return render(request, 'challenges/챌린지 생성 상세.html', {'form': form})


#챌린지 목록 조회

#챌린지 상세 조회

#챌린지 생성(장기)

#챌린지 생성(단기)

#챌린지 참가 버튼

#챌린지 인증글 작성

#챌린지에 참여한 다른 사람들의 인증글 확인


#챌린지 생성
def challenge_create(request):
    if request.method == "POST":
        try:
            # JSON 데이터 파싱
            data = json.loads(request.body)

            board = data.get('board')
            challenge_title = data.get('challenge_title')
            challenge_content = data.get('challenge_content')
            duration = data.get('duration')
            images = data.get('images', [])

            # 필수 필드가 없으면 오류 반환
            if not board or not challenge_title or not challenge_content:
                return JsonResponse({'status': 'error', 'message': '필수 필드가 누락되었습니다.'}, status=400)

            # 새로운 챌린지 인스턴스 생성
            challenge = Challenges(
                created_username=request.user,
                challenge_title=challenge_title,
                challenge_content=challenge_content,
                board='LONG_TERM' if board == '장기' else 'SHORT_TERM',
                created_date=timezone.now(),
            )

            # 장기 챌린지의 경우 duration 필드를 설정
            if challenge.board == 'LONG_TERM':
                try:
                    challenge.duration = int(duration.replace('일', ''))
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': '유효하지 않은 duration 값입니다.'}, status=400)

            # 챌린지 저장
            challenge.save()

            '''
            이미지 처리 방법 논의후 추가
            '''

            # 성공
            return JsonResponse({
                'message': '글 작성 성공',
                'challenge_id': challenge.id
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON 파싱 오류가 발생했습니다.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # POST 요청이 아닌 경우
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


#챌린지 목록 조회
def challenge_list(request):
    challengelist = Challenges.objects.all()
    return render(request, 'challenges/challengeList.html', {'challengelist': challengelist})

#챌린지 상세 조회

#챌린지 생성(장기)

#챌린지 생성(단기)

#챌린지 참가 버튼

#챌린지 인증글 작성

#챌린지에 참여한 다른 사람들의 인증글 확인






def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Post, pk=challenge_id)
    return render(request, 'challenges/글열람.html', {'challenge': challenge})


