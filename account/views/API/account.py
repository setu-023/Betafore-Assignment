from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import UserSerializer
from account.models import User


class CustomerListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter()

    def get_permissions(self):
      
        if self.request.method == 'GET':
            return (permissions.IsAdminUser(),)
    
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)
        

    def create(self, request, *args, **kwargs):

        try:
            user = User.objects.create(
                email=self.request.data['email'],
                name=self.request.data['name']
            )          
            user.set_password(self.request.data['password'])
            user.save()
            serializer = self.get_serializer(user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(data={'message': f'this field is required: {e}'}, status=status.HTTP_409_CONFLICT)


class LoginAPIView(ListCreateAPIView):
    
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data['email'])
            password = request.data['password']
            otp = (request.data['otp'])
        except Exception as e:
            return Response(data={'message': f'this field is requored: {e}'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if user.check_password(password):
            if user.otp==str(otp):
                get_token = refresh = get_tokens_for_user(user)
                print(get_token)
                return Response({'msg': 'successfully logged in', 'data':get_token}, status.HTTP_200_OK,)
            else:
                return Response({'msg': 'Invalid otp', }, status.HTTP_405_METHOD_NOT_ALLOWED,)
        else:
            return Response({'msg': 'Invalid password', }, status.HTTP_405_METHOD_NOT_ALLOWED,)


class LogoutAPIVIEW(ListCreateAPIView):

    def post(self, request):

        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()   
            return Response({'msg': 'logout', 'data':[]}, status.HTTP_200_OK,)
        except Exception as e:
            return Response(data={'message': f'{e}', 'data':[]}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }