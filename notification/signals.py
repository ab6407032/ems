from django.db.models import signals
from django.dispatch import receiver
from rest_framework import serializers
from notification.models import OTP
from sms import *
from notification.otp import OneTimePassword


@receiver(signals.pre_save, sender=OTP)
def create_otp(sender, instance, **kwargs):
    o = OneTimePassword()
    o.generate_otp(instance.email, instance.mobile, instance.used_for)

""""
@receiver(signals.post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Address.objects.create(user=instance)
"""



