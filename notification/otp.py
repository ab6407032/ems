from rest_framework import serializers
from .models import OTP
from django.db.models import Q
import random
from languages.en.error import *
from third_party.twilio import Twilio
from third_party.email import Email
from notification.models import Template

UPPER_LIMIT = 1001
LOWER_LIMIT = 9999

"""One time password utility class"""


class OneTimePassword:
    """Generate and save a four digit random one time password start"""

    def get_template(self):
        notification = Template.objects.filter(
            used_for="otp", active=True).first()
        return notification.subject, notification.body_html, notification.body
        # return "OTP FOR TITAS", "Your otp is {otp}"

    def send_otp(self, mobile, otp, used_for):
        t = Twilio()
        subject, message_html, sms = self.get_template()
        print(sms)
        sms = sms.replace('{otp}', str(otp))
        res_data, message = t.send_otp_code(mobile, sms, 'sms')
        print(res_data)
        if res_data == 'success':
            return True
        else:
            raise serializers.ValidationError([message])

    def send_otp_email(self, email, otp, used_for):
        t = Email()
        subject, message_html, sms = self.get_template()
        sms = sms.replace('{otp}', str(otp))
        print(subject, sms, email)
        res_data = t.email(subject, sms, email)
        print(res_data)
        if res_data:
            return True
        else:
            raise serializers.ValidationError([OTP_EMAIL_ERR])

    def generate_otp(self, email=None, mobile=None, used_for=None):
        print(email)
        print(mobile)
        print(used_for)
        one_time_pass = random.randrange(UPPER_LIMIT, LOWER_LIMIT + 1)
        otp = None
        if email is not None and mobile is None and used_for:
            otp = OTP.objects.filter(Q(email=email)).filter(
                Q(used_for=used_for)).first()
        elif email is None and mobile is not None and used_for:
            otp = OTP.objects.filter(Q(mobile__icontains=mobile)).filter(
                Q(used_for=used_for)).first()
        elif email is not None and mobile is not None and used_for:
            otp = OTP.objects.filter(Q(email=email)).filter(
                Q(mobile__icontains=mobile)).filter(Q(used_for=used_for)).first()
        else:
            otp = None

        if otp is not None:
            if otp.otp_attempts >= 3:
                raise serializers.ValidationError([OTP_ATTEMPTS_ERR])
            else:
                if otp.mobile and otp.email is None:
                    result = self.send_otp(otp.mobile, one_time_pass, used_for)
                    if result:
                        print("hello")
                        otp.otp_attempts = otp.otp_attempts + 1
                        otp.otp = one_time_pass
                        otp.save()
                    else:
                        raise serializers.ValidationError([OTP_COMMON_ERR])

                elif otp.email and otp.mobile is None:
                    result = self.send_otp_email(
                        otp.email, one_time_pass, used_for)
                    if result:
                        print("hello")
                        otp.otp_attempts = otp.otp_attempts + 1
                        otp.otp = one_time_pass
                        otp.save()
                    else:
                        raise serializers.ValidationError([OTP_COMMON_ERR])
                elif otp.email and otp.mobile:

                    result = self.send_otp(otp.mobile, one_time_pass, used_for)
                    # result = self.send_otp_email(otp.email, one_time_pass, used_for)
                    if result:
                        print("hello")
                        otp.otp_attempts = otp.otp_attempts + 1
                        otp.otp = one_time_pass
                        otp.save()
                    else:
                        raise serializers.ValidationError([OTP_COMMON_ERR])
                else:
                    raise serializers.ValidationError([OTP_COMMON_ERR])
        else:
            if mobile is not None and email is None:
                result = self.send_otp(mobile, one_time_pass, used_for)
                if result:
                    otp = OTP.objects.create(mobile=mobile, otp=one_time_pass, used_for=used_for,
                                             otp_attempts=1)
                else:
                    raise serializers.ValidationError([OTP_COMMON_ERR])

            elif mobile is None and email is not None:
                result = self.send_otp_email(email, one_time_pass, used_for)
                print(result)
                if result:
                    otp = OTP.objects.create(email=email, otp=one_time_pass, used_for=used_for,
                                             otp_attempts=1)
                else:
                    raise serializers.ValidationError([OTP_COMMON_ERR])

            elif email is not None and mobile is not None:
                result = self.send_otp(mobile, one_time_pass, used_for)
                print(result)
                # result = self.send_otp_email(email, one_time_pass, used_for)
                if result:
                    otp = OTP.objects.create(email=email, mobile=mobile, otp=one_time_pass, used_for=used_for,
                                             otp_attempts=1)
                else:
                    raise serializers.ValidationError([OTP_COMMON_ERR])
            else:
                raise serializers.ValidationError([OTP_COMMON_ERR])
        return otp

    """Check otp is present in the otp table or otp validity"""

    def is_otp_valid(self, pk, one_time_pass):
        print(pk, one_time_pass)
        try:
            result = OTP.objects.filter(Q(email=pk) | Q(
                mobile__icontains=pk)).filter(Q(otp=one_time_pass)).first()
            print(OTP.objects.filter(Q(email=pk) | Q(mobile__icontains=pk)).filter(
                Q(otp=one_time_pass)).query)
            if result:
                return True
            else:
                raise serializers.ValidationError([OTP_COMMON_ERR])
        except OTP.DoesNotExist:
            raise serializers.ValidationError([OTP_COMMON_ERR])

    """Deleting the otp after its usage"""

    def del_otp(self, pk, otp):
        try:
            result = OTP.objects.filter(Q(email=pk) | Q(
                mobile__icontains=pk)).filter(Q(otp=otp)).first()
            if result:
                result.delete()
                return True
            else:
                raise serializers.ValidationError([OTP_COMMON_ERR])
        except OTP.DoesNotExist:
            raise serializers.ValidationError([OTP_COMMON_ERR])
