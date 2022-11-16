from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenBlacklistView

from account.views.API.account import *

urlpatterns = [
    path('register/', CustomerListCreateAPIView.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('login/', LoginAPIView.as_view(),),
    path('logout/', LogoutAPIVIEW.as_view(), name='token_blacklist'),

]
