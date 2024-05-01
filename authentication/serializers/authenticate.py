from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from user.models import User, Profile
from notification.otp import OneTimePassword
from authentication.languages.en.authenticate import *
from django.db.models import Q
from datetime import datetime

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'mobile', 'mobile_alt', 'middle_name', 'last_name')
        #read_only_fields = ('created_by', 'modified_by')


class UserRegisterGoogleSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)  

    class Meta:
        model = User
        fields = ('id', 'email', 'user_type', 'profile')

    def create(self, validated_data):
        screen_name = validated_data.pop('screen_name')  if 'screen_name' in validated_data else None
        split_email = validated_data.get('email').split('@')

        screen_name = split_email[0]

        # user = User.objects.create(screen_name=screen_name, **validated_data)

        is_already_exists = User.objects.filter(email=validated_data.get('email')).exists()
        if is_already_exists:
            return User.objects.filter(email=validated_data.get('email')).first()
        else:
            if validated_data.get('profile'):
                profile = validated_data.pop('profile')
            else:
                profile = None     

            user = User.objects.create(screen_name=screen_name, **validated_data)

            user.password = User.objects.make_random_password()
            user.save()

            if profile is not None:
                if 'user' in profile:
                    profile.pop('user')
                Profile.objects.create(user=user, **profile)
            return user

class UserRegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    mobile = serializers.SerializerMethodField(required=False)    
    otp = serializers.CharField(max_length=4, required=True, read_only=False)
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'user_type', 'is_staff', 'is_superuser',
                  'is_active', 'profile', 'address', 'otp', 'mobile', 'screen_name')

    def validate_email(self, email):
        is_already_exists = User.objects.filter(email=email).exists()
        if is_already_exists:
            print(USER_EXISTS)
            raise serializers.ValidationError(USER_EXISTS)
        self.pk = email
        return email

    def validate_mobile(self, mobile):
        is_already_exists = User.objects.filter(profile__mobile=mobile).exists()
        if is_already_exists:
            raise serializers.ValidationError(USER_EXISTS)
        self.pk = mobile
        return mobile

    def validate(self, data):
        if self.pk:
            o = OneTimePassword()
            is_valid = o.is_otp_valid(self.pk, data.get("otp"))
            return data
        raise serializers.ValidationError(BAD_DATA)


    """def validate_password(self, value):
        password_validation.validate_password(value)
        return value"""

    def create(self, validated_data):
        mobile = validated_data.pop('mobile')  if 'mobile' in validated_data else None
        screen_name = validated_data.pop('screen_name')  if 'screen_name' in validated_data else None
        address = validated_data.pop('address')  if 'address' in validated_data else None
        profile = validated_data.pop('profile')  if 'profile' in validated_data else None
        otp = validated_data.pop('otp')  if 'otp' in validated_data else None

        split_email = validated_data.get('email').split('@')

        screen_name = split_email[0]

        user = User.objects.create(screen_name=screen_name, **validated_data)

        user.password = make_password(validated_data.get('password'))
        user.save()
            
        if self.pk:
            o = OneTimePassword()
            o.del_otp(self.pk, otp)


        if profile is not None:
            if 'user' in profile:
                profile.pop('user')
            Profile.objects.create(user=user, **profile)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100, required=False)
    mobile = serializers.CharField(max_length=15, required=False)
    password = serializers.CharField(required=True, write_only=True)

class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'is_staff', 'is_superuser', 'is_logged_in', 'user_type', 'screen_name')
        read_only_fields = ('id', 'is_active', 'is_staff', 'is_superuser', 'is_logged_in', 'user_type', 'screen_name')

class ForgotPassSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100, required=False)
    mobile = serializers.CharField(max_length=15, required=False)

    def validate_email(self, email):
        is_already_exists = User.objects.filter(email=email).exists()
        if is_already_exists == False:
            raise serializers.ValidationError(USER_NOT_FOUND)
        self.pk = email
        return email

    def validate_mobile(self, mobile):
        is_already_exists = User.objects.filter(profile__mobile=mobile).exists()
        if is_already_exists == False:
            raise serializers.ValidationError(USER_NOT_FOUND)
        self.pk = mobile
        return mobile

    def create(self, validated_data):
        o = OneTimePassword();
        user = User.objects.filter(Q(email=self.pk) | Q(profile__mobile=self.pk)).first()
        # otp = o.generate_otp(user.email, user.profile.mobile, "fp",)
        otp = o.generate_otp(user.email, None, "fp",)
        return otp

class ResetPassSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(required=True, write_only=True)
    mobile = serializers.CharField(max_length=15, required=False)
    otp = serializers.CharField(max_length=4, required=True, read_only=False)

    def validate_email(self, email):
        is_already_exists = User.objects.filter(email=email).exists()
        if is_already_exists == False:
            raise serializers.ValidationError(USER_NOT_FOUND)
        self.pk = email
        return email

    def validate_mobile(self, mobile):
        is_already_exists = User.objects.filter(profile__mobile=mobile).exists()
        if is_already_exists == False:
            raise serializers.ValidationError(USER_NOT_FOUND)
        self.pk = mobile
        return mobile

    def validate(self, data):       
        if self.pk:
            o = OneTimePassword()
            is_valid = o.is_otp_valid(self.pk, data.get("otp"))
            return data
        raise serializers.ValidationError(BAD_DATA)

    def create(self, validated_data):
        user = User.objects.filter(Q(email=self.pk) | Q(profile__mobile=self.pk)).first()
        user.password = make_password(validated_data.get('password'))
        user.save()

        
        if self.pk:
            o = OneTimePassword()
            o.del_otp(self.pk, validated_data.get("otp"))
            return {"email": user.email, "mobile": user.profile.mobile, "otp": validated_data.get('otp')}
        raise serializers.ValidationError(BAD_DATA)
