from ..models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..forms.ChallengeForm import challengeForm
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpRequest, HttpResponse
import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes




#챌린지 생성
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def challenge_create(request):
    if request.method == "POST":
        try:
            # JSON 데이터 파싱
            data = json.loads(request.body)


            # 필수 필드 추출
            board = data.get('board')
            challenge_title = data.get('challenge_title')
            challenge_content = data.get('challenge_content')
            duration_str = data.get('duration')
            images = data.get('images', [])

            duration = int(''.join(filter(str.isdigit, duration_str)))


            # 필수 필드 검증
            if not board or not challenge_title or not challenge_content:
                return JsonResponse({'status': 'error', 'message': '필수 필드가 누락되었습니다.'}, status=400)

            # 새로운 챌린지 인스턴스 생성
            challenge = Challenges(
                created_username=request.user,
                challenge_title=challenge_title,
                challenge_content=challenge_content,
                board='LONG_TERM' if board == '장기' else 'SHORT_TERM',
                created_date=timezone.now(),
                start_date=timezone.now().date(),

                end_date=timezone.now().date() + timezone.timedelta(days=duration), #duration 값을 int로 변환후 days = duration 해야함

                images = json.dumps(images)
            )


            # 챌린지 저장
            challenge.save()

            # 성공적인 응답 반환
            return JsonResponse({
                'message': '글 작성 성공',
                'challenge_id': challenge.id
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON 파싱 오류가 발생했습니다.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # POST 요청이 아닌 경우 오류 반환
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

#챌린지 목록 조회
def challenge_list(request, board):
    try:
        # 페이지와 사이즈 파라미터 가져오기
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))

        # 필터링할 board 값
        if board not in ['LONG_TERM', 'SHORT_TERM']:
            return JsonResponse({'error': 'Invalid board parameter'}, status=400)

        # 챌린지 목록 조회
        challenges = Challenges.objects.filter(board=board)

        # 페이징 처리
        paginator = Paginator(challenges, size)
        page_obj = paginator.get_page(page)

        # 결과를 JSON 형식으로 변환
        response_data = {
            'page': page_obj.number,
            'size': size,
            'totalPages': paginator.num_pages,
            'totalItems': paginator.count,
            'posts': [
                {
                    'challenge_id': challenge.id,
                    'challenge_title': challenge.challenge_title,
                    'created_username': challenge.created_username.username,
                }
                for challenge in page_obj.object_list
            ]
        }

        return JsonResponse(response_data, safe=False)

    except Exception as e:
        # 서버 오류 처리
        return JsonResponse({'error': str(e)}, status=500)


#챌린지 상세 조회
def challenge_detail(request, board, challenge_id):
    try:
        # challenge_id로 챌린지 객체 조회
        challenge = get_object_or_404(Challenges, board = board, id = challenge_id,)

        # 응답 데이터 생성
        response_data = {
            'challenge_id': challenge.id,
            'board': '장기' if challenge.board == 'LONG_TERM' else '단기',
            'challenge_title': challenge.challenge_title,
            'created_username': challenge.created_username.username,
            'created_date': challenge.created_date.isoformat(),  # ISO 형식의 날짜 문자열
            #'likes': 0,  # 좋아요 수를 추적하는 별도의 모델이 있을 경우, 여기서 가져와야 함
            'duration': f"{challenge.duration}일" if challenge.board == 'LONG_TERM' else "하루",
            'challenge_content': challenge.challenge_content,
            'images': challenge.images,
        }
        # JSON 응답 반환
        return JsonResponse(response_data, status=200)

    except Challenges.DoesNotExist:
        # 해당 챌린지 아이디를 가진 챌린지가 존재하지 않는 경우
        return JsonResponse({'status': 'error'}, status=404)

    except Exception as e:
        # 서버 오류
        return JsonResponse({'status': 'error', 'message' : str(e)}, status=500)


#챌린지 참가 버튼

#챌린지 인증글 작성

#챌린지에 참여한 다른 사람들의 인증글 확인




