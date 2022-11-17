from dataclasses import field
from pyexpat import model
from rest_framework import serializers

from .models import Friend, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=('password',)

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model=Friend
        fields='__all__'