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

class CommentListCreateAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        
        request.data['comment_by'] = User.objects.get(email=request.user).id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'message': 'comment created', 'data':serializer.data}, status.HTTP_201_CREATED,)
        else:
            return Response({'message': 'something went wrong', 'data': serializer.errors}, status.HTTP_405_METHOD_NOT_ALLOWED,)


    def get(self, request):
        
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        if serializer.data:
            return Response({'message': 'showing comment', 'data':serializer.data}, status.HTTP_200_OK,)
        else:
            return Response({'message': 'no data found', 'data': []}, status.HTTP_404_NOT_FOUND)


class CommentRetrieveUpdateDestroyAPIViewAPIView(APIView):

    def get(self, request, pk, *args, **kwargs):
        print(pk)
        try:
            comment = Comment.objects.get(id=pk)
            serializer = CommentSerializer(comment)
            return Response({'message': 'showing Comment', 'data':serializer.data}, status.HTTP_200_OK)
        except:
            return Response({'message': 'no data found', 'data': []}, status.HTTP_404_NOT_FOUND)



    def put(self, request, pk, *args, **kwargs):
        print(pk)
        comment = Comment.objects.get(id=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            return Response({'message': 'comment updated', 'data':serializer.data}, status.HTTP_200_OK)
        else:
            return Response({'message': 'something went wrong', 'data': serializer.errors}, status.HTTP_405_METHOD_NOT_ALLOWED)


    def delete(self, request, pk, *args, **kwargs):
        try:
            print(pk)
            comment = Comment.objects.get(id=pk)
            comment.delete()
            return Response({'message': 'Comment deleted', 'data':[]}, status.HTTP_200_OK)
        except:
            return Response({'message': 'no data found', 'data': []}, status.HTTP_404_NOT_FOUND)
