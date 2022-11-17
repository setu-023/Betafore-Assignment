from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenBlacklistView

from account.views.API.account import *
from account.views.API.friend import *


urlpatterns = [
    path('register/', CustomerListCreateAPIView.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('login/', LoginAPIView.as_view(),),
    path('logout/', LogoutAPIVIEW.as_view(), name='token_blacklist'),

    path('sendFriendRequest/', sendFriendRequestAPIView.as_view(), name='sendFriendRequest'),
    path('accecptFriendRequest/', acceptFriendRequestAPIView.as_view(), name='sendFriendRequest'),
    path('myFriendList/', myFriendListAPIView.as_view(), name='sendFriendRequest'),

]
