from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'email']

class SendFriendRequest(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'email', 'request_sent']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

class UserRequest(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','request_received']


class UserFriendList(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','friend_list']

class UserSent(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["request_sent"]

class SearchSerializer(serializers.ModelField):
    user = serializers.CharField(source='User')
    class Meta:
        model = Profile
        fields = ['id',"email"]
