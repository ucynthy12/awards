from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile,Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields =['id','title','image', 'url','details','user','published']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields =('name','profile_picture','bio')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    posts = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'profile', 'posts']