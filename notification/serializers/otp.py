from django.db.models import Q
from rest_framework import serializers
from notification.otp import OneTimePassword
from user.models import User
from languages.en.error import *
from notification.models import OTP


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'

    def create(self, validated_data):
        mobile = validated_data.get('mobile', None)
        email = validated_data.get('email', None)
        used_for = validated_data.get('used_for', None)
        user = None
        if used_for == "fp":
            if mobile is not None:
                user = User.objects.filter(
                    profile__mobile__icontains=mobile).first()
                if user:
                    mobile = user.profile.mobile

        # if used_for == "reg":
        #     if mobile is not None:
        #         mobile_exists = User.objects.filter(profile__mobile__icontains=mobile).exists()
        #         if mobile_exists:
        #             raise serializers.ValidationError([USER_EXISTS_ERR])
        #     if email is not None:
        #         email_exists = User.objects.filter(email=email).exists()
        #         if email_exists:
        #             raise serializers.ValidationError([USER_EXISTS_ERR])

        # if mobile is not None and email is None and used_for is not None:

        # if email is not None  and mobile is None and used_for is not None:
        #     o = OneTimePassword()
        #     otp = o.generate_otp(email, None, used_for)
        #     return otp
        # if email is not None and mobile is not None and used_for is not None:
        #     o = OneTimePassword()
        #     otp = o.generate_otp(email, mobile, used_for)
        #     return otp
        o = OneTimePassword()
        otp = o.generate_otp(email, mobile, used_for)
        return otp

        # profile__mobile=data['mobile'][-10:]

    def validate(self, data):
        user = None
        is_already_exists = False
        if data.get('email'):
            email = data.get('email', None)
            is_already_exists = User.objects.filter(email=email).exists()
            if is_already_exists and data['used_for'] == 'reg':
                print(USER_EXISTS_ERR)
                raise serializers.ValidationError([USER_EXISTS_ERR])
            otp = OTP.objects.filter(email=email).filter(
                Q(used_for=data['used_for'])).first()

        if data.get('mobile'):
            mobile = data.get('mobile', None)
            is_already_exists = User.objects.filter(
                profile__mobile=mobile).exists()
            if is_already_exists and data['used_for'] == 'reg':
                print(USER_EXISTS_ERR)
                raise serializers.ValidationError([USER_EXISTS_ERR])
            otp = OTP.objects.filter(mobile=mobile).filter(
                Q(used_for=data['used_for'])).first()

        if otp is not None:
            if is_already_exists and data['used_for'] == 'reg':
                print(USER_EXISTS_ERR)
                raise serializers.ValidationError([USER_EXISTS_ERR])

            if otp.otp_attempts >= 3:
                raise serializers.ValidationError([OTP_ATTEMPTS_ERR])

        return data
