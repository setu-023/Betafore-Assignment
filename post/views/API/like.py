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

class LikeListCreateAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        try:
            like = Like.objects.get(post=request.data['post'], liked_by=User.objects.get(email=request.user).id)
            like.delete()
            return Response({ 'message': 'like has been removed', 'data':[]}, status.HTTP_200_OK,)

        except:
            request.data['liked_by'] = User.objects.get(email=request.user).id
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({ 'message': 'like created', 'data':serializer.data}, status.HTTP_201_CREATED,)
            else:
                return Response({'message': 'something went wrong', 'data': serializer.errors}, status.HTTP_200_OK,)


    def get(self, request):
        
        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)
        if serializer.data:
            return Response({'message': 'showing data', 'data':serializer.data}, status.HTTP_200_OK,)
        else:
            return Response({'message': 'no data found', 'data': []}, status.HTTP_404_NOT_FOUND)


class LikeRetrieveUpdateDestroyAPIViewAPIView(APIView):

    def get(self, request, pk, *args, **kwargs):
        print(pk)
        try:
            like = Like.objects.get(id=pk)
            serializer = LikeSerializer(like)
            return Response({'message': 'showing data', 'data':serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'message': 'no data found', 'data': []}, status.HTTP_404_NOT_FOUND)


    def put(self, request, pk, *args, **kwargs):

        print(pk)
        like = Like.objects.get(id=pk)
        serializer = LikeSerializer(like, data=request.data, partial=True)
        if serializer.is_valid():
            return Response({'message': 'data updated', 'data':serializer.data, 'status':status.HTTP_200_OK})
        else:
            return Response(data={'message': 'something went wrong', 'data': serializer.errors, 'status':status.HTTP_405_METHOD_NOT_ALLOWED})



    def delete(self, request, pk, *args, **kwargs):

        try:
            print(pk)
            like = Like.objects.get(id=pk)
            like.delete()
            return Response({'message': 'data deleted', 'data':[]}, status.HTTP_200_OK)
        except:
            return Response({'message': 'no data found', 'data': []}, status.HTTP_404_NOT_FOUND)
