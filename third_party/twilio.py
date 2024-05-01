
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings


class Twilio:
    API_SID = settings.TWILIO_ACCOUNT_SID
    API_AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
    MESSAGING_SID = settings.TWILIO_MESSAGE_SERVICE_SID
    TWILIO_NUMBER = settings.TWILIO_FROM

    # print(API_SID,API_AUTH_TOKEN,  MESSAGING_SID, TWILIO_NUMBER)

    def send_otp_code(self, phone_number, message, channel):
        if channel == 'voice':
            return self.send_otp_via_voice_call(phone_number, message)
        if channel == 'sms':
            return self.send_otp_via_sms(phone_number, message)

    def send_otp_via_voice_call(self, mobile, message):
        client = Client(self.API_SID, self.API_AUTH_TOKEN)
        call = client.calls.create(
            twiml=f"<Response><Say voice='alice'>{message}</Say><Pause length='1'/><Say>{message}</Say><Pause length='1'/><Say>Goodbye</Say></Response>",
            to="+91" + mobile,
            from_=self.TWILIO_NUMBER
        )

        print(call.sid)

    def send_otp_via_sms(self, mobile, message):
        print(mobile, message)
        res_status = ""
        msg = ""
        client = Client(self.API_SID, self.API_AUTH_TOKEN)
        try:
            message = client.messages.create(
                to=mobile,
                from_=self.TWILIO_NUMBER,
                body=message,
                messaging_service_sid=self.MESSAGING_SID,
            )
            res_status = "success"
            msg = ""
            print(message)
        except TwilioRestException as e:
            msg = e.msg
        return res_status, msg
