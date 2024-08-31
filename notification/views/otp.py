from django.http import Http404
from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

from filters import DynamicSearchFilter
from paginator import CustomPagination
from languages.en.error import *
from languages.en.success import *
from notification.models import OTP
from notification.serializers import OTPSerializer


class OTPViewset(viewsets.ModelViewSet):
    queryset = OTP.objects.all()
    serializer_class = OTPSerializer
    pagination_class = CustomPagination
    filter_backends = (DynamicSearchFilter,)
    parser_class = (FileUploadParser,)
    authentication_classes = []
    permission_classes = []

    def create(self, request, version):
        serializer = OTPSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            result = {
                "success": {
                    'message': OTP_SENT
                },
            }
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk=None, mobile=None, used_for=None):
        try:
            if pk is not None:
                return OTP.objects.get(pk=pk)
            else:
                return OTP.objects.get(mobile=mobile, used_for=used_for)
        except OTP.DoesNotExist:
            return None

    def retrieve(self, request, version, pk=None):
        if pk is not None:
            otp = self.get_object(pk)
        else:
            otp = self.get_object(None, request.data.get(
                'mobile'), request.data.get('used_for'))
        serializer = OTPSerializer(otp, context={'request': request})
        return Response(serializer.data)

    def update(self, request, version, pk=None):
        otp = self.get_object(pk)
        serializer = OTPSerializer(
            otp, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            result = {
                "success": {
                    'message': OTP_SENT
                },
            }
            return Response(result, status=status.HTTP_200_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, version, pk=None):
        pass

    def destroy(self, request, version, pk=None, mobile=None, used_for=None):
        if pk is not None:
            otp = self.get_object(pk)
        else:
            otp = self.get_object(None, request.data.get(
                'mobile'), request.data.get('used_for'))
        otp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def verify(self, request, version):
        mobile = request.data.get('mobile', 'None')
        used_for = request.data.get('used_for', 'None')
        user_otp = request.data.get('otp', 'None')
        if mobile is None or used_for is None or user_otp is None:
            raise serializers.ValidationError([OTP_BAD_DATA_ERR])
        otp = self.get_object(None, mobile, used_for)
        if user_otp == otp.otp:
            otp.delete()
            result = {
                "success": {
                    'message': OTP_VERIFICATION_SUCCESS
                },
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            raise serializers.ValidationError([OTP_NOT_MATCHED_ERR])

    @action(detail=False, methods=['post'])
    def resend(self, request, version):
        mobile = request.data.get('mobile', 'None')
        used_for = request.data.get('used_for', 'None')
        if mobile is None or used_for is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        otp = self.get_object(None, mobile, used_for)
        print(request.data)
        serializer = OTPSerializer(
            otp, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": OTP_RESENT}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
