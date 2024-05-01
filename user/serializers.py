from rest_framework import serializers
from user.models import User, Profile
from datetime import datetime


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'mobile', 'middle_name', 'last_name')
        # read_only_fields = ('mobile', 'mobile_alt')


class UserListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = User
        fields = ('id', 'email',  'user_type', 'is_staff',
                  'is_superuser', 'is_active', 'profile')
        

class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)


    class Meta:
        model = User
        fields = ('id', 'screen_name', 'email', 'password', 'user_type', 'is_staff', 'is_superuser', 'is_active', 'profile',
                  'address')


