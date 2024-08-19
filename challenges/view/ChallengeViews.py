from ..models.ChallengesModel import Challenges
from ..models.PostModel import Post
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from ..forms import ChallengeForm


def challenge_list(request):
    challengelist = Challenges.objects.all()
    return render(request, 'challenges/challengeList.html', {'challengelist': challengelist})


def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Post, pk=challenge_id)
    return render(request, 'challenges/글열람.html', {'challenge': challenge})


def challenge_create(request):
    if request.method == "POST":
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.author = request.user
            challenge.created_date = timezone.now()

            challenge.save()  # DB에 적용

            # 방금 생성한 PK와 일치하는 챌린지의 상세페이지로 이동
            return redirect('challenge_detail', pk=challenge.pk)

    # POST 요청이 없는 경우
    else:
        # 빈 폼 전달
        form = challengeForm()

    # 챌린지 생성 페이지
    return render(request, 'challenges/챌린지 생성 상세.html', {'form': form})
