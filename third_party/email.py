from django.core.mail import send_mail
from django.conf import settings

class Email:
    def email(self, subject, message, receiver):
        result = send_mail(
                            subject,
                            '',
                            settings.EMAIL_HOST_USER,
                            [receiver],
                            fail_silently=False,
                            html_message=message
                        )
        if result:
            return True
        return False
            