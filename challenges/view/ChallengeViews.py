from ..models import *

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..forms.ChallengeForm import challengeForm

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



def challenge_list(request):
    challengelist = Challenges.objects.all()
    return render(request, 'challenges/challengeList.html', {'challengelist': challengelist})


def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Post, pk=challenge_id)
    return render(request, 'challenges/글열람.html', {'challenge': challenge})


