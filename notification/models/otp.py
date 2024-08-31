from django.db import models

USUAGE = (
    ('reg', 'Registration'),
    ('fp', 'Forgot Password'),
    ('rmn', 'RMN'),
    ('custom', 'Custom'),
    ('otp', 'Otp'),
    ('oth', 'Others')
)


class OTP(models.Model):
    mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    otp = models.CharField(max_length=10, blank=True, null=True)
    used_for = models.CharField(
        max_length=20,
        choices=USUAGE,
        default='',
        null=True
    )
    otp_attempts = models.SmallIntegerField(blank=True, null=True)
    otp_sent = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
