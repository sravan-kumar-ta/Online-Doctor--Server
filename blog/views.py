from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blog import serializers
from blog.models import Posts


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6


class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.PostSerializer
    queryset = Posts.objects.all()
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(is_public=True)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if request.user.role == 'doctor':
            serializer = self.serializer_class(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response({'message': 'Only doctors can create a blog.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def is_author(self):
        instance = self.get_object()
        return self.request.user == instance.author

    def update(self, request, *args, **kwargs):
        if self.is_author():
            return super().update(request, *args, **kwargs)
        return Response({'message': 'Only authors can edit post.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def destroy(self, request, *args, **kwargs):
        if self.is_author():
            return super().destroy(request, *args, **kwargs)
        return Response({'message': 'Only authors can delete a post.'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(['GET'], detail=False)
    def get_my_posts(self, request):
        queryset = self.get_queryset().filter(author=request.user)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(['GET'], detail=True)
    def like_or_dislike(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        liked_users = post.likes.all()
        if user in liked_users:
            post.likes.remove(user)
            return Response({'message': 'not liked', 'total_likes': post.total_likes()}, status=status.HTTP_200_OK)
        post.likes.add(user)
        return Response({'message': 'liked', 'total_likes': post.total_likes()}, status=status.HTTP_201_CREATED)

    @action(['GET'], detail=True)
    def liked_or_not(self, request, *args, **kwargs):
        post = self.get_object()
        liked_users = post.likes.all()
        if request.user in liked_users:
            return Response({'message': 'liked'})
        return Response({'message': 'not liked'})
