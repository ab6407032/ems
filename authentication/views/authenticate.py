from django.core.exceptions import ImproperlyConfigured
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from authentication.authentication import *
from django.db.models import Q
from authentication.languages.en.authenticate import *
from common.languages.en.otp import *
from authentication.serializers.authenticate import (
    AuthUserSerializer, UserRegisterSerializer, UserLoginSerializer, ResetPassSerializer,
    ForgotPassSerializer, ProfileSerializer, UserRegisterGoogleSerializer
)
from common.serializers import EmptySerializer
from user.models import Profile
from third_party.google import Google

class AuthenticateViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': UserLoginSerializer,
        'register': UserRegisterSerializer,
        'forgot_password': ForgotPassSerializer,
        'reset_password': ResetPassSerializer,
        'google_login': UserRegisterGoogleSerializer
    }
    authentication_classes = []
    permission_classes = []
    lookup_field = 'email'

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def get_object(self, pk=None):
        try:
            return User.objects.filter(Q(email=pk) | Q(profile__mobile=pk)).first()
        except User.DoesNotExist:
            return None

    def get_pk(self, request):
        pk = None
        if 'email' in request.data:
            if request.data['email']:
                pk = request.data['email']
        if 'mobile' in request.data:
            if request.data['mobile']:
                pk = request.data['mobile']
        #print(pk)
        return pk

    @action(methods=['POST', ], detail=False)
    def login(self, request, version):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth = Authentication()
        pk = self.get_pk(request)
        user, token = auth.authenticate(pk, serializer.validated_data.get('password'))
        # import ipdb;ipdb.set_trace()
        # g = user.groups.all()[0]
        # ipdb > g.privileges.all()
        data = AuthUserSerializer(user).data
        user.is_logged_in = True
        user.save()
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = None

        if hasattr(user, 'profile') and user.profile is not None:
           profile = ProfileSerializer(user.profile).data
        result = {
            'token': token,
            "success": {
                'message': "Successfully logged in"
            }, 
            'profile': profile 
        }
        result.update(data)
        return Response(data=result, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register(self, request, version):
        pk = self.get_pk(request)
        #print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        auth = Authentication()
        user, token = auth.authenticate(pk, serializer.validated_data.get('password'))
        user.is_logged_in = True
        user.save()
        data = AuthUserSerializer(user).data
        result = {'token': token, "message": REGISTRATION_SUCCESS, 'profile': ProfileSerializer(user.profile).data }
        result.update(data)
        return Response(data=result, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def forgot_password(self, request, version):
        pk = self.get_pk(request)
        user = self.get_object(pk)
        if user is not None:
            serializer = self.get_serializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message": OTP_SENT, "mobile": user.profile.mobile, "email": user.email, }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({[NOT_REGISTERED]}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def reset_password(self, request, version):
        pk = self.get_pk(request)
        user = self.get_object(pk)
        if user is not None:
            serializer = self.get_serializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                auth = Authentication()
                user, token = auth.authenticate(pk, request.data.get('password'))
                data = AuthUserSerializer(user).data
                result = {'token': token, "message": PASSWORD_CHANGE_SUCCESS}
                result.update(data)
                return Response(data=result, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(
                {[NOT_REGISTERED]}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['POST', ], detail=False)
    def logout(self, request, version):
        user = User.objects.get(email=request.user.email)        
        user.is_logged_in = False
        user.save()
        request.session.flush()
        data = {'message': LOGGED_OUT}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def google_login(self, request, version):   
        google = Google()     
        check_google_token = google.login(request.data.get('token'))
        print(check_google_token)
        print(request.data.get('email'))
        if not User.objects.filter(email=request.data.get('email')).exists():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        auth = Authentication()
        user, token = auth.authenticate(request.data.get('email'))
        user.is_logged_in = True
        user.save()
        data = AuthUserSerializer(user).data
        profile = None
        if  hasattr(user, 'profile'):
            profile = ProfileSerializer(user.profile).data
        result = {'token': token, "message": SUCCESS_MSG, 'profile':  profile}
        result.update(data)
        return Response(data=result, status=status.HTTP_201_CREATED)

