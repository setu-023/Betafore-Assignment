from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from django.db.models import Q

from account.models import *
from account.serializers import *
from post.models import *
from post.serializers import *

class PostListCreateAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'message': 'post created', 'data':serializer.data}, status.HTTP_201_CREATED,)
        else:
            return Response({'message': 'something went wrong', 'data': serializer.errors}, status.HTTP_200_OK,)


    def get(self, request):
        
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        if serializer.data:
            return Response({'message': 'showing post', 'data':serializer.data}, status.HTTP_200_OK,)
        else:
            return Response({'message': 'no data found', 'data': []}, status.HTTP_404_NOT_FOUND)


class PostRetrieveUpdateDestroyAPIViewAPIView(APIView):

    def get(self, request, pk, *args, **kwargs):
        print(pk)
        try:
            post = Post.objects.get(id=pk)
            serializer = PostSerializer(post)
            return Response({'message': 'showing post', 'data':serializer.data, 'status':status.HTTP_200_OK})
        except:
            return Response(data={'message': 'no data found', 'data': [], 'status':status.HTTP_404_NOT_FOUND})



    def put(self, request, pk, *args, **kwargs):

        print(pk)
        post = Post.objects.get(id=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            return Response({'message': 'post updated', 'data':serializer.data, 'status':status.HTTP_200_OK})
        else:
            return Response(data={'message': 'something went wrong', 'data': serializer.errors, 'status':status.HTTP_405_METHOD_NOT_ALLOWED})



    def delete(self, request, pk, *args, **kwargs):

        try:
            print(pk)
            post = Post.objects.get(id=pk)
            post.delete()
            return Response({'message': 'post deleted', 'data':[], 'status':status.HTTP_200_OK})
        except:
            return Response(data={'message': 'no data found', 'data': [], 'status':status.HTTP_404_NOT_FOUND})


    
class SearchPeopleAPIViewAPIView(APIView):

    permission_classes=[permissions.IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        users = User.objects.filter(name__icontains=self.request.GET.get('q',''))
        serializer = UserSerializer(users, many=True)
        if users:
            return Response({'message': 'showing post', 'data':serializer.data}, status.HTTP_200_OK)
        else:
            return Response({'message': 'no data found', 'data': []}, status.HTTP_404_NOT_FOUND)


    
class AllPostAPIViewAPIView(APIView):

    permission_classes=[permissions.IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        friends = Friend.objects.get(user=request.user)
        get_friends = friends.friend_list
        print(get_friends)
        get_user = User.objects.get(email=request.user).id
        print(get_user)
        posts = Post.objects.filter(
                Q(owner__in=get_friends) | 
                Q(owner=get_user) 
             ).order_by('-created_at')
        if posts:
            serializer = PostSerializer(posts, many=True).data
            return Response({'message': 'showing post', 'data':serializer}, status.HTTP_200_OK)
        else:
            return Response({'message': 'no data found', 'data': []}, status.HTTP_404_NOT_FOUND)

