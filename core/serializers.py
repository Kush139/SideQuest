from rest_framework import serializers
from .models import Profile, Post, LikePost, FollowerCount
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['user', 'full_name', 'id_user', 'bio', 'profileimg', 'location']

    def get_user(self, obj):
        return obj.user.username

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'caption', 'created_at', 'num_of_likes']

class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = ['post_id', 'username']

class FollowerCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowerCount
        fields = ['follower', 'user']
