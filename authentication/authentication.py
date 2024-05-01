from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .languages.en.authenticate import *
from user.models import User
from django.db.models import Q


class Authentication:
    def authenticate(self, pk, password = False):
        result = User.objects.filter(Q(email=pk) | Q(profile__mobile=pk)).first()

        if result is not None:
            if password:
                user = authenticate(username=result.email,  password=password)
            else:
                user = result
        else:
            raise serializers.ValidationError([USER_NOT_FOUND])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            groups = ""
            # for g in user.groups.all():
            #     groups = groups + g.name + ","
            # if groups.endswith(','):
            #     groups = groups[:-1]
            #payload['auth'] = groups
            #token = jwt_encode_handler(payload)
            #'refresh': str(refresh),
            #'access': str(refresh.access_token),
            return user, str(refresh.access_token)
        else:
            raise serializers.ValidationError([INCORRECT_PIN])




