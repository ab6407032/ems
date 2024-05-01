import uuid
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from common.middlewares import current_user


class BaseModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        max_length=25,
        blank=True,
        editable=False,
        default='',
        on_delete=models.CASCADE,
        related_name='%(class)s_createdby'
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        max_length=25,
        blank=True,
        editable=False,
        default='',
        on_delete=models.CASCADE,
        related_name='%(class)s_modifiedby'
    )

    class Meta:
        abstract = True
        ordering = ('-created_on', )

    @staticmethod
    def get_current_user():
        return current_user.get_current_user()

    def set_user_fields(self, user):
        """
        Set user-related fields before saving the instance.
        If no user with a primary key is given the fields are not
        set.
        """
        if user and user.pk:
            if not self.pk:
                self.created_by = user
            self.modified_by = user

    def save(self, *args, **kwargs):
        # self.modified_by = now()
        current_user = self.get_current_user()
        self.set_user_fields(current_user)
        super(BaseModel, self).save(*args, **kwargs)

