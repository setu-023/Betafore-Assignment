from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import FriendSerializer, UserSerializer
from account.models import Friend, User


class sendFriendRequestAPIView(ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        try:
            print(request.user)
            user = User.objects.get(email=request.user)
            print(user)
            send_to = request.data['send_to']
        except Exception as e:
            return Response({'message': f'this field is requored: {e}', 'data': []}, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        try:
            friend = Friend.objects.get(user=user, sent_friend_request=send_to)
            return Response({'msg': 'friend request has been sent previously', 'data':[]}, status.HTTP_200_OK,)

        except:
            friend = Friend.objects.create(user=User.objects.get(email=request.user),
                                           sent_friend_request=send_to)

            friend2 = Friend.objects.create(user=User.objects.get(id=send_to),
                                           friend_request= User.objects.get(email=request.user).id)
            serializer = FriendSerializer(friend).data
        return Response({'msg': 'friend request has been sent', 'data':serializer}, status.HTTP_201_CREATED,)



class acceptFriendRequestAPIView(ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        try:
            print(request.user)
            user = User.objects.get(email=request.user)
            print(user)
            get_friend = request.data['friend']
            response = request.data['response']

        except Exception as e:
            return Response({'message': f'this field is required: {e}', 'data': []}, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        try:
            friend = Friend.objects.get(user=user, friend_request=get_friend)
            if response=='accecpt':
                friend.friend_list = get_friend
                friend.friend_request = None
                friend.save()
                friend = Friend.objects.get(user=User.objects.get(id=get_friend), sent_friend_request=User.objects.get(email=user).id)
                friend.friend_list = User.objects.get(email=request.user).id
                friend.sent_friend_request = None
                friend.save()
                return Response({'msg': 'friend request has been accecpted', 'data':[]}, status.HTTP_200_OK,)
            else:
                friend.friend_request = None
                friend.save()
                friend = Friend.objects.get(user=User.objects.get(id=get_friend), sent_friend_request=User.objects.get(email=user).id)
                friend.sent_friend_request = None
                friend.save()
            return Response({'msg': 'friend request has been declined', 'data':[]}, status.HTTP_200_OK,)

        except Exception as e:
            return Response({'msg': 'something went wrong', 'data':str(e)}, status.HTTP_201_CREATED,)


class myFriendListAPIView(ListCreateAPIView):

    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        
        try:
            print(request.user)
            friends = Friend.objects.get(user=request.user)
            print(friends.friend_list)
            serializer = FriendSerializer(friends).data
            return Response({ 'message': 'showing data', 'data': serializer}, status.HTTP_405_METHOD_NOT_ALLOWED)
        except Exception as e:
            print(e)
            return Response({'message': f'this field is required: {e}', 'data': []}, status.HTTP_405_METHOD_NOT_ALLOWED)
        