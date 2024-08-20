from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Like, Post

@permission_classes([IsAuthenticated])  #문제생길시 잠시삭제
def like_post(request, post_id):
    user = request.user
    if request.method == "POST":
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'status': 'error', 'message': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        # 좋아요가 이미 존재하는지 확인
        existing_like = Like.objects.filter(user=user, post=post).first()

        if existing_like:
            # 좋아요가 이미 존재하면 제거
            existing_like.delete()
            return Response({'status': 'success', 'message': 'Like removed.'}, status=status.HTTP_200_OK)
        else:
            # 좋아요가 없으면 추가
            Like.objects.create(user=user, post=post)
            return Response({'status': 'success', 'message': 'Like added.'}, status=status.HTTP_201_CREATED)

