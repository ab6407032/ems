from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from user.managers import UserManager
from model_utils import Choices
from common.models import BaseModel

USER_TYPE = Choices(
    ('staff', 'Staff'),
    ('user', 'User'),
    ('admin', 'Admin'),
    ('agent', 'Agent'),
)
STATUS = Choices(
    ('active', 'Active'),
    ('suspended', 'Suspended'),
)


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    screen_name = models.CharField(_('Screen Name'),  max_length=20, default='', null=True, blank=True,)
    user_type = models.CharField(choices=USER_TYPE, max_length=30, default='', null=True, blank=True,
                                 verbose_name="User Type")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_logged_in = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS, max_length=30, default='', null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True)
    failed_attempts = models.PositiveSmallIntegerField(null=True, blank=True)
    groups = models.ForeignKey(Group, default='', null=True, blank=True, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name="profile")
    first_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="First Name")
    middle_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Middle Name")
    last_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Last Name")
    mobile = models.CharField(
        max_length=15, verbose_name="Mobile No", null=True, blank=True,)
    mobile_alt = models.CharField(max_length=10, blank=True, null=True, verbose_name="Alternate Mobile No")
    is_online = models.BooleanField(default = False)

    def __str__(self):
        return self.user.email
    

class Address(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="address")
    address_line1 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Address Line 1")
    address_line2 = models.CharField(max_length=255, null=True, blank=True, verbose_name="Address Line 2")
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name="City")
    state = models.CharField(max_length=50, null=True, blank=True, verbose_name="State")
    country = models.CharField(max_length=50, null=True, blank=True, verbose_name="Country")
    pin = models.CharField(max_length=7, null=True, blank=True, verbose_name="Pin")
    latitude = models.CharField(max_length=255, null=True, blank=True, verbose_name="Latitude")
    longitude = models.CharField(max_length=255, null=True, blank=True, verbose_name="Longitude")
    google_address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Google Address")

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

